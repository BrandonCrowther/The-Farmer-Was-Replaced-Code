# exp-028 — renoise — result

**Outcome.** diagnostic — the floor stands, and conditions matter more than it does

**Four clean champion runs.**

| run | time |
| --- | --- |
| 020 | 02:52.271 |
| 028 r1 | 02:52.275 |
| 028 r2 | 02:52.419 |
| 028 r3 | 02:52.329 |

**mean 02:52.323 · sd 0.069 s · range 0.148 s · cv 0.04%**

The game is extremely repeatable when conditions match, and exp-002's original
0.15 s floor was right all along. The 2.41 s "correction" written an hour earlier
was wrong: it pooled these clean runs with instrumented ones, which is comparing
different code — the exact error it was written to fix. Withdrawn, and the
stamps on 012, 014 and 017 withdrawn with it.

**What is real, and larger than the floor.** Identical champion-equivalent code
scored far off this distribution when run late in a long session:

| run | time | distance from clean mean |
| --- | --- | --- |
| 023 | 02:47.682 | **67 sd faster** |
| 026 | 02:51.263 | **15 sd faster** |

Instrumentation cannot explain it — 026 carries more of it than 023 and is the
slower of the two. What both share is that they ran roughly twenty cycles into
the memory leak that later OOM-killed Steam, while all four clean runs ran on
freshly relaunched games.

**Consequence for method**, regardless of cause: compare only runs made under
similar game conditions, re-baseline after a relaunch, and treat any floor as
valid only for the conditions it was measured under. The 02:47.682 personal best
is real but belongs to conditions, not to a code change.
