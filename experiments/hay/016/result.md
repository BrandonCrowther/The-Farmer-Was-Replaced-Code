# exp-016 — no-carrot — result

**Outcome.** rejected — and it explains the whole design

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:16.787** | +11.464 s vs champion |

**Baseline.** 03:05.323 · **Variant.** 03:16.787 · **Delta.** **+11.464 s (+6.2%)**

**Noise floor.** 0.15 s. The regression is 76x the floor. All carrot warnings
vanished from `output.txt`, so the change certainly took effect.

**Verdict. The companion walk is not overhead — it is how growth time gets
hidden.**

Skipping a doomed carrot planting should be strictly better: the walk earns no
multiplier either way, so not walking ought to be free. It is not, and the reason
reframes every result so far.

Grass takes time to ripen. While a drone is off planting a companion, its own
grass is growing. 009 measured the busy-wait at 3 ticks *with* the walk in place —
that is not evidence the farm is tick-bound, it is evidence the walk almost
exactly covers the growth. Remove the walk on a third of passes and the drone
arrives home early and waits instead, converting useful work into idling.

So the design sits on a balance point: **walk time ~= growth time.** That is why
008 (removing waiting by adding tiles) failed, why 011 (removing the walk
entirely) failed by 67x, and why this fails too. Anything that shortens the walk
below the growth time buys nothing, because the saving turns straight into
waiting.

**What that implies for the remaining gap.** Going faster needs the *growth* to
be faster, not the walking to be shorter. Growth scales linearly with ground
water, 1x at 0 to 5x at 1 — and water is supply-limited: one 0.25 tank per 10
seconds, while 32 tiles held at 0.75 would drain roughly ten times that. The
farm is water-starved by an order of magnitude, so `while get_water() < 0.75`
can never reach its threshold and spins on failed `use_item` calls, which is
both the ~1000 warnings a run and roughly 200 ticks a pass.

Next: stop chasing an unreachable threshold. Queued as 017.
