#!/usr/bin/env python3
"""
Create GitHub Issues with templates and automation.

Usage:
    from create_issue import create_issue

    issue = create_issue(
        repo="owner/repo",
        title="Bug: Something is broken",
        body="Description of the issue...",
        labels=["bug", "priority-high"],
        assignees=["developer1"]
    )
"""

from github import Github
import os
from pathlib import Path


def load_template(template_name: str = "default") -> str:
    """Load issue template from assets folder."""
    templates_dir = Path(__file__).parent.parent / "assets"
    template_path = templates_dir / "issue_template.md"

    if template_path.exists():
        return template_path.read_text()
    return ""


def create_issue(
    repo: str,
    title: str,
    body: str = None,
    body_template: str = None,
    labels: list = None,
    assignees: list = None,
    milestone: int = None,
):
    """
    Create a GitHub issue with optional template and automation.

    Args:
        repo: Repository in format "owner/repo"
        title: Issue title
        body: Issue description (overrides body_template)
        body_template: Template name to use (e.g., "default", "bug", "feature")
        labels: List of label names to apply
        assignees: List of user logins to assign
        milestone: Milestone number to add to

    Returns:
        Issue object from PyGithub
    """
    # Initialize GitHub client
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")

    g = Github(token)
    repository = g.get_repo(repo)

    # Prepare issue body
    issue_body = body
    if issue_body is None and body_template:
        issue_body = load_template(body_template)

    # Get milestone object if provided
    milestone_obj = None
    if milestone:
        milestone_obj = repository.get_milestone(milestone)

    # Create issue
    issue = repository.create_issue(
        title=title,
        body=issue_body or "",
        labels=labels or [],
        assignees=assignees or [],
        milestone=milestone_obj,
    )

    print(f"✓ Created issue #{issue.number}: {title}")
    print(f"  URL: {issue.html_url}")

    if labels:
        print(f"✓ Added labels: {', '.join(labels)}")
    if assignees:
        print(f"✓ Assigned to: {', '.join(assignees)}")

    return issue


def update_issue(
    repo: str,
    issue_number: int,
    title: str = None,
    body: str = None,
    state: str = None,
    state_reason: str = None,
    labels: list = None,
    assignees: list = None,
    milestone: int = None,
):
    """
    Update an existing issue.

    Args:
        repo: Repository in format "owner/repo"
        issue_number: Issue number to update
        title: New title
        body: New body
        state: "open" or "closed"
        state_reason: "completed", "not_planned", or "reopened"
        labels: List of labels (replaces existing)
        assignees: List of assignees (replaces existing)
        milestone: Milestone number

    Returns:
        Updated Issue object
    """
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    g = Github(token)
    repository = g.get_repo(repo)
    issue = repository.get_issue(issue_number)

    # Build update kwargs
    update_kwargs = {}
    if title:
        update_kwargs["title"] = title
    if body:
        update_kwargs["body"] = body
    if state:
        update_kwargs["state"] = state
    if state_reason:
        update_kwargs["state_reason"] = state_reason
    if labels is not None:
        update_kwargs["labels"] = labels
    if assignees is not None:
        update_kwargs["assignees"] = assignees
    if milestone:
        update_kwargs["milestone"] = repository.get_milestone(milestone)

    if update_kwargs:
        issue.edit(**update_kwargs)
        print(f"✓ Updated issue #{issue_number}")

    return issue


def add_issue_comment(repo: str, issue_number: int, comment: str):
    """
    Add a comment to an issue.

    Args:
        repo: Repository in format "owner/repo"
        issue_number: Issue number
        comment: Comment text

    Returns:
        IssueComment object
    """
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    g = Github(token)
    repository = g.get_repo(repo)
    issue = repository.get_issue(issue_number)

    issue_comment = issue.create_comment(comment)
    print(f"✓ Added comment to issue #{issue_number}")

    return issue_comment


def close_issue(
    repo: str,
    issue_number: int,
    state_reason: str = "completed",
    comment: str = None,
):
    """
    Close an issue with optional comment.

    Args:
        repo: Repository in format "owner/repo"
        issue_number: Issue number to close
        state_reason: "completed" or "not_planned"
        comment: Optional closing comment

    Returns:
        Closed Issue object
    """
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    g = Github(token)
    repository = g.get_repo(repo)
    issue = repository.get_issue(issue_number)

    # Add comment if provided
    if comment:
        issue.create_comment(comment)

    # Close issue
    issue.edit(state="closed", state_reason=state_reason)
    print(f"✓ Closed issue #{issue_number} ({state_reason})")

    return issue


def search_issues(
    query: str,
    repo: str = None,
    sort: str = "created",
    order: str = "desc",
):
    """
    Search for issues using GitHub search syntax.

    Args:
        query: Search query (e.g., "is:open label:bug")
        repo: Optional repo to limit search to "owner/repo"
        sort: "comments", "created", "updated"
        order: "asc" or "desc"

    Returns:
        List of Issue objects
    """
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    g = Github(token)

    # Add repo filter if provided
    full_query = query
    if repo:
        full_query = f"{query} repo:{repo}"

    # Search issues
    issues = g.search_issues(query=full_query, sort=sort, order=order)

    print(f"Found {issues.totalCount} issues matching: {full_query}")
    return list(issues)


def list_issues(
    repo: str,
    state: str = "open",
    labels: list = None,
    assignee: str = None,
    since: str = None,
):
    """
    List issues with filters.

    Args:
        repo: Repository in format "owner/repo"
        state: "open", "closed", or "all"
        labels: Filter by labels
        assignee: Filter by assignee username
        since: ISO 8601 date string

    Returns:
        List of Issue objects
    """
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    g = Github(token)
    repository = g.get_repo(repo)

    kwargs = {"state": state}
    if labels:
        kwargs["labels"] = labels
    if assignee:
        kwargs["assignee"] = assignee
    if since:
        kwargs["since"] = since

    issues = repository.get_issues(**kwargs)

    issue_list = list(issues)
    print(f"Found {len(issue_list)} issues in {repo} ({state})")

    return issue_list


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 3:
        print("Usage: python create_issue.py <repo> <title> [body]")
        print("Example: python create_issue.py owner/repo 'Bug: Login fails' 'Description...'")
        sys.exit(1)

    repo = sys.argv[1]
    title = sys.argv[2]
    body = sys.argv[3] if len(sys.argv) > 3 else None

    issue = create_issue(
        repo=repo,
        title=title,
        body=body,
        body_template="default" if not body else None,
    )

    print(f"\nIssue created successfully!")
    print(f"View at: {issue.html_url}")
