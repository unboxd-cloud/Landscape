# Landscape Scoring

The landscape includes a scoring rubric in `data/scoring.yml`.

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

## Review principle

Scores should be evidence-based. Avoid scoring based only on brand recognition, hype, or personal preference.

## Future extension

Future versions may add per-entry scores under a dedicated file such as `data/scores.yml`.
