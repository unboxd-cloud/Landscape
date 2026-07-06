# Contribution Guide

Thank you for helping improve the Unboxd Cloud Landscape.

## How to contribute

1. Choose the correct data file in `data/`.
2. Add or update an entry.
3. Keep the entry concise and architectural.
4. Run YAML validation locally where possible.
5. Open a pull request with a short explanation.

## Entry style

Use this format for project entries:

```yaml
- id: example-project
  name: Example Project
  category: agent-runtime
  type: workflow-runtime
  maturity: active
  role: Short explanation of the architectural role.
  homepage: https://example.com/
```

## Category IDs

Use the IDs from `data/categories.yml`.

## Avoid

- marketing-only descriptions
- duplicate entries
- unverifiable claims
- entries without a clear role
- proprietary-only components without an open interoperability path
