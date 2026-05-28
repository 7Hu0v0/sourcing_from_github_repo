# Sourcing From GitHub Repo

Codex skill for sourcing contributors from a GitHub repository.

It helps extract a contributor table from repo commit history:

`Github ID | Commit | Institution | LinkedIn | personal home page | commit email`

The workflow uses the target repository's Git history as the source of truth for contributor names, commit counts, and commit emails. It also includes guardrails for avoiding protected-identity inference and cross-repository personal email harvesting.

## Usage

Clone or fetch the target repository, then run:

```bash
python3 scripts/extract_contributors.py /path/to/repo --rev origin/main --format markdown
```

For CSV:

```bash
python3 scripts/extract_contributors.py /path/to/repo --rev origin/main --format csv
```

## Files

- `SKILL.md`: Codex skill instructions.
- `scripts/extract_contributors.py`: Repeatable contributor extraction helper.
- `agents/openai.yaml`: Skill metadata.
