# exp-087 — same-tree territory partition — result

**Outcome.** **Rejected — analytical closure, backed by live probe
measurements, no real leaderboard cycle spent.** Every same-tree
mechanism found either has no synchronization primitive to build it
on, or costs more than it saves once the *ripple* cost (not just the
mechanism's own overhead) is counted. This closes queue item 087
outright, and with it the whole shared-territory-planting family
(078, 086, 087) — see "what this means for the queue" below, which
also directly answers the user's separate "compact the plot into 2D
blocks" proposal from earlier in the session: it fails for the same
structural reason, independent of geometry.

**Real numbers gathered** (two live probes, `zzRunner.py` → `import
main` trick, reduced/no target, no real scored cycle — matching
077/086's own validation methodology):

| probe | result |
| --- | --- |
| setup-phase scan cost, isolated from spawn-in walk (`walk_start`/`scan_start` split in `driver()`) | 32/32 drones report `visits 30` (exact match to the offline model's 960=32×30); scan-loop cost clusters at 23846/25486/25896/27126 ticks depending on which wrap-seam group a base falls in → **~795-904 ticks per candidate visit**, averaged |
| spawn-tree shape probe (BFS-weighted-tiebreak spanning tree over the sharing graph, root=(18,23), depth 7, max fanout 3, chosen because it captures the same 146/204 redundant tiles as the best shape-blind Kruskal tree at *much* less depth) | max printed `NODE_START` tick (same measurement convention 077 used for its "443" baseline) = **933**, vs 077's measured 443 for today's depth-5/fanout-2 tree — **+490 ticks of pure spawn-latency**, before any planting-order cost is even added |

**The mechanism-level chain** (each candidate checked against real
measurements or already-established facts before being ruled out —
`docs/LOOP.md`'s "measure before designing around it"):

1. **A shared "setup done" flag array, polled non-blockingly.** Dead
   on arrival — `experiments/hay/050` already measured that module-
   level globals are **drone-isolated**, not shared; a write in one
   drone is invisible to any other. No new probe needed, this fact
   already existed.

2. **Restructure the spawn tree to follow physical adjacency**, so
   every tree edge is a free "child trusts parent" relationship
   (parent's own setup runs, in real program order, before the
   `spawn_drone()` call that creates that child — no wait_for() or
   handle-passing needed at all for *that* edge). Offline model
   (`spanning_tree_v2.py`) found a shape capturing 146/204 (72%) of
   086's redundant tiles at depth 7/fanout 3 — better than the naive
   max-weight-but-depth-10 tree found the session before. Live-probed
   (see table above): **+490 ticks of spawn latency alone**, before
   even accounting for the fact that "child trusts parent" requires
   the parent to plant the *entire* candidate window (not just the
   shared subset) before spawning if done naively, which — modeled
   below — is far worse than the 490 by itself. Rejected.

3. **Same idea, applied only to whichever of today's *existing* 31
   tree edges happen, by chance, to already be adjacent bases** — zero
   tree-shape risk, since the tree doesn't change at all. Real find:
   **11 of today's 31 edges are physically-adjacent pairs**, capturing
   **44/204** redundant tiles for free, structurally. But "free" here
   only covers not-needing-a-second-fan-out; it still requires the
   *parent* to plant those specific shared tiles before the
   `spawn_drone()` call that creates the dependent child — and that
   insertion delays **everything spawned after it in that parent's own
   sequential code**, which includes the child's *entire subtree*, not
   just the child itself. Measured this ripple directly against
   today's real tree: the 11 opportunistic edges' child-side subtrees
   are sized [15, 7, 3, 1, 1, 1, 7, 3, 1, 1, 1] (e.g., edge (3,3)→(3,8)
   alone gates 15 of the 32 drones' start times, since that child's
   subtree contains 15 nodes in today's tree). Weighting each edge's
   ~3400-tick shared-subset-planting delay (4 tiles × ~850) by its
   downstream subtree size gives a fleet-wide ripple cost of **~41 ×
   3400 ≈ 139,000 ticks**, against a saving of only **44 × ~850 ≈
   37,000 ticks** — a **net loss of roughly 4x**, not a wash. Rejected,
   and this generalizes: because both the cost (tiles planted early)
   and the saving (tiles skipped later) scale with the *same* tile
   count, while the cost additionally multiplies by however many
   drones sit downstream in the tree, "parent finishes relevant work
   before spawning" is *structurally* unfavorable on this tree shape
   for any edge with more than a trivial subtree — it is at best a
   wash for a leaf edge and a clear loss for anything upstream of one.

4. **A dedicated short-lived "signal" drone per shared edge**, whose
   only job is to plant the shared subset and `return` quickly, so a
   dependent can `has_finished()`-poll it non-blockingly (using the
   handoff's finding #1: handles work correctly when passed to a
   drone that didn't spawn them) instead of delaying anything in the
   spawn sequence. This avoids candidate 3's ripple entirely — the
   signal task runs in parallel, off to the side, not blocking any
   sibling or the parent's own driver(). But: today's tree already
   uses all **32 of 32** `max_drones()` for the whole 2-hour run (one
   per base, confirmed live: `FARM world 32 max_drones 32`, and the
   champion's own spawn tree is sized to exactly 32). `spawn_drone()`
   "returns `None` if all drones are already spawned" (documented).
   Any extra signal drone needs a spare concurrent slot that does not
   exist during the setup rush — the exact window every signal drone
   would need one. The only way around that collision is not to have
   32 base-drones and signal-drones coexist, i.e. a genuinely phased
   design — which is 086's two-phase-spawn shape, already built,
   validated, and rejected for its own (different, walk-back) reason.
   Rejected: the mechanism that would make this design cheap is
   exactly the mechanism the 32-drone cap forbids running concurrently
   with a full 32-base tree.

**What this means for the queue.** All four mechanisms this session
could find for same-tree cross-drone coordination are closed, for two
independent, now numerically-confirmed reasons: (a) the only *free*
ordering primitive (real program order: "I do X before I spawn you")
necessarily delays every drone downstream of the insertion point, and
that ripple cost scales with subtree size while the saving does not,
making it a loss for any edge that isn't a bare leaf; (b) the only
*non-blocking* primitive (a dedicated signal drone polled via
`has_finished()`) needs a spare drone slot that the existing 32-base,
32-cap design has no room for without going fully phased, which is
086's already-rejected shape. This closes 087, and with it the
078/086/087 shared-territory-planting family outright — not "same
size class, inconclusive" as 086/queue's prior note put it, but a
structural dead end backed by measured constants (~850 ticks/visit,
~200-210 ticks/spawn, the 32-drone hard cap, and real subtree-size
data from today's actual tree).

**Directly answers the user's separate "compact the plot into 2D
blocks" proposal** (packing bases into tighter `xxxccxxxccxxxcc`-style
clusters so drones share more boundary, discussed earlier this
session, before this experiment): that proposal is a *geometry*
change meant to increase how much sharing surface exists to capture.
It does not change *how* a dependent would safely learn a shared tile
is ready — it still needs one of the four mechanisms above, all four
of which are now closed regardless of geometry. A 2D block layout
would, if anything, make candidate 3's ripple worse (more edges per
node means more insertion points delaying more downstream drones), not
better. This line of attack is exhausted; a real win here needs a
different shape entirely, not another sharing topology.

**Baseline.** 085: 01:54.587, #52 — unaffected, no code change, no
real leaderboard cycle spent. Game verified restored to 085 and
reloaded (`live/main.py` hash `2e70124694fd5f0f1d7f7dc91a4a7914`,
matches `saves/hay/main.py`) after both probes.

**Verdict.** No merge. `record.json`/`queue.md` updated to close 087
and note the family is exhausted. Journal-only push per
`docs/LOOP.md`'s "lost or inconclusive" path (no `saves/` diff to
carry — this experiment never modified the deployed champion).
