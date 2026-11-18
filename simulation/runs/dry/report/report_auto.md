# Synthetic pilot – automatic summary

Run: `/home/user/VF/simulation/runs/dry`  
Participants with logs: 3; outcomes: 3; surveys saved: 3

## Tasks by store version

| version | n | success | median steps | median steps (successful) | mean mistakes | mean off-list | mean ease | outcomes |
|---|---|---|---|---|---|---|---|---|
| control | 3 | 1.0 | 14 | 14 | 0 | 0.33 | 3.33 | {'completed': 3} |
| filter | 3 | 1.0 | 7 | 7 | 0 | 0 | 5.0 | {'completed': 3} |
| label | 3 | 1.0 | 15 | 15 | 0 | 0 | 4.0 | {'completed': 3} |

## Stuck / failure points: 4 (see stuck_points.csv)

## Survey items

| item | sub | n | mean | sd | top share | near-zero variance |
|---|---|---|---|---|---|---|
| Q1 |  | 3 |  |  | 1.0 | YES |
| Q10 |  | 3 |  |  | 1.0 | YES |
| Q11 |  | 3 |  |  | 0.67 |  |
| Q12 |  | 3 |  |  | 0.67 |  |
| Q13 |  | 3 | 1989.67 | 20.29 | 0.33 |  |
| Q2 |  | 3 |  |  | 0.33 |  |
| Q3 | Regular store | 3 | 3 | 0.0 | 1.0 | YES |
| Q3 | Store with a vegan filter | 3 | 1 | 0.0 | 1.0 | YES |
| Q3 | Store with vegan labels | 3 | 2 | 0.0 | 1.0 | YES |
| Q4a | alt | 3 | 3.67 | 0.47 | 0.67 | YES |
| Q4a | filter | 3 | 4.67 | 0.47 | 0.67 | YES |
| Q4b | alt | 3 | 3 | 0.0 | 1.0 | YES |
| Q4b | filter | 3 | 4.67 | 0.47 | 0.67 | YES |
| Q4c | alt | 3 | 2.67 | 0.47 | 0.67 | YES |
| Q4c | filter | 3 | 4.67 | 0.47 | 0.67 | YES |
| Q4d | alt | 3 | 3.33 | 0.47 | 0.67 | YES |
| Q4d | filter | 3 | 3.67 | 0.47 | 0.67 | YES |
| Q5 |  | 3 | 35 | 14.72 | 0.33 |  |
| Q6a |  | 3 | 3.67 | 0.47 | 0.67 | YES |
| Q6b |  | 3 | 2.67 | 0.47 | 0.67 | YES |
| Q6c |  | 3 | 1.67 | 0.47 | 0.67 | YES |
| Q7 |  | 3 | 2.33 | 1.25 | 0.33 |  |
| Q9 |  | 3 |  |  | 0.33 |  |

## Contradictions: 0 (see contradictions.csv)


## Possible confusion flags in reasons: 1 (see confusion_flags.csv)

## Analysis pipeline output

- Within-person steps: filter vs control: n=3, mean diff (filter - control)=-8.67, filter lower in 3, higher in 0
- Within-person steps: filter vs alt: n=3, mean diff (filter - alt)=-8.67, filter lower in 3, higher in 0
- Within-person mistakes: filter vs control: n=3, mean diff (filter - control)=0, filter lower in 0, higher in 0
- Within-person mistakes: filter vs alt: n=3, mean diff (filter - alt)=0, filter lower in 0, higher in 0
- Q1 store choice: Store with a vegan filter: 3
- Q5 share of convenience barrier removed: mean 35%, median 40%, range 15-50 (n=3)
- Q6a mean 3.67 (n=3)
- Q6b mean 2.67 (n=3)
- Q6c mean 1.67 (n=3)
- Model 'primary': 2 participants, success 1.0, median steps 11.5
- Model 'secondary': 1 participants, success 1.0, median steps 14
- Model 'primary': Q5 mean 27.5 (n=2)
- Model 'secondary': Q5 mean 50 (n=1)
