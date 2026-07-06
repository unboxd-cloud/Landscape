# Relationship Graph

The landscape includes a lightweight relationship graph in `data/relations.yml`.

The graph explains how components connect across the stack.

## Relation format

```yaml
- id: source-target-purpose
  source: source-entry-id
  target: target-entry-id
  type: uses
  description: Short explanation of the relationship.
```

## Valid relation types

- `runs`
- `uses`
- `supports`
- `integrates-with`
- `observes`
- `complements`
- `depends-on`
- `replaces`

## Rules

- `source` must reference an existing entry or category ID.
- `target` must reference an existing entry or category ID.
- `id` must be unique inside `data/relations.yml`.
- Descriptions should explain architecture, not marketing.

## Why this matters

The relationship graph turns the landscape from a list into an architecture map. It helps readers understand not only what tools exist, but how they work together.
