//! xorshift64+ PRNG and Lemire range reduction.
//! Real code: `tokio/src/util/rand.rs` (`FastRand`).

pub struct FastRand {
    one: u32,
    two: u32,
}

impl FastRand {
    pub fn new(seed: u64) -> Self {
        let one = (seed >> 32) as u32;
        let mut two = seed as u32;
        if two == 0 {
            // xorshift state must not be all zeros.
            two = 1;
        }
        FastRand { one, two }
    }

    /// Two 32-bit xorshift sequences added together, shift triplet [17, 7, 16].
    pub fn fastrand(&mut self) -> u32 {
        let mut s1 = self.one;
        let s0 = self.two;
        s1 ^= s1 << 17;
        s1 = s1 ^ s0 ^ s1 >> 7 ^ s0 >> 16;
        self.one = s0;
        self.two = s1;
        s0.wrapping_add(s1)
    }

    /// A number in `0..n` without a division: `(r * n) >> 32`.
    pub fn fastrand_n(&mut self, n: u32) -> u32 {
        let mul = (self.fastrand() as u64).wrapping_mul(n as u64);
        (mul >> 32) as u32
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn deterministic_for_same_seed() {
        let mut a = FastRand::new(42);
        let mut b = FastRand::new(42);
        for _ in 0..100 {
            assert_eq!(a.fastrand(), b.fastrand());
        }
    }

    #[test]
    fn range_is_respected_and_roughly_uniform() {
        let mut r = FastRand::new(7);
        let mut buckets = [0u32; 8];
        for _ in 0..80_000 {
            let v = r.fastrand_n(8);
            assert!(v < 8);
            buckets[v as usize] += 1;
        }
        for count in buckets {
            assert!((9_000..11_000).contains(&count), "{buckets:?}");
        }
    }
}
