# Case: idx26_118e8cc4ea

- Task: **Object Spatial Relationship** (Perception)
- Group: **relational**
- Ground truth: `C`

## Answers by arm

| Arm | Parsed | Correct | VLM calls | Objects | Relations |
|---|---|---|---|---|---|
| b1_direct | `A` | no | 1 | None | None |
| b2_tiling | `C` | yes | 9 | None | None |
| b3_selected | `D` | no | 6 | 9 | 0 |
| proposed_ctsr | `C` | yes | 6 | 9 | 32 |

## Objects (global coordinates)

| id | label | bbox | tiles |
|---|---|---|---|
| 0 | largest gray H-shaped building | [1892.0, 3192.0, 2562.0, 3900.0] | [17, 22] |
| 1 | largest gray H-shaped building | [1094.0, 2012.0, 1636.0, 2488.0] | [11] |
| 2 | largest gray H-shaped building | [398.0, 2926.0, 672.0, 3142.0] | [15] |
| 3 | largest gray H-shaped building | [3433.0, 3104.0, 3633.0, 3228.0] | [19] |
| 4 | white circular building | [1221.0, 2292.0, 1404.0, 2402.0] | [11] |
| 5 | white circular building | [3640.0, 3370.0, 3738.0, 3438.0] | [19] |
| 6 | white circular building | [2550.0, 2886.0, 2634.0, 2945.0] | [17] |
| 7 | white circular building | [665.0, 2803.0, 738.0, 2858.0] | [15] |
| 8 | white circular building | [2493.0, 3772.0, 2534.0, 3797.0] | [22] |

## Relations

| subject | predicate | object | value | cross-tile |
|---|---|---|---|---|
| #0 | contains | #8 |  | no |
| #1 | contains | #4 |  | no |
| #2 | adjacent | #7 | north-east | no |
| #3 | near | #5 | south-east | no |
| #4 | direction | #7 | south-west | yes |
| #6 | direction | #8 | south | yes |
| #1 | direction | #7 | south-west | yes |
| #3 | direction | #6 | west | yes |
| #2 | direction | #4 | north-east | yes |
| #1 | direction | #2 | south-west | yes |
| #3 | direction | #8 | south-west | yes |
| #5 | direction | #6 | north-west | yes |
| #5 | direction | #8 | west | yes |
| #0 | direction | #3 | east | yes |
| #1 | direction | #6 | south-east | yes |
| #4 | direction | #6 | south-east | yes |
| #0 | direction | #5 | east | yes |
| #0 | direction | #4 | north-west | yes |
| #0 | direction | #1 | north-west | yes |
| #0 | direction | #7 | north-west | yes |
| #0 | direction | #2 | west | yes |
| #4 | direction | #8 | south-east | yes |
| #6 | direction | #7 | west | yes |
| #1 | direction | #8 | south-east | yes |
| #7 | direction | #8 | south-east | yes |
| #2 | direction | #6 | east | yes |
| #2 | direction | #8 | east | yes |
| #1 | direction | #3 | south-east | yes |
| #3 | direction | #4 | west | yes |
| #1 | direction | #5 | south-east | yes |
| #4 | direction | #5 | south-east | yes |
| #0 | direction | #6 | north-east | no |

## Raw response: b3_selected

```
ANSWER: D
```

## Raw response: proposed_ctsr

```
ANSWER: C
```