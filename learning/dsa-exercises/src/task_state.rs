//! A task's flags and reference count packed into one atomic word.
//! Real code: `tokio/src/runtime/task/state.rs`.

use std::sync::atomic::{AtomicUsize, Ordering::AcqRel, Ordering::Acquire};

pub const RUNNING: usize = 0b0001;
pub const COMPLETE: usize = 0b0010;
pub const NOTIFIED: usize = 0b0100;
pub const JOIN_INTEREST: usize = 0b1000;
pub const JOIN_WAKER: usize = 0b1_0000;
pub const CANCELLED: usize = 0b10_0000;

const STATE_MASK: usize = RUNNING | COMPLETE | NOTIFIED | JOIN_INTEREST | JOIN_WAKER | CANCELLED;
const REF_COUNT_MASK: usize = !STATE_MASK;
const REF_COUNT_SHIFT: usize = REF_COUNT_MASK.trailing_zeros() as usize;
pub const REF_ONE: usize = 1 << REF_COUNT_SHIFT;

/// One reference for the scheduler, one for the `JoinHandle`, one for the
/// `Notified` that is about to be scheduled.
pub const INITIAL_STATE: usize = (REF_ONE * 3) | JOIN_INTEREST | NOTIFIED;

#[derive(Debug, PartialEq)]
pub enum TransitionToRunning {
    Success,
    Cancelled,
    /// Already running or complete: the caller must just drop its reference.
    Failed,
}

pub struct State(AtomicUsize);

impl Default for State {
    fn default() -> Self {
        Self::new()
    }
}

impl State {
    pub fn new() -> Self {
        State(AtomicUsize::new(INITIAL_STATE))
    }

    pub fn load(&self) -> usize {
        self.0.load(Acquire)
    }

    pub fn ref_count(&self) -> usize {
        (self.load() & REF_COUNT_MASK) >> REF_COUNT_SHIFT
    }

    pub fn ref_inc(&self) {
        let prev = self.0.fetch_add(REF_ONE, AcqRel);
        assert!(prev <= isize::MAX as usize, "ref-count overflow");
    }

    /// Returns `true` if this was the last reference: the caller must free the task.
    pub fn ref_dec(&self) -> bool {
        let prev = self.0.fetch_sub(REF_ONE, AcqRel);
        assert!(prev & REF_COUNT_MASK >= REF_ONE, "ref-count underflow");
        prev & REF_COUNT_MASK == REF_ONE
    }

    /// NOTIFIED -> RUNNING, as a single compare-and-swap loop.
    pub fn transition_to_running(&self) -> TransitionToRunning {
        let mut curr = self.load();
        loop {
            assert!(curr & NOTIFIED != 0, "task must be notified to run");
            if curr & (RUNNING | COMPLETE) != 0 {
                return TransitionToRunning::Failed;
            }
            let next = (curr & !NOTIFIED) | RUNNING;
            match self.0.compare_exchange_weak(curr, next, AcqRel, Acquire) {
                Ok(_) if next & CANCELLED != 0 => return TransitionToRunning::Cancelled,
                Ok(_) => return TransitionToRunning::Success,
                Err(actual) => curr = actual,
            }
        }
    }

    /// RUNNING -> idle. Returns `true` if the task was woken while running and
    /// must be scheduled again.
    pub fn transition_to_idle(&self) -> bool {
        let prev = self.0.fetch_and(!RUNNING, AcqRel);
        prev & NOTIFIED != 0
    }

    /// Wake: set NOTIFIED. Returns `true` if the caller must schedule the task
    /// (it was idle and not already notified).
    pub fn transition_to_notified(&self) -> bool {
        let prev = self.0.fetch_or(NOTIFIED, AcqRel);
        prev & (RUNNING | COMPLETE | NOTIFIED) == 0
    }

    pub fn transition_to_complete(&self) {
        let prev = self.0.fetch_xor(RUNNING | COMPLETE, AcqRel);
        assert!(prev & RUNNING != 0 && prev & COMPLETE == 0);
    }

    pub fn cancel(&self) {
        self.0.fetch_or(CANCELLED, AcqRel);
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn layout() {
        assert_eq!(REF_COUNT_SHIFT, 6);
        assert_eq!(REF_ONE, 64);
        assert_eq!(State::new().ref_count(), 3);
    }

    #[test]
    fn lifecycle() {
        let s = State::new();
        assert_eq!(s.transition_to_running(), TransitionToRunning::Success);
        // Woken while running: no need to schedule now, but run again after idle.
        assert!(!s.transition_to_notified());
        assert!(s.transition_to_idle());
        assert_eq!(s.transition_to_running(), TransitionToRunning::Success);
        s.transition_to_complete();
        assert!(s.load() & COMPLETE != 0);
        assert!(!s.transition_to_notified());
        assert!(!s.ref_dec());
        assert!(!s.ref_dec());
        assert!(s.ref_dec(), "last reference frees the task");
    }

    #[test]
    fn cancelled_task_reports_cancelled() {
        let s = State::new();
        s.cancel();
        assert_eq!(s.transition_to_running(), TransitionToRunning::Cancelled);
    }

    #[test]
    fn concurrent_ref_counting() {
        let s = std::sync::Arc::new(State::new());
        let handles: Vec<_> = (0..8)
            .map(|_| {
                let s = s.clone();
                std::thread::spawn(move || {
                    for _ in 0..10_000 {
                        s.ref_inc();
                        assert!(!s.ref_dec());
                    }
                })
            })
            .collect();
        for h in handles {
            h.join().unwrap();
        }
        assert_eq!(s.ref_count(), 3);
    }
}
