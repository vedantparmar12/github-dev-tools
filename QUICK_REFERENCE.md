# GitHub Dev Tools - Quick Reference

## Setup (One-time)

```bash
# 1. Set GitHub token
export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"

# 2. Install dependencies
pip install -r scripts/requirements.txt

# 3. Install skill
./install.sh  # or .\install.ps1 on Windows
```

## Common Commands

### Repository Operations

```bash
# Create repository
python scripts/repo_operations.py create my-repo --private

# Create branch
python scripts/repo_operations.py branch owner/repo feature-name main

# Search code
python scripts/repo_operations.py search "query"

# Fork repository
python scripts/repo_operations.py fork owner/repo --org myorg
```

### Pull Requests

```bash
# Create PR
python scripts/create_pr.py owner/repo "feat: Title" source-branch target-branch

# In Python
from scripts.create_pr import create_pull_request, merge_pr

pr = create_pull_request(
    repo="owner/repo",
    title="feat: Add feature",
    head="feature-branch",
    base="main",
    reviewers=["user1", "user2"],
    labels=["enhancement"]
)

merge_pr(repo="owner/repo", pr_number=42, merge_method="squash")
```

### Issues

```bash
# Create issue
python scripts/create_issue.py owner/repo "Bug: Title" "Description"

# In Python
from scripts.create_issue import create_issue, search_issues, close_issue

issue = create_issue(
    repo="owner/repo",
    title="Bug: Login fails",
    labels=["bug", "priority-high"],
    assignees=["developer1"]
)

# Search issues
issues = search_issues("is:open label:bug", repo="owner/repo")

# Close issue
close_issue(repo="owner/repo", issue_number=42, state_reason="completed")
```

## In Codex CLI

### Natural Language (Implicit)

```
Create a PR from feature-auth to main
List all open bugs in owner/repo
Search for "authentication" in Python files
Create an issue for the login bug
```

### Explicit Invocation

```
$github-dev-tools create a pull request from feature-login to main
$github-dev-tools list issues with label:bug
```

## Python API Quick Start

```python
from github import Github
import os

g = Github(os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"])

# Get repo
repo = g.get_repo("owner/repo")

# Create branch
source = repo.get_branch("main")
repo.create_git_ref(ref="refs/heads/new-branch", sha=source.commit.sha)

# Push file
repo.create_file("path/file.py", "message", "content", branch="branch-name")

# Create PR
pr = repo.create_pull(title="Title", body="Body", head="source", base="target")

# Create issue
issue = repo.create_issue(title="Title", body="Body", labels=["bug"])

# Search code
results = g.search_code("query language:python org:myorg")

# List issues
issues = repo.get_issues(state="open", labels=["bug"])
```

## Search Syntax

### Issues/PRs
```
is:issue is:open label:bug author:@me
is:pr is:merged review-requested:@me
updated:<2024-01-01 milestone:"v1.0"
```

### Code
```
"function_name" language:python org:myorg
filename:config extension:json path:src/
```

## Error Codes

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Unauthorized | Check token |
| 403 | Forbidden | Verify scopes |
| 404 | Not Found | Check repo name |
| 422 | Validation Failed | Check parameters |

## File Locations

```
github-dev-tools/
├── SKILL.md              # Main skill instructions
├── README.md             # Full documentation
├── scripts/              # Python utilities
│   ├── create_pr.py
│   ├── create_issue.py
│   └── repo_operations.py
├── assets/               # Templates
│   ├── pr_template.md
│   └── issue_template.md
└── references/           # API docs
    ├── tools-reference.md
    └── search-syntax.md
```

## Quick Workflows

### Feature Development
```python
# 1. Create branch
repo.create_git_ref(ref="refs/heads/feature", sha=main_sha)

# 2. Push changes
repo.create_file("file.py", "msg", "content", branch="feature")

# 3. Create PR
pr = repo.create_pull(title="feat: X", head="feature", base="main")

# 4. Request review
pr.create_review_request(reviewers=["user"])

# 5. Merge
pr.merge(merge_method="squash")
```

### Batch File Push
```python
from scripts.repo_operations import push_multiple_files

push_multiple_files(
    repo_name="owner/repo",
    files=[{"path": "f1.py", "content": "..."}, {"path": "f2.py", "content": "..."}],
    message="Add files",
    branch="main"
)
```

## Links

- [Full Documentation](README.md)
- [PyGithub Docs](https://pygithub.readthedocs.io/)
- [GitHub API](https://docs.github.com/en/rest)
- [Agent Skills Spec](https://agentskills.io/)
