# exp-079 — stray-tick scour

**Hypothesis.** 075/076/077 each found one specific piece of overhead
that never fires or never varies (a no-op guard call, an unwrapped walk,
a sequential spawn chain). The queue's own framing after 077/078 is
that this class of fix — provable safe from reading the code, no new
game mechanic assumed — is what's left, not another macro-structure
change. A direct scour of `driver()` and its bush-wall setup loop should
find more of the same.

**Variable.** Three independent, each provably behavior-preserving by
construction:
1. Reroll chase: `planted[key] == ctype` → `ctype == Entities.Bush`.
   `planted` has exactly one write site in the file (bush-wall setup,
   always `Entities.Bush`), so the dict-value lookup was re-deriving a
   constant at runtime; a direct comparison is cheaper and semantically
   identical.
2. Bush-wall setup: `d1 = wdist(...); d2 = wdist(...); if d1<=3 or
   d2<=3:` → compute `d1` first, only compute `d2` if `d1` already
   misses. `or` already short-circuits in this language (documented,
   same rule Python itself uses) — the truth table is unchanged, only
   the number of `wdist()` calls (~11 ticks each) drops.
3. Bush-wall setup: two `get_entity_type()` calls with nothing state-
   mutating between them → one call, cached in a local.

**Metric.** Two: (a) a single-drone bounded-cycle smoke test (900
cycles, hot loop only, matching 068-075's methodology) for the reroll
fix; (b) the real leaderboard time/rank for the combined effect,
since (2)/(3) are setup-phase-only and invisible to (a) by construction
(same blind spot 076/077's setup fixes had against this smoke-test
shape).

**Baseline.** 077 (`auto_experiment/hay/077`): 01:56.890, #59. Hot-loop
smoke test baseline for comparison: 075's 873.02 ticks/harvest (last
smoke-test measurement before 076/077's setup-only changes, which this
metric can't see).

**Correctness check.** All three changes are provable equivalent by
reading the code (single write site for `planted`'s value; `or`'s
short-circuit is a documented language rule; nothing mutates state
between the two `get_entity_type()` calls) — no new assumption about
game mechanics, unlike 078's rejected territory-partitioning idea.
Still validated live before the real run (target=200,000, `zzRunner.py`
→ `import main`, `MY_POS` per drone): 32/32 unique positions, clean,
no warnings — confirms the wdist short-circuit didn't change which
positions get walked/planted.
