# Prioritization analysis

## Use when

Use prioritization when there are more candidate initiatives than available time, budget, people, or attention. Choose a method that matches the available evidence rather than manufacturing precise scores.

## Method

1. Define the objective and decision horizon.
2. List comparable items with the same unit of analysis.
3. Choose a small set of criteria, such as impact, effort, confidence, reach, urgency, or risk reduction.
4. Define score meanings before scoring.
5. Apply weights only when criteria have different importance.
6. Show the ranking and explain uncertainty or ties.
7. Run a sensitivity check for assumptions that could change the order.

## Framework data

```json
{
  "method": "impact-effort",
  "criteria": ["impact", "effort"],
  "weights": {"impact": 0.6, "effort": 0.4},
  "items": [
    {"name": "Self-service onboarding", "scores": {"impact": 5, "effort": 2}, "confidence": "medium"}
  ],
  "ranking": ["Self-service onboarding"],
  "sensitivity": "Ranking changes if effort is weighted above 60%."
}
```

## Quality checks

- Items are comparable and have the same scoring scale.
- Criteria are not double-counting the same factor.
- Scores have a stated basis and confidence.
- The ranking is not presented as objective truth.
- Sensitivity and unresolved evidence are visible.
