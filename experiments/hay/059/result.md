# exp-059 — REROLL_LIMIT=3 (between the champion's 2 and 057's 5) — result

**Outcome.** rejected — worse than 057's `REROLL_LIMIT=5`, brackets 5
as the local optimum.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 02:44.211, Global Rank #111 (unchanged, PB stays 02:42.421) | modal, `VERDICT=scored` |

**Baseline.** 057: `REROLL_LIMIT=5`, 02:42.421 (champion). 058:
`REROLL_LIMIT=10`, 02:55.859 (rejected).

**Variant.** `REROLL_LIMIT=3`. **Delta.** +1.1% vs 057 — smaller
regression than 058's +8.3%, but still a regression.

**Noise floor.** Single real run each — not independently repeated,
but 3, 5, and 10 now form a clean bracket (worse, best, worse) that's
too consistent in shape to be pure noise.

**Screenshots.** `logs/captures/20260817-093057-exp-hay-059-r1.png`

**Verdict.** `REROLL_LIMIT=5` sits at or very near the true local peak
— both a lower (3) and a much higher (10) value underperform it, and
the shape (small loss at 3, larger loss at 10) is consistent with a
smooth cost curve peaking near 5, not a cliff. Not adopted; champion
stays 057. This parameter is settled — further fine-tuning between
3-5 or 5-10 is unlikely to move the needle much given how flat the
curve looks near the peak. The remaining gap to the cluster
(~750-856 ticks/harvest vs current ~1,250-1,300) needs a different
lever, not further REROLL_LIMIT tuning.
