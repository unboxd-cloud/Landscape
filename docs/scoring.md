# Landscape Scoring

The landscape includes a scoring rubric in `data/scoring.yml` and per-entry scores in `data/scores.yml`.

The scoring model is intended to support architectural decisions, not popularity rankings.

## Dimensions

- Openness
- Maturity
- Self-hostability
- Governance readiness
- Cloud-native fit

## Scale

Scores use a 0 to 5 scale.

| Score | Meaning |
| --- | --- |
| 0 | Not applicable or unknown |
| 1 | Weak fit |
| 2 | Partial fit |
| 3 | Usable fit |
| 4 | Strong fit |
| 5 | Excellent fit |

## Per-entry score format

```yaml
- entry: kubernetes
  openness: 5
  maturity: 5
  self-hostability: 5
  governance-readiness: 5
  cloud-native-fit: 5
  notes: Mature cloud-native control plane and strong ecosystem fit.
```

## Validation

CI validates that:

- every score references an existing entry
- every score value is an integer from 0 to 5
- each entry appears at most once in `data/scores.yml`

## Review principle

Scores should be evidence-based. Avoid scoring based only on brand recognition, hype, or personal preference.
