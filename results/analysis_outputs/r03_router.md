# A3. Offline router between global view and zooming

2983 scored items, 5-fold stratified cross-validation repeated 20 times. Routing uses only the benchmark's task label and the question keywords. McNemar p on repeat 0.

| Method | Accuracy (%) | Relational | Non-rel. | VLM calls | s/item | vs Selection (pp) | p |
|---|---|---|---|---|---|---|---|
| Direct | 41.3 | 37.9 | 42.6 | 1.00 | 3.0 | | |
| Selection | 43.1 | 33.4 | 46.7 | 6.10 | 15.4 | | |
| Proposed | 42.7 | 33.4 | 46.2 | 6.10 | 15.5 | | |
| group router (pre-registered split) | 44.3 ± 0.0 | 37.9 | 46.7 | 4.76 | 11.3 | +1.2 [+0.4, +2.0] | 0.0039 |
| task router (Direct / Selection) | 44.2 ± 0.1 | 37.4 | 46.4 | 4.82 | 11.2 | +0.9 [+0.1, +1.7] | 0.03 |
| task router (Direct / Selection / Proposed) | 44.1 ± 0.1 | 37.4 | 46.7 | 4.85 | 11.3 | +1.1 [+0.2, +1.9] | 0.012 |
| keyword + task router (logistic) | 43.6 ± 0.2 | 36.5 | 46.0 | 4.26 | 9.7 | +0.4 [-0.5, +1.3] | 0.46 |
| keyword-only router (no task label) | 43.6 ± 0.2 | 36.5 | 46.1 | 4.26 | 9.6 | +0.4 [-0.5, +1.3] | 0.41 |

Oracle (best of Direct / Selection per item): 51.2%; best of all three: 52.6%.

- group router (pre-registered split): routes Direct 27%, Selection 73%
- task router (Direct / Selection): routes Direct 26%, Selection 74%
- task router (Direct / Selection / Proposed): routes Direct 25%, Selection 45%, Proposed 30%
- keyword + task router (logistic): routes Direct 37%, Selection 63%
- keyword-only router (no task label): routes Direct 37%, Selection 63%
