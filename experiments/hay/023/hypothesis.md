# exp-023 — measure-preplanted

**Not an optimisation.** 021's write-up claimed overlap is cooperation —
neighbours pre-stocking companion tiles — but never measured it. This classifies
every companion arrival, on the champion layout, with `quick_print` from the
origin drone only.

**Categories.** `skip_own_record` (map hit, no walk), `match_neighbour` (arrived,
right plant already there, no record of planting it — the cooperation claim),
`match_stale_own`, `mismatch_own`, `mismatch_new`.
