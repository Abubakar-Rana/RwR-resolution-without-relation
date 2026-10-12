# A5. Tier-2: the relation block once grounding works

Same 1201 items in both regimes (800 relational, 401 non-relational).

## Accuracy (%)

| Method | All | Relational | Non-relational |
|---|---|---|---|
| Direct | 41.2 | 37.9 | 47.9 |
| Selection (VLM objects) | 38.6 | 33.4 | 48.9 |
| Proposed (VLM objects) | 38.0 | 33.4 | 47.1 |
| Selection (detector) | 36.7 | 31.5 | 47.1 |
| Proposed (detector) | 38.4 | 33.2 | 48.6 |

## Effect of adding the relation block

| Grounding | Group | Delta (pp) [95% CI] | p | wins/losses |
|---|---|---|---|---|
| VLM objects | all | -0.6 [-2.1, +0.9] | 0.52 | 40/47 |
| detector objects | all | +1.7 [-0.2, +3.5] | 0.095 | 75/55 |
| VLM objects | relational | +0.0 [-2.1, +2.1] | 1 | 37/37 |
| detector objects | relational | +1.8 [-0.6, +4.1] | 0.18 | 54/40 |
| VLM objects | non-relational | -1.7 [-3.5, +0.0] | 0.092 | 3/10 |
| detector objects | non-relational | +1.5 [-1.5, +4.5] | 0.41 | 21/15 |

## Did better grounding improve the relation effect? (paired, same items)

| Group | Improvement (pp) [95% CI] | permutation p |
|---|---|---|
| all | +2.2 [+0.0, +4.6] | 0.0698 |
| relational | +1.8 [-1.2, +4.9] | 0.291 |
| non-relational | +3.2 [+0.0, +6.5] | 0.066 |

## Detector vocabulary

- objects matching a question keyword: 10.5% of the objects in a scene, on average
- most frequent labels: tree (15350), vehicle (4400), house (2994), building house (1086), building (1035), farmland (682), road (667), cars vehicle (274)
