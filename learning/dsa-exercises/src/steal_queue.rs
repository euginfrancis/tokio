//! Bounded ring-buffer run queue with "steal half" and "overflow half".
//! Real code: `tokio/src/runtime/scheduler/multi_thread/queue.rs`.
//!
//! Tokio's version is lock-free (atomic `head`/`tail`, two heads packed in one u64)
//! so other threads can steal concurrently. This one is single-threaded so the
//! index arithmetic is easy to see.

pub const CAPACITY: usize = 256;
const MASK: usize = CAPACITY - 1;

pub struct LocalQueue<T> {
    buffer: Vec<Option<T>>,
    /// Indices grow forever and wrap; `index & MASK` is the slot. Using wider
    /// indices than needed is what lets Tokio tell "full" from "empty".
    head: u32,
    tail: u32,
}

impl<T> Default for LocalQueue<T> {
    fn default() -> Self {
        Self::new()
    }
}

impl<T> LocalQueue<T> {
    pub fn new() -> Self {
        LocalQueue {
            buffer: (0..CAPACITY).map(|_| None).collect(),
            head: 0,
            tail: 0,
        }
    }

    pub fn len(&self) -> usize {
        self.tail.wrapping_sub(self.head) as usize
    }

    pub fn is_empty(&self) -> bool {
        self.len() == 0
    }

    /// Push; when full, move half the queue plus `task` to `global` in one batch.
    pub fn push_back_or_overflow(&mut self, task: T, global: &mut Vec<T>) {
        if self.len() < CAPACITY {
            let idx = self.tail as usize & MASK;
            self.buffer[idx] = Some(task);
            self.tail = self.tail.wrapping_add(1);
            return;
        }
        let take = CAPACITY / 2;
        for _ in 0..take {
            global.push(self.pop().expect("queue is full"));
        }
        global.push(task);
    }

    pub fn pop(&mut self) -> Option<T> {
        if self.is_empty() {
            return None;
        }
        let idx = self.head as usize & MASK;
        self.head = self.head.wrapping_add(1);
        self.buffer[idx].take()
    }

    /// Steal ceil(n/2) tasks from `self` into `dst`; returns one of them to run now.
    pub fn steal_into(&mut self, dst: &mut LocalQueue<T>) -> Option<T> {
        let n = self.len();
        let n = n - n / 2;
        if n == 0 || dst.len() + n > CAPACITY {
            return None;
        }
        for _ in 0..n {
            let t = self.pop().expect("counted");
            dst.push_back_or_overflow(t, &mut Vec::new());
        }
        // Like Tokio: the thief runs the last stolen task immediately.
        dst.pop_back()
    }

    fn pop_back(&mut self) -> Option<T> {
        if self.is_empty() {
            return None;
        }
        self.tail = self.tail.wrapping_sub(1);
        self.buffer[self.tail as usize & MASK].take()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fifo_order() {
        let mut q = LocalQueue::new();
        let mut g = Vec::new();
        for i in 0..10 {
            q.push_back_or_overflow(i, &mut g);
        }
        assert_eq!((0..10).map(|_| q.pop().unwrap()).collect::<Vec<_>>(), (0..10).collect::<Vec<_>>());
        assert!(q.pop().is_none());
    }

    #[test]
    fn overflow_moves_half_plus_one() {
        let mut q = LocalQueue::new();
        let mut g = Vec::new();
        for i in 0..CAPACITY + 1 {
            q.push_back_or_overflow(i, &mut g);
        }
        assert_eq!(g.len(), CAPACITY / 2 + 1);
        assert_eq!(q.len(), CAPACITY / 2);
        assert_eq!(g[0], 0);
        assert_eq!(*g.last().unwrap(), CAPACITY);
    }

    #[test]
    fn steal_takes_half_rounded_up() {
        let mut victim = LocalQueue::new();
        let mut thief = LocalQueue::new();
        let mut g = Vec::new();
        for i in 0..7 {
            victim.push_back_or_overflow(i, &mut g);
        }
        let mut empty: LocalQueue<i32> = LocalQueue::new();
        assert_eq!(empty.steal_into(&mut LocalQueue::new()), None);

        // 7 tasks: the thief takes 7 - 7/2 = 4 and runs the last one (3) right away.
        let got = victim.steal_into(&mut thief);
        assert_eq!(got, Some(3));
        assert_eq!(thief.len(), 3);
        assert_eq!(victim.len(), 3);
    }

    #[test]
    fn indices_wrap() {
        let mut q = LocalQueue::new();
        q.head = u32::MAX - 2;
        q.tail = u32::MAX - 2;
        let mut g = Vec::new();
        for i in 0..6 {
            q.push_back_or_overflow(i, &mut g);
        }
        assert_eq!(q.len(), 6);
        assert_eq!((0..6).map(|_| q.pop().unwrap()).collect::<Vec<_>>(), vec![0, 1, 2, 3, 4, 5]);
    }
}
