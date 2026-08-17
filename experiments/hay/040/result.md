# exp-040 — draw-pattern-check — result

**Outcome.** rejected (the hypothesis that the multi-drone draw isn't
IID) — a clean, decisive negative result, even more rigorous than 013's.

**Numbers.** 12,600 draws (300/repeat × 42 internal repeats, all pooled).

| check | measured | IID-uniform expectation |
| --- | --- | --- |
| type frequency | Bush 33.98%, Tree 33.22%, Carrot 32.80% | 33.33% each |
| distinct positions | 24 | 24 (matches 004's radius-3 wrapped-ball count — same on Hay's larger world, since ball size depends only on radius, not world size) |
| position count spread | 470-559 (n≈24, mean 525) | consistent with uniform + sampling noise |
| P(same type as previous draw) | 0.3316 | 0.3333 |
| P(same exact pair as previous) | 0.0143 | 0.0139 (1/3 × 1/24) |

Every check matches IID-uniform closely, tighter than 013's smaller sample.
**The draw is genuinely random here too — 31 active neighbours don't
change it.** This is measured live during a real, fully-populated 32-drone
run, not an isolated probe, so it directly rules out "the multi-drone
context perturbs the RNG."

**Baseline.** 013 (hay_single, solo, n=300): equally clean IID confirmation.

**Noise floor.** N/A — this is a distributional check, not a comparison.
n=12,600 gives strong power; nothing this size and this clean is
consistent with meaningful hidden structure.

**Screenshots.** `logs/captures/20260816-233632-exp-hay-040-r1.png` — run
scored normally (02:52.665, PB/rank unchanged), confirming the sampling
code didn't disturb the champion's behaviour.

**Verdict.** The companion draw is IID-uniform whether solo (hay_single) or
inside a 32-drone swarm (Hay) — confirmed directly, not assumed. **039's
~441-tick estimate for the leader is not explained by "they beat the
draw."** That leaves two possibilities: (a) 039's ratio-based estimate
carries a wrong assumption — most likely the same-drone-count /
same-per-drone-harvest-share assumption, which was never independently
verified for the leader's actual design, or (b) the leader's edge comes
from somewhere structurally different from anything tested tonight (a
different layout, a different yield mechanism, or something not yet
considered). Given the draw itself is now ruled out cleanly in both
contexts, further investigation should stop chasing the companion-RNG
angle and instead re-examine whether 039's harvest-count assumption is
sound, or look for a completely different mechanism.
