# exp-067 — does the champion's exact reroll pattern match 066's cost? — result

**Outcome.** Confirmed exactly. Reroll cost is 207 ticks in the
champion's real usage pattern, not just in 066's ripeness-confirmed
setup.

**Numbers.**

```
FIRST_HARVEST_GAIN 512 entity Entities.Grass can_harvest False
REROLL 0 ticks 200 hay_gain 0 entity_after Entities.Grass can_harvest False
REROLL 1 ticks 200 hay_gain 0 entity_after Entities.Grass can_harvest False
REROLL 2 ticks 200 hay_gain 0 entity_after Entities.Grass can_harvest False
REROLL 3 ticks 200 hay_gain 0 entity_after Entities.Grass can_harvest False
REROLL 4 ticks 200 hay_gain 0 entity_after Entities.Grass can_harvest False
REROLL 5 ticks 200 hay_gain 0 entity_after Entities.Grass can_harvest False
```

Every reroll-pattern `harvest()` (no ripeness check, called on a
just-regrown, definitely-immature tile) costs exactly 200 — never 1 —
and yields 0 Hay every time, exactly as expected from the doc ("an
entity was removed" is what's priced, not ripeness). The tile keeps
auto-regrowing after each one (`entity_after` stays `Entities.Grass`
throughout).

**Verdict.** No correction needed to 066's number. Reroll cost in the
champion's actual reroll loop = `harvest()` (200) + `instructions()` (7,
confirmed separately in 066) ≈ 207, confirmed in the exact call pattern
the real code uses, not just in an idealized ripeness-checked setup.
This closes out the cost-model validation — the corrected numbers in
`record.json`'s 066 note are solid. Next: measure where the *real*
057 champion currently sits, in real ticks/harvest, against the
corrected ~622 floor, before designing any new variant — the past
REROLL_LIMIT sweep (058/059) already ran under these true costs (the
game was never wrong, only my mental model was), so the fix isn't
necessarily "retune the same knob harder."
