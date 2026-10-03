//! FIFO-fair semaphore with partial permit assignment, and an RwLock built on it.
//! Real code: `tokio/src/sync/batch_semaphore.rs`, `tokio/src/sync/rwlock.rs`.
//!
//! Tokio's waiters live in an intrusive linked list inside the waiting futures and
//! are woken with `Waker`s. Here waiters are ids in a `VecDeque`, and "waking" means
//! returning the id from `release`.

use std::collections::VecDeque;

struct Waiter {
    id: u64,
    /// Permits still needed. Can be partially filled before the waiter is woken.
    needed: usize,
}

pub struct Semaphore {
    permits: usize,
    waiters: VecDeque<Waiter>,
}

impl Semaphore {
    pub fn new(permits: usize) -> Self {
        Semaphore {
            permits,
            waiters: VecDeque::new(),
        }
    }

    pub fn available(&self) -> usize {
        self.permits
    }

    /// Fast path succeeds only if nobody is queued: that is what makes it fair.
    pub fn try_acquire(&mut self, n: usize) -> bool {
        if self.waiters.is_empty() && self.permits >= n {
            self.permits -= n;
            true
        } else {
            false
        }
    }

    /// Returns `true` if acquired immediately, otherwise `id` is queued at the back.
    pub fn acquire(&mut self, id: u64, n: usize) -> bool {
        if self.try_acquire(n) {
            return true;
        }
        self.waiters.push_back(Waiter { id, needed: n });
        // Hand over whatever is free right now to the front of the queue.
        let free = std::mem::take(&mut self.permits);
        let woken = self.assign(free);
        debug_assert!(woken.is_empty() || woken == [id]);
        !woken.is_empty()
    }

    /// Give permits back; returns the ids that are now fully satisfied, in FIFO order.
    pub fn release(&mut self, n: usize) -> Vec<u64> {
        self.assign(n)
    }

    fn assign(&mut self, mut rem: usize) -> Vec<u64> {
        let mut woken = Vec::new();
        while rem > 0 {
            let Some(front) = self.waiters.front_mut() else { break };
            let give = rem.min(front.needed);
            front.needed -= give;
            rem -= give;
            if front.needed == 0 {
                woken.push(self.waiters.pop_front().unwrap().id);
            }
        }
        self.permits += rem;
        woken
    }
}

/// Reader = 1 permit, writer = all permits. FIFO order means a queued writer
/// blocks later readers, so writers never starve.
pub struct RwLock {
    sem: Semaphore,
}

pub const MAX_READS: usize = 32;

impl Default for RwLock {
    fn default() -> Self {
        Self::new()
    }
}

impl RwLock {
    pub fn new() -> Self {
        RwLock {
            sem: Semaphore::new(MAX_READS),
        }
    }
    pub fn read(&mut self, id: u64) -> bool {
        self.sem.acquire(id, 1)
    }
    pub fn write(&mut self, id: u64) -> bool {
        self.sem.acquire(id, MAX_READS)
    }
    pub fn unlock_read(&mut self) -> Vec<u64> {
        self.sem.release(1)
    }
    pub fn unlock_write(&mut self) -> Vec<u64> {
        self.sem.release(MAX_READS)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn big_request_is_not_starved() {
        let mut s = Semaphore::new(2);
        assert!(s.acquire(1, 2));
        assert!(!s.acquire(2, 5)); // big waiter queues first
        assert!(!s.acquire(3, 1)); // small one must wait behind it
        assert_eq!(s.release(2), vec![]); // partially fills waiter 2 (2 of 5)
        assert_eq!(s.release(3), vec![2]);
        assert_eq!(s.release(5), vec![3]);
        assert_eq!(s.available(), 4);
    }

    #[test]
    fn writer_blocks_later_readers() {
        let mut l = RwLock::new();
        assert!(l.read(1));
        assert!(!l.write(2));
        assert!(!l.read(3), "reader arriving after a waiting writer must wait");
        assert_eq!(l.unlock_read(), vec![2]);
        assert_eq!(l.unlock_write(), vec![3]);
    }
}
