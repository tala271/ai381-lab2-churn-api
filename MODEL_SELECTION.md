# Model selection

## The question
The model predicts whether a telecom customer will churn (leave). A missed churner means a lost customer who never got a retention offer. A false alarm means we spend a discount on someone who would have stayed.

## Candidates
| Candidate | Why I tried it | AUC | F1 | F1 per slice (lowest) | p95 latency (ms) | Size (KB) | MLflow run ID |
|---|---|---|---|---|---|---|---|
| logreg | Simple linear baseline. C=0.5 and class_weight=balanced so the smaller churn class is not ignored. | 0.797 | 0.585 | 0.316 (two-year) | 5.7 | 3.5 | deae11e8f9aa42c68f74674dea212557 |
| random_forest | Non-linear model that can catch interactions. 300 trees, max_depth=6 to limit overfitting. | 0.772 | 0.573 | 0.400 (two-year) | 24.3 | 2353 | d12486ea1ec14ac1a90cf07a0f5d749f |
| gradient_boosting | Boosted trees. Slow learning rate (0.05) and shallow trees (depth 3) for stability. | 0.759 | 0.396 | 0.250 (one-year) | 6.1 | 206 | ece9fb9bbb6f4d4e882dbbe9da9867ab |

## The champion
I picked logreg. It has the best overall F1 (0.585), the best AUC (0.797), the best F1 on month-to-month customers (0.626), the lowest latency (5.7 ms) and is tiny (3.5 KB).
gradient_boosting was clearly worse (F1 0.396), so I dropped it.
random_forest is better on the two-year slice (0.400 vs 0.316), but it is 4x slower and about 600x larger, and its overall F1 is lower.
What I accepted losing: logreg is weak on two-year contracts (F1 0.316). I accept this because those customers churn rarely and the test set for that slice is small.

## My promotion rules
- Latency budget (p95): 15 ms, because logreg takes 5.7 ms on my laptop and CI runners are slower, so I leave a safety margin of about 2.5x. random_forest (24.3 ms) would be blocked.
- Minimum gain to replace the champion (F1 points): 0.01, because small differences in F1 are noise on a small test set, and a new model should be clearly better to justify a deployment.

## What I would check next
The two-year slice has very few customers, so its F1 changes a lot with small changes in the data. In production I would check that slice again with more data, and watch for data drift, because the model was trained on one data file (hash 76a6447e764b).
