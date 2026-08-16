# exp-033 — probe-the-reroll — result

**Outcome.** diagnostic — 032's claim is false, and a mechanic is corrected

**5,485 reroll attempts.**

| outcome | count | share |
| --- | --- | --- |
| preference **changed** | 3,642 | **66.4%** |
| unchanged | 1,843 | 33.6% |

66.4% is precisely the 2/3 expected from a fresh uniform roll over {Bush, Tree,
Carrot} when the previous value was Carrot. **The reroll works.**

> **CORRECTION 2026-08-16 (036).** Everything below this line in this section was
> wrong. `get_companion()` is **deterministic for a standing plant**: 036
> bracketed 7,958 query pairs around ~800 ticks of work and saw zero changes in
> type or position. The 66.4% above is real, but the replant is what causes it —
> 036 also finds Carrot at 4.1% of preferences where a fresh roll gives 33%, and
> (1/3)³ = 3.7% is exactly what `REROLL_LIMIT = 2` successful replants leave.
>
> The bad step was reading `mid_entity == Entities.Grass` as proof that no
> replant occurred. It does not show that, and I never tested what it does show.
> 035 was then built on the false reading and lost 12.5 s. A cheap 1-tick reroll
> does not exist; a reroll costs a 200-tick plant.

~~**And it works without replanting anything.**~~ `mid_entity` reads
`Entities.Grass` on all 5,485 attempts, so the loop's `harvest()` did not clear
the tile (the plant was unripe) and `instructions()` planted nothing (the entity
was already Grass). Nothing about the tile changed — and the preference changed
anyway.

~~**`get_companion()` is therefore non-deterministic per call**~~, not a fixed
property of the plant standing there. Two earlier statements need adjusting:

- **032's write-up is wrong** where it says the loop "spins to its cap and
  rerolls nothing", and wrong to conclude 020's mechanism was mis-attributed.
  020 stands as written. Corrected in place.
- **010's result** ruled out caching the satisfied companion "because the
  preference rerolls every pass". The conclusion was right; the reason is
  sharper — it rerolls on every *query*, so there is nothing to cache at any
  timescale.

**Why 032 lost anyway.** Rerolling is cheap and effective, but 032 asked for a
much rarer event: a request matching the map on *both* type and position. 020
only asks for "not Carrot", which two thirds of rolls satisfy immediately.
Attempts per pass bear that out — 8,505 passes needed none, 2,705 needed one,
1,390 needed two.

**Method note.** This is the fourth mechanism this session that had to be
measured rather than argued, and the second where my *written-up explanation* was
wrong while the *measured result* was fine. The runs have been trustworthy
throughout; the prose about them has not.
