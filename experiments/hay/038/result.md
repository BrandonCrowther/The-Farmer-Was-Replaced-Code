# exp-038 — reroll-before-walk-general — result

**Outcome.** rejected — essentially no effect, slightly worse.

**Numbers.** Fresh-conditions baseline (020 unmodified, run immediately
before this variant, same relaunch): **02:52.338**. Variant: **02:52.510**.
PB unchanged at 02:47.682 (that figure remains flagged as run-condition
noise, not attributable to code — record.json). Global rank unchanged,
#130.

**Baseline.** 02:52.338 (this session's clean-condition reference,
matching the documented 02:52.323 mean almost exactly — confirms conditions
were genuinely comparable).

**Delta.** **+0.172s (worse)**. Warning counts shifted (`Didn't have
required items to plant Carrot` 184, `Cannot plant Carrot on Grassland` 48)
but nothing dramatic — consistent with "the change did approximately
nothing," not a regression with an identifiable cause.

**Noise floor.** 0.069s (1 sd, 4 clean runs, from 028). A +0.172s delta is
≈2.5 sd — borderline distinguishable from pure noise, but small, negative,
and from a single run each side; not confidently a real regression, just
not an improvement either.

**Screenshots.** `logs/captures/20260816-225956-exp-hay-038-r1.png`.

**Verdict.** hay_single's reroll-before-walk was a large throughput win
there because the *baseline* hit rate was low (~25-33%, solo drone, no
neighbour cooperation). Hay's drones already hit 44-66% via 021's
"contention is cooperation" effect — there's much less slack for a cheap
reroll to capture, and this run suggests what's left isn't worth the
generalisation's own overhead (more rerolls attempted per pass, each
still costing a plant). **Rejected — journal only, code stays on this
branch.** The lesson that *does* transfer usefully from hay_single tonight
is the Carrot/wood one, not this one — worth checking next whether Hay's
own wood economics have anything analogous to hay_single's short-probe
blind spot (003, corrected by 006/007), rather than re-trying reroll
generalisation with a different limit.
