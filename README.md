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

## Repository structure

```text
.
├── landscape.yml
├── data/
│   ├── categories.yml
│   ├── projects.yml
│   ├── protocols.yml
│   ├── platforms.yml
│   └── vendors.yml
├── docs/
│   ├── index.md
│   ├── architecture.md
│   ├── governance.md
│   └── contribution-guide.md
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

## Current status

This repository is in its initial seeded state. The next steps are:

1. Expand project entries.
2. Add schema validation.
3. Generate a static website from the YAML data.
4. Publish the landscape through GitHub Pages.
5. Add contribution templates and review governance.

## License

Code and configuration are licensed under Apache-2.0 unless otherwise noted.

Documentation is licensed under CC BY 4.0 unless otherwise noted.
