# exp-030 — instrument-two-plots — result

**Outcome.** diagnostic — the missing ticks found, and the multi-plot line closed

| visit outcome | count | share | avg work |
| --- | --- | --- | --- |
| ripe — harvested | 10,517 | 71% | 879 |
| **unripe — wasted trip** | **4,283** | **29%** | 5 |

**29% of visits arrive at an unripe plot**, pay a 200-tick move, check
`can_harvest()` for 5 ticks, and leave.

The 029 model missed this because `t0` was taken *after* the move, so movement
never entered `work` at all. Accounting for it:

```
per harvest = 879 work + (14,800 visits x 200 ticks) / 10,517 harvests
            = 879 + 281 = 1,160 ticks
```

against the champion's 967 — **+20%, matching the +16% measured.** The books
balance, with no third invented mechanism required.

**Why, and why the line is closed.** A two-plot cycle revisits each plot every
~2,320 ticks. Grass needs ~2,819 ticks to ripen at water 0 (019). The plot is
simply not ready when the drone returns, 29% of the time.

More plots give each one longer to grow but add more visits that can be wasted —
027 at four plots lost twice what 029 lost at two, which is the same effect at a
larger dose.

**The general result: waiting in place beats walking to check.** The champion
idles 437 ticks on a skip pass and spends nothing on movement. A drone that walks
elsewhere to stay busy pays 200 ticks a hop to learn one bit — whether that plot
is ready. Idle time is not automatically waste; it is waste only if something
cheaper than 200 ticks a step could fill it, and while growth is the binding
constraint nothing can.

**What this leaves.** Every remaining idea has to make grass ripen faster, or
make the multiplied harvest itself cheaper. Keeping the drone busy is not a
strategy here.
