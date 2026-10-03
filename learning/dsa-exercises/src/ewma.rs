//! Exponentially weighted moving average used to tune how often a worker checks
//! the global queue. Real code: `tokio/src/runtime/scheduler/multi_thread/stats.rs`.

pub const ALPHA: f64 = 0.1;
pub const TARGET_INTERVAL_NS: f64 = 200_000.0;
pub const MAX_TASKS_PER_INTERVAL: u32 = 127;

pub struct Stats {
    pub poll_time_ewma_ns: f64,
}

impl Stats {
    pub fn new(initial_ns: f64) -> Self {
        Stats {
            poll_time_ewma_ns: initial_ns,
        }
    }

    /// `ewma = alpha * sample + (1 - alpha) * ewma`.
    pub fn record(&mut self, sample_ns: f64) {
        self.poll_time_ewma_ns = ALPHA * sample_ns + (1.0 - ALPHA) * self.poll_time_ewma_ns;
    }

    /// How many tasks to poll between global-queue checks.
    pub fn global_queue_interval(&self) -> u32 {
        let n = (TARGET_INTERVAL_NS / self.poll_time_ewma_ns) as u32;
        n.clamp(2, MAX_TASKS_PER_INTERVAL)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn converges_to_new_level() {
        let mut s = Stats::new(1_000.0);
        for _ in 0..100 {
            s.record(10_000.0);
        }
        assert!((s.poll_time_ewma_ns - 10_000.0).abs() < 1.0);
        assert_eq!(s.global_queue_interval(), 20);
    }

    #[test]
    fn interval_is_clamped() {
        assert_eq!(Stats::new(1.0).global_queue_interval(), MAX_TASKS_PER_INTERVAL);
        assert_eq!(Stats::new(1e9).global_queue_interval(), 2);
    }
}
