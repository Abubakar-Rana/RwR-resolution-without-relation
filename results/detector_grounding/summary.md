# Tier-2 detector experiment: 1201 items (800 relational, 401 non-relational)

## Accuracy (%)

| Method | All | Relational | Non-relational |
|---|---|---|---|
| Direct | 41.2 | 37.9 | 47.9 |
| Selection (VLM extractor) | 38.6 | 33.4 | 48.9 |
| Proposed (VLM extractor) | 38.0 | 33.4 | 47.1 |
| Selection + detector | 36.7 | 31.5 | 47.1 |
| Proposed + detector | 38.4 | 33.2 | 48.6 |

## Grounding

| Extractor | no-object scenes | mean objects | with relations | with cross-tile |
|---|---|---|---|---|
| VLM extractor (original Proposed) | 52% | 5.7 | 46% | 25% |
| detector (Proposed + detector) | 0% | 24.9 | 100% | 99% |

## Paired comparisons (pp, 95% CI, McNemar p, MDE at 80% power)

**relation block, with detector (Selection+det -> Proposed+det)  [KEY TEST]**
- all: +1.7 [-0.2, +3.6], p=0.0953, wins/losses 75/55, MDE 2.7 (n=1201)
- relational: +1.8 [-0.6, +4.1], p=0.18, wins/losses 54/40, MDE 3.4 (n=800)
- non-relational: +1.5 [-1.5, +4.5], p=0.405, wins/losses 21/15, MDE 4.2 (n=401)

**relation block, original (Selection -> Proposed)**
- all: -0.6 [-2.1, +0.9], p=0.52, wins/losses 40/47, MDE 2.2 (n=1201)
- relational: +0.0 [-2.1, +2.1], p=1, wins/losses 37/37, MDE 3.0 (n=800)
- non-relational: -1.7 [-3.5, +0.0], p=0.0923, wins/losses 3/10, MDE 2.5 (n=401)

**detector objects vs VLM objects, no relations**
- all: -1.8 [-3.7, +0.0], p=0.0672, wins/losses 55/77, MDE 2.7 (n=1201)
- relational: -1.9 [-4.2, +0.4], p=0.142, wins/losses 38/53, MDE 3.3 (n=800)
- non-relational: -1.7 [-5.0, +1.5], p=0.349, wins/losses 17/24, MDE 4.5 (n=401)

**full new method vs original Proposed**
- all: +0.4 [-1.7, +2.5], p=0.753, wins/losses 83/78, MDE 3.0 (n=1201)
- relational: -0.1 [-2.8, +2.6], p=1, wins/losses 60/61, MDE 3.8 (n=800)
- non-relational: +1.5 [-1.5, +4.7], p=0.43, wins/losses 23/17, MDE 4.4 (n=401)

**full new method vs Direct**
- all: -2.8 [-5.1, -0.5], p=0.0206, wins/losses 85/119, MDE 3.3 (n=1201)
- relational: -4.6 [-7.6, -1.8], p=0.00267, wins/losses 54/91, MDE 4.2 (n=800)
- non-relational: +0.7 [-3.0, +4.5], p=0.795, wins/losses 31/28, MDE 5.3 (n=401)

## Key test by stratum (post-treatment; descriptive)

- relation block non-empty / relational: +1.8 [-0.6, +4.1], p=0.18, n=799
- relation block non-empty / non-relational: +1.8 [-1.3, +4.8], p=0.311, n=398
- >=1 cross-tile relation / relational: +1.8 [-0.6, +4.2], p=0.18, n=793
- >=1 cross-tile relation / non-relational: +1.8 [-1.0, +4.8], p=0.311, n=397

## Compute

- sel_det: 1.00 VLM calls/item, 6.3 s/item, 2.1 GPU-h
- prop_det: 1.00 VLM calls/item, 6.4 s/item, 2.1 GPU-h
