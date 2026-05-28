---
name: sourcing-from-github-repo
description: Use when a user wants to source or research candidates from a GitHub repository by auditing contributors, commit history, GitHub profiles, LinkedIn/profile links, personal home pages, institutions, commit emails from the target repo, and surname-based candidate filters. Includes privacy guardrails for contact information and cross-repository email harvesting.
metadata:
  short-description: Source candidates from GitHub repo contributors
---

# Sourcing From GitHub Repo

Use this skill to turn a GitHub repository into a structured contributor sourcing table.
The typical output fields are:

`Github ID | Commit | Institution | LinkedIn | personal home page | commit email`

## Guardrails

- Do not infer whether someone is Chinese, non-Chinese, or any other ethnicity from their name, avatar, language, employer, or location.
- If asked to filter "non-Chinese" or similar, state that you cannot infer protected identity. Offer a mechanical surname-string filter instead.
- Do not harvest personal/non-company emails across unrelated public repositories for outreach lists.
- It is okay to report commit emails that appear in the target repository being analyzed.
- For contact fields, prefer self-published channels on the person's GitHub profile, LinkedIn, or personal homepage.
- Label inferred fields clearly. For example, `Institution` from `@google.com` should be described as `Google (commit email)` rather than current employer.

## Workflow

1. Confirm the input is a specific repository URL, not an organization page.
2. Clone or fetch the target repository.
   - If the repo is already cloned, run `git fetch origin` and use `origin/main` or the default remote branch.
   - Otherwise clone with `--filter=blob:none` when possible.
3. Use Git history as the source of truth for contributor names, commit counts, and commit emails:
   - `git shortlog -sne <rev>`
   - `git log --format='%aN <%aE> %aL' <rev>`
4. Use GitHub contributors API or profile pages to map author identities to GitHub logins when the login differs from the commit email local-part.
5. Search only public profile surfaces for LinkedIn and personal home page:
   - GitHub profile `blog`/links/company fields
   - LinkedIn search results that clearly match the GitHub identity
   - Personal homepage linked from GitHub or a clearly matching search result
6. Apply surname filters mechanically:
   - Match exact tokens in the public author name or verified GitHub profile display name.
   - Include a note that this is a string filter, not an ethnicity classifier.
7. Produce a table ordered by descending commit count unless the user asks for another order.
8. Include sources used: repository URL, git history, GitHub contributors/profile pages, LinkedIn/profile search results.

## Repeatable Extraction

Use `scripts/extract_contributors.py` when you need a deterministic starting table from a local clone:

```bash
python3 scripts/extract_contributors.py /path/to/repo --rev origin/main --surname-filter surnames.txt --format markdown
```

The script reads only the target repository's git history. It does not search other repositories or collect cross-repo personal emails.

## Table Conventions

- `Github ID`: Prefer GitHub contributors API login. If unavailable, use the commit email local-part only when it corresponds to a public GitHub profile or mark it as inferred.
- `Commit`: Use target repo commit count from `git shortlog`.
- `Institution`: Use public profile company if available; otherwise use commit email domain as `Google (commit email)`, `NVIDIA (commit email)`, etc.
- `LinkedIn`: Only include a clearly matching public LinkedIn profile.
- `personal home page`: Include GitHub `blog` field or a clearly matching personal homepage.
- `commit email`: Only include emails present in the target repository's commit history.
