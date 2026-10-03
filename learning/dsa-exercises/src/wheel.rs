//! Hierarchical timing wheel: 6 levels x 64 slots, 1 tick = 1 ms.
//! Real code: `tokio/src/runtime/time/wheel/{mod,level}.rs`.
//!
//! Tokio stores timers in intrusive linked lists; here each slot is a `Vec<(id, deadline)>`.

pub const NUM_LEVELS: usize = 6;
pub const BITS_PER_LEVEL: usize = 6;
pub const LEVEL_MULT: usize = 1 << BITS_PER_LEVEL;
pub const MAX_DURATION: u64 = 1 << (BITS_PER_LEVEL * NUM_LEVELS);

/// Which level a timer belongs to: the highest bit where `now` and `when` differ.
pub fn level_for(elapsed: u64, when: u64) -> usize {
    const SLOT_MASK: u64 = (1 << BITS_PER_LEVEL) - 1;
    let masked = elapsed ^ when | SLOT_MASK;
    if masked >= MAX_DURATION {
        return NUM_LEVELS - 1;
    }
    masked.ilog2() as usize / BITS_PER_LEVEL
}

/// Width of one slot on `level`, in ticks: 64^level.
pub fn slot_range(level: usize) -> u64 {
    (LEVEL_MULT as u64).pow(level as u32)
}

/// Width of a whole level, in ticks: 64^(level + 1).
pub fn level_range(level: usize) -> u64 {
    LEVEL_MULT as u64 * slot_range(level)
}

pub fn slot_for(when: u64, level: usize) -> usize {
    ((when >> (level * BITS_PER_LEVEL)) % LEVEL_MULT as u64) as usize
}

struct Level {
    level: usize,
    /// Bit `i` set <=> `slots[i]` is non-empty.
    occupied: u64,
    slots: Vec<Vec<(u64, u64)>>,
}

impl Level {
    fn new(level: usize) -> Self {
        Level {
            level,
            occupied: 0,
            slots: (0..LEVEL_MULT).map(|_| Vec::new()).collect(),
        }
    }

    /// Circular "find next set bit after now" in O(1).
    fn next_occupied_slot(&self, now: u64) -> Option<usize> {
        if self.occupied == 0 {
            return None;
        }
        let now_slot = ((now / slot_range(self.level)) % LEVEL_MULT as u64) as usize + 1;
        let occupied = self.occupied.rotate_right(now_slot as u32);
        let zeros = occupied.trailing_zeros() as usize;
        Some((zeros + now_slot) % LEVEL_MULT)
    }

    /// When the next occupied slot on this level starts, in absolute ticks.
    fn next_expiration(&self, now: u64) -> Option<(usize, u64)> {
        let slot = self.next_occupied_slot(now)?;
        let level_start = now & !(level_range(self.level) - 1);
        let mut deadline = level_start + slot as u64 * slot_range(self.level);
        if deadline <= now {
            // The slot is in the next rotation of this level.
            deadline += level_range(self.level);
        }
        Some((slot, deadline))
    }
}

pub struct Wheel {
    elapsed: u64,
    levels: Vec<Level>,
}

impl Default for Wheel {
    fn default() -> Self {
        Self::new()
    }
}

impl Wheel {
    pub fn new() -> Self {
        Wheel {
            elapsed: 0,
            levels: (0..NUM_LEVELS).map(Level::new).collect(),
        }
    }

    pub fn elapsed(&self) -> u64 {
        self.elapsed
    }

    /// O(1) insert. Returns `false` if the deadline already passed.
    pub fn insert(&mut self, id: u64, when: u64) -> bool {
        if when <= self.elapsed {
            return false;
        }
        let level = level_for(self.elapsed, when);
        let slot = slot_for(when, level);
        let lvl = &mut self.levels[level];
        lvl.slots[slot].push((id, when));
        lvl.occupied |= 1 << slot;
        true
    }

    /// Advance time to `now`, returning ids of expired timers in deadline order.
    pub fn poll(&mut self, now: u64) -> Vec<u64> {
        let mut fired = Vec::new();
        loop {
            // The earliest non-empty slot across levels (lower levels win ties).
            let next = self
                .levels
                .iter()
                .filter_map(|l| l.next_expiration(self.elapsed).map(|(s, d)| (d, l.level, s)))
                .min();
            let Some((deadline, level, slot)) = next else { break };
            if deadline > now {
                break;
            }
            self.elapsed = deadline;
            let lvl = &mut self.levels[level];
            lvl.occupied &= !(1 << slot);
            let mut entries = std::mem::take(&mut lvl.slots[slot]);
            entries.sort_by_key(|&(_, when)| when);
            for (id, when) in entries {
                if when <= self.elapsed {
                    fired.push(id);
                } else {
                    // Cascade: re-insert at a finer level, now that we're closer.
                    self.insert(id, when);
                }
            }
        }
        self.elapsed = self.elapsed.max(now);
        fired
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn levels_by_distance() {
        assert_eq!(level_for(0, 1), 0);
        assert_eq!(level_for(0, 63), 0);
        assert_eq!(level_for(0, 64), 1);
        assert_eq!(level_for(0, 4095), 1);
        assert_eq!(level_for(0, 4096), 2);
        assert_eq!(level_for(0, u64::MAX), NUM_LEVELS - 1);
    }

    #[test]
    fn next_slot_wraps_around() {
        let mut l = Level::new(0);
        l.occupied = 1 << 3;
        assert_eq!(l.next_occupied_slot(10), Some(3));
        l.occupied |= 1 << 20;
        assert_eq!(l.next_occupied_slot(10), Some(20));
    }

    #[test]
    fn fires_in_order_across_levels() {
        let mut w = Wheel::new();
        w.insert(1, 5);
        w.insert(2, 100);
        w.insert(3, 5_000);
        w.insert(4, 70);
        assert!(w.poll(4).is_empty());
        assert_eq!(w.poll(80), vec![1, 4]);
        assert_eq!(w.poll(4_999), vec![2]);
        assert_eq!(w.poll(5_000), vec![3]);
    }

    #[test]
    fn many_random_timers_fire_exactly_at_deadline() {
        let mut rng = crate::rand::FastRand::new(1);
        let mut w = Wheel::new();
        let mut expected: Vec<(u64, u64)> = (0..2_000)
            .map(|id| (1 + rng.fastrand_n(300_000) as u64, id))
            .collect();
        for &(when, id) in &expected {
            w.insert(id, when);
        }
        expected.sort();
        let mut got = Vec::new();
        for now in (0..=300_000).step_by(997) {
            for id in w.poll(now) {
                let when = expected.iter().find(|e| e.1 == id).unwrap().0;
                assert!(when <= now && now - when < 997, "id {id} when {when} now {now}");
                got.push(id);
            }
        }
        got.extend(w.poll(300_001));
        assert_eq!(got.len(), expected.len());
    }
}
