# exp-002 — raise water threshold for wood (multi)'s blocking growth wait

**Hypothesis (before analysis).** `wood`'s seeded driver blocks fully on
growth (`Common.await_harvest()`, no interleaving) and only tops up
water to 0.5, not the 0.999 wood_single/Hay found makes growth
fastest. Since growth speed directly gates wall-clock time here (no
interleaving hides it), raising the threshold looked like a
low-risk, single-parameter lever borrowed from tonight's wood_single
win.

**Reconsidered before touching any code or the live game.** Two facts
from 001's own real-run numbers change the calculus:

1. **588 "not enough water" warnings already occur at the current,
   conservative 0.5 threshold**, out of 24,415 harvests across 32
   drones sharing one `Items.Water` pool. Raising every drone's target
   threshold toward 0.999 would increase each drone's water demand
   substantially, very plausibly *worsening* contention on the shared
   pool rather than the marginal, harmless-noise level 001 measured —
   the opposite of hay/sunflowers (multi)'s finding that the guard
   condition itself (not the threshold) was what mattered.
2. **The design is already about as tick-efficient as wood_single's
   hard-won number, via a completely different mechanism.** 001's own
   real numbers: 2,232,112 total ticks / 24,415 harvests ≈ 91
   ticks/harvest *summed across 32 parallel drones* — converting to a
   per-drone wall-clock-equivalent (×32, since drones run concurrently,
   not sequentially) gives ≈2,912, in the same range as wood_single's
   own carefully-interleaved 2,682 ticks/harvest. This design gets
   there not via per-drone interleaving but via sheer parallelism (32
   drones each scanning forward, never revisiting a tile, so *someone*
   is always finishing a harvest) — meaning growth-wait may already be
   well hidden in aggregate even though no single drone individually
   pipelines it.

**Status: closed, no code change, no live run.** The premise (growth
speed is an unhidden, freely-improvable bottleneck) doesn't survive
contact with 001's own numbers — there's a real, evidenced downside
(worse shared-pool contention) against an upside that's already likely
small (the design isn't leaving obvious throughput on the table the
way wood_single's old design was). Not worth spending a real ~6-minute
scored cycle to find out empirically what the numbers already argue
against; this is exactly the kind of speculative change tonight's own
`docs/LOOP.md` discipline says to skip. A genuine redesign here (full
pre-seed + interleaving à la wood_single) is a much bigger undertaking
— cross-drone Tree-adjacency avoidance in a packed 32-drone grid is a
harder problem than wood_single's single-drone 4-tile layout — and
isn't attempted this session; flagged as a real but large lead for a
future one if `wood` (multi)'s rank ever needs revisiting.
