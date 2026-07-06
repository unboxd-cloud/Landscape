# Unboxd Cloud Landscape

A living landscape for open, cloud-native, agentic, protocol-first, and sovereign infrastructure primitives used across the Unboxd Cloud and AGenNext ecosystem.

This repository is designed to become a CNCF-style ecosystem map for:

- agent runtimes
- identity and access systems
- policy and governance engines
- data, memory, and storage layers
- observability and FinOps tools
- protocol standards
- commerce and payment rails
- developer experience platforms
- sovereign, edge, and self-hosted infrastructure

## Purpose

The landscape helps builders, partners, students, enterprises, and operators understand which technologies belong in the stack, why they matter, and how they relate to each other.

It is not only a vendor list. It is a decision map.

## Outputs

The repository generates multiple outputs from the YAML registry:

- searchable static website through GitHub Pages
- `landscape.json` machine-readable export
- `graph/landscape-graph.mmd` Mermaid relationship graph
- `graph/landscape-graph.dot` Graphviz relationship graph

## Repository structure

```text
.
├── landscape.yml
├── data/
│   ├── categories.yml
│   ├── projects.yml
│   ├── protocols.yml
│   ├── platforms.yml
│   ├── vendors.yml
│   └── relations.yml
├── docs/
│   ├── index.md
│   ├── architecture.md
│   ├── governance.md
│   ├── relationship-graph.md
│   └── contribution-guide.md
├── schema/
│   └── entry.schema.json
├── scripts/
│   ├── build-site.py
│   ├── validate-registry.py
│   └── export-graph.py
└── .github/workflows/
    ├── validate.yml
    └── pages.yml
```

## Landscape categories

1. Identity & Access
2. Agent Runtime
3. Policy & Governance
4. Data & Memory
5. Observability
6. Protocols
7. Commerce & Payments
8. Developer Experience
9. Edge & Sovereign Cloud
10. Storage & Filesystems

## Principles

- Open standards first
- Cloud-native by default
- Self-hostable where possible
- No unnecessary vendor lock-in
- Policy before execution
- Identity before access
- Provenance before trust
- Governance before scale

## Local development

```bash
pip install -r requirements.txt
python scripts/validate-registry.py
python scripts/build-site.py
python scripts/export-graph.py
```

Generated files are written to `_site/` and `dist/`.

## Current status

This repository now contains the first working version of the landscape registry, static site generator, validation pipeline, relationship graph, and graph export tooling.

Next steps:

1. Expand ecosystem entries.
2. Add visual graph rendering in the website.
3. Add release automation for versioned landscape snapshots.
4. Add scoring fields for maturity, license, deployment model, and governance readiness.

## License

Code and configuration are licensed under Apache-2.0 unless otherwise noted.

Documentation is licensed under CC BY 4.0 unless otherwise noted.
