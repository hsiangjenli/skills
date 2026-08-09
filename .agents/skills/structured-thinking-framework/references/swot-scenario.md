# SWOT and scenario analysis

## Use when

Use SWOT for a compact view of internal capabilities and external conditions. Add scenario analysis when the external environment is uncertain or multiple futures would change the recommendation.

## Method

1. Define the decision, scope, and time horizon.
2. Separate internal factors (strengths and weaknesses) from external factors (opportunities and threats).
3. Label each item as fact, assumption, estimate, interpretation, or unknown.
4. Identify the few factors that materially affect the decision.
5. Build two to four plausible scenarios using distinct external conditions.
6. Convert the analysis into strategic options and trigger signals.

## Framework data

```json
{
  "strengths": [{"text": "Existing distribution", "evidence_type": "fact"}],
  "weaknesses": [{"text": "Limited support capacity", "evidence_type": "estimate"}],
  "opportunities": [{"text": "New segment demand", "evidence_type": "assumption"}],
  "threats": [{"text": "Price competition", "evidence_type": "fact"}],
  "scenarios": [
    {"name": "High demand", "conditions": ["segment grows"], "response": "Scale support before launch"}
  ],
  "strategic_options": ["Pilot with a narrow segment"]
}
```

## Quality checks

- Internal and external factors are not mixed.
- The analysis does not become an unprioritized list.
- Scenarios are plausible, distinct, and time-bounded.
- Options include trade-offs and trigger conditions.
- Weak evidence is labeled and tested with a next action.
