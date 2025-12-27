---
name: github-dev-tools
description: >
  Essential GitHub automation for daily developer workflows. Use when Claude needs
  to work with GitHub repositories, issues, pull requests, branches, discussions,
  gists, and notifications. Covers repository management (create repos, branches,
  push/pull files, search code), issue tracking (create/update issues, comments,
  labels), PR workflows (create PRs, request reviews, merge, view diffs), team
  collaboration (discussions, gists, notifications). Triggers on: create a PR,
  list my issues, search code, create branch, merge pull request, create issue,
  add comment, list notifications, create gist.
metadata:
  short-description: GitHub automation for repos, issues, PRs, and collaboration
  version: 1.0.0
  author: Custom Skills Team
  requires:
    - PyGithub>=2.1.1
  environment:
    - GITHUB_PERSONAL_ACCESS_TOKEN
---

# GitHub Dev Tools Skill

Automate GitHub workflows directly from Codex. This skill provides comprehensive GitHub integration for repository management, issue tracking, pull requests, and team collaboration.

## Prerequisites

### Environment Setup

1. **GitHub Personal Access Token Required**

   Set the environment variable:
   ```bash
   export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"
   ```

2. **Required Scopes**
   - `repo` - Full repository access
   - `read:org` - Read organization data
   - `gist` - Create/manage gists
   - `notifications` - Access notifications

3. **Install Dependencies**
   ```bash
   pip install -r scripts/requirements.txt
   ```

## Quick Start Guide

### Workflow 1: Feature Development Cycle

```python
# 1. Create a new feature branch
from github import Github
import os

g = Github(os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"])
repo = g.get_repo("owner/repo")
source = repo.get_branch("main")
repo.create_git_ref(ref="refs/heads/feature-auth", sha=source.commit.sha)

# 2. Push changes
repo.create_file(
    "src/auth.py",
    "Add authentication module",
    "def authenticate(user): pass",
    branch="feature-auth"
)

# 3. Create pull request
pr = repo.create_pull(
    title="feat: Add authentication module",
    body="""## Changes
- Added auth.py module
- Implemented user authentication

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass

Closes #42
""",
    head="feature-auth",
    base="main",
    draft=False
)

# 4. Request reviews
pr.create_review_request(reviewers=["teammate1", "teammate2"])
```

### Workflow 2: Issue Triage & Management

```python
# List open bugs
repo = g.get_repo("owner/repo")
issues = repo.get_issues(state="open", labels=["bug"])

for issue in issues:
    # Add priority labels
    if "critical" in issue.title.lower():
        issue.add_to_labels("priority-high")
        issue.edit(assignees=["oncall-engineer"])
        issue.create_comment("Escalating to on-call engineer")
```

### Workflow 3: Code Search & Discovery

```python
# Search for security vulnerabilities
results = g.search_code(
    query='password in:file language:python org:myorg NOT "password="'
)

for result in results:
    print(f"Potential hardcoded password: {result.repository.full_name}/{result.path}")
```

## Core Workflows

### Repository Operations

#### Creating a Repository
```python
# Use the create_repository helper script
from scripts.repo_operations import create_repository

create_repository(
    name="new-project",
    description="My new project",
    private=True,
    auto_init=True,
    organization="myorg"  # Optional: creates in org
)
```

#### Branch Management
```python
# Create branch from main
repo.create_git_ref(
    ref="refs/heads/feature-branch",
    sha=repo.get_branch("main").commit.sha
)

# List all branches
branches = repo.get_branches()
for branch in branches:
    print(f"{branch.name} - Last commit: {branch.commit.commit.message}")
```

#### File Operations
```python
# Create/update single file
repo.create_file("path/to/file.py", "Add new file", "content", branch="main")

# Update existing file (requires SHA)
contents = repo.get_contents("path/to/file.py", ref="main")
repo.update_file(
    contents.path,
    "Update file",
    "new content",
    contents.sha,
    branch="main"
)

# Push multiple files at once (see scripts/repo_operations.py)
from scripts.repo_operations import push_multiple_files

push_multiple_files(
    repo,
    files=[
        {"path": "src/app.py", "content": "..."},
        {"path": "src/utils.py", "content": "..."}
    ],
    message="Add initial modules",
    branch="main"
)
```

### Issue Management

#### Creating Issues
```python
# Use the create_issue helper script
from scripts.create_issue import create_issue

create_issue(
    repo="owner/repo",
    title="Bug: Login fails with OAuth",
    body="""## Description
Users cannot log in using OAuth providers.

## Steps to Reproduce
1. Click "Login with Google"
2. Authorize app
3. Redirected to error page

## Expected Behavior
Should redirect to dashboard

## Environment
- Browser: Chrome 120
- OS: macOS 14
""",
    labels=["bug", "priority-high"],
    assignees=["developer1"]
)
```

#### Issue Search & Filters
```python
# Find stale issues
issues = repo.get_issues(
    state="open",
    labels=["needs-info"],
    since=datetime(2024, 1, 1)
)

# Advanced search
results = g.search_issues(
    "is:issue is:open label:bug updated:<2024-01-01 repo:owner/repo"
)
```

### Pull Request Workflows

#### Creating PRs
```python
# Use the create_pr helper script
from scripts.create_pr import create_pull_request

pr = create_pull_request(
    repo="owner/repo",
    title="feat: Add user dashboard",
    body_template="default",  # Uses assets/pr_template.md
    head="feature-dashboard",
    base="main",
    draft=False,
    reviewers=["reviewer1", "reviewer2"],
    labels=["enhancement"]
)
```

#### PR Review & Merge
```python
# Approve PR
pr = repo.get_pull(42)
pr.create_review(
    body="LGTM! Great work on the implementation.",
    event="APPROVE"
)

# Request changes
pr.create_review(
    body="Please address the following issues:\n- Add error handling\n- Update tests",
    event="REQUEST_CHANGES"
)

# Merge PR
pr.merge(
    merge_method="squash",  # Options: merge, squash, rebase
    commit_title="feat: add user dashboard (#42)",
    commit_message="Adds dashboard with user stats and activity feed"
)
```

#### Viewing PR Details
```python
# Get PR diff
pr = repo.get_pull(42)
files = pr.get_files()
for file in files:
    print(f"{file.filename}: +{file.additions} -{file.deletions}")
    if file.patch:
        print(file.patch)

# Check CI status
commits = pr.get_commits()
latest_commit = commits.reversed[0]
statuses = latest_commit.get_statuses()
for status in statuses:
    print(f"{status.context}: {status.state}")
```

### Team Collaboration

#### Discussions
```python
# List discussions
discussions = repo.get_discussions()
for disc in discussions:
    print(f"{disc.title} - {disc.comments} comments")

# Create discussion
discussion = repo.create_discussion(
    title="RFC: New API Design",
    body="Proposing changes to our API structure...",
    category_id="DIC_kwDO..."  # Get from list_discussion_categories
)
```

#### Gists
```python
# Create code snippet
gist = g.get_user().create_gist(
    public=False,
    files={
        "example.py": github.InputFileContent("print('Hello')")
    },
    description="Python example"
)
print(f"Gist URL: {gist.html_url}")
```

#### Notifications
```python
# List unread notifications
notifications = g.get_user().get_notifications(all=False)
for notif in notifications:
    print(f"{notif.subject['title']} - {notif.repository.full_name}")

# Mark as read
notif.mark_as_read()
```

## Advanced Patterns

### Automated Issue Triage

```python
# Script to auto-label and assign issues
def triage_new_issues(repo):
    issues = repo.get_issues(state="open", labels=["triage"])

    for issue in issues:
        # Auto-label based on title/body keywords
        if "bug" in issue.title.lower() or "error" in issue.body.lower():
            issue.add_to_labels("bug")
        if "feature" in issue.title.lower() or "enhancement" in issue.body.lower():
            issue.add_to_labels("enhancement")

        # Remove triage label
        issue.remove_from_labels("triage")

        # Auto-assign based on labels
        if "documentation" in [label.name for label in issue.labels]:
            issue.edit(assignees=["docs-team"])
```

### Automated PR Checks

```python
# Check if PR meets requirements
def validate_pr(pr):
    checks = {
        "has_description": len(pr.body) > 50,
        "has_tests": any("test" in f.filename for f in pr.get_files()),
        "small_size": pr.additions + pr.deletions < 500,
        "ci_passing": all(s.state == "success" for s in pr.get_commits().reversed[0].get_statuses())
    }

    if not all(checks.values()):
        pr.create_issue_comment(
            f"PR validation failed:\n" +
            "\n".join(f"- {k}: {'✓' if v else '✗'}" for k, v in checks.items())
        )
        pr.add_to_labels("needs-work")
```

### Batch Operations

```python
# Close stale issues
def close_stale_issues(repo, days=90):
    cutoff = datetime.now() - timedelta(days=days)
    issues = repo.get_issues(state="open", since=cutoff)

    for issue in issues:
        if issue.updated_at < cutoff:
            issue.create_comment(
                f"Closing due to inactivity. Please reopen if still relevant."
            )
            issue.edit(state="closed", state_reason="not_planned")
```

## Error Handling

### Common Errors

| Error Code | Meaning | Solution |
|------------|---------|----------|
| 401 Unauthorized | Invalid or expired token | Regenerate GitHub PAT with correct scopes |
| 403 Forbidden | Insufficient permissions | Check token has required scopes (repo, read:org, etc.) |
| 404 Not Found | Resource doesn't exist | Verify owner/repo/issue_number are correct |
| 422 Validation Failed | Invalid parameters | Check required fields in request body |
| 409 Conflict | Resource conflict | Branch/ref already exists or merge conflict |

### Retry Logic

```python
from time import sleep

def retry_on_rate_limit(func, *args, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except github.RateLimitExceededException as e:
            if attempt < max_retries - 1:
                sleep(60)  # Wait 1 minute
                continue
            raise
```

## Reference Files

- **[tools-reference.md](references/tools-reference.md)** - Complete API reference for all GitHub operations
- **[search-syntax.md](references/search-syntax.md)** - GitHub search query syntax guide

## Templates

- **[PR Template](assets/pr_template.md)** - Standard pull request template
- **[Issue Template](assets/issue_template.md)** - Standard issue template

## Helper Scripts

Located in `scripts/` directory:
- `create_pr.py` - Create pull requests with templates
- `create_issue.py` - Create issues with templates
- `repo_operations.py` - Repository management utilities
- `requirements.txt` - Python dependencies

## Usage Tips

1. **Always verify credentials** before running operations
2. **Use draft PRs** for work-in-progress features
3. **Search before creating** to avoid duplicate issues
4. **Link issues to PRs** using "Fixes #123" or "Closes #123" in PR body
5. **Request reviews explicitly** rather than relying on code owners
6. **Use descriptive commit messages** following conventional commits

## Troubleshooting

### Token Issues
```bash
# Verify token is set
echo $GITHUB_PERSONAL_ACCESS_TOKEN

# Test token validity
python -c "from github import Github; import os; print(Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN']).get_user().login)"
```

### Rate Limiting
Check your rate limit status:
```python
rate_limit = g.get_rate_limit()
print(f"Core: {rate_limit.core.remaining}/{rate_limit.core.limit}")
print(f"Search: {rate_limit.search.remaining}/{rate_limit.search.limit}")
print(f"Reset: {rate_limit.core.reset}")
```
