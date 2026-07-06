# Landscape Snapshots

Snapshots create stable, dated exports of the landscape registry.

## Local snapshot

```bash
python scripts/snapshot.py
```

This writes a dated JSON file to `snapshots/`.

## Release snapshot

Use the `Release Landscape Snapshot` GitHub Actions workflow and provide a version such as:

```text
v2026.07
```

The workflow validates the registry, builds the site, exports graphs, creates a snapshot, packages release assets, and publishes a GitHub release.

## Release assets

Each release includes:

- `landscape.json`
- `landscape-graph.mmd`
- `landscape-graph.dot`
- dated snapshot JSON
- compressed release bundle

## Why snapshots matter

Snapshots make the landscape auditable over time. They allow teams to refer to a specific architecture map when making platform decisions, writing documentation, or reviewing technology choices.
