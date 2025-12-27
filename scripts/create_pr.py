#!/usr/bin/env python3
"""
Create GitHub Pull Requests with templates and automation.

Usage:
    from create_pr import create_pull_request

    pr = create_pull_request(
        repo="owner/repo",
        title="feat: Add new feature",
        head="feature-branch",
        base="main",
        body_template="default",
        reviewers=["user1", "user2"]
    )
"""

from github import Github
import os
from pathlib import Path


def load_template(template_name: str = "default") -> str:
    """Load PR template from assets folder."""
    templates_dir = Path(__file__).parent.parent / "assets"
    template_path = templates_dir / "pr_template.md"

    if template_path.exists():
        return template_path.read_text()
    return ""


def create_pull_request(
    repo: str,
    title: str,
    head: str,
    base: str = "main",
    body: str = None,
    body_template: str = None,
    draft: bool = False,
    reviewers: list = None,
    team_reviewers: list = None,
    labels: list = None,
    assignees: list = None,
    maintainer_can_modify: bool = True,
):
    """
    Create a pull request with optional template and automation.

    Args:
        repo: Repository in format "owner/repo"
        title: PR title
        head: Source branch name
        base: Target branch name (default: "main")
        body: PR description (overrides body_template)
        body_template: Template name to use (e.g., "default")
        draft: Create as draft PR
        reviewers: List of user logins to request review from
        team_reviewers: List of team slugs to request review from
        labels: List of label names to apply
        assignees: List of user logins to assign
        maintainer_can_modify: Allow maintainer edits

    Returns:
        PullRequest object from PyGithub
    """
    # Initialize GitHub client
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")

    g = Github(token)
    repository = g.get_repo(repo)

    # Prepare PR body
    pr_body = body
    if pr_body is None and body_template:
        pr_body = load_template(body_template)

    # Create pull request
    pr = repository.create_pull(
        title=title,
        body=pr_body or "",
        head=head,
        base=base,
        draft=draft,
        maintainer_can_modify=maintainer_can_modify,
    )

    print(f"✓ Created PR #{pr.number}: {title}")
    print(f"  URL: {pr.html_url}")

    # Add reviewers
    if reviewers or team_reviewers:
        pr.create_review_request(
            reviewers=reviewers or [], team_reviewers=team_reviewers or []
        )
        if reviewers:
            print(f"✓ Requested reviews from: {', '.join(reviewers)}")
        if team_reviewers:
            print(f"✓ Requested reviews from teams: {', '.join(team_reviewers)}")

    # Add labels
    if labels:
        pr.add_to_labels(*labels)
        print(f"✓ Added labels: {', '.join(labels)}")

    # Add assignees
    if assignees:
        pr.add_to_assignees(*assignees)
        print(f"✓ Assigned to: {', '.join(assignees)}")

    return pr


def update_pr(
    repo: str,
    pr_number: int,
    title: str = None,
    body: str = None,
    state: str = None,
    base: str = None,
    reviewers: list = None,
    labels: list = None,
):
    """
    Update an existing pull request.

    Args:
        repo: Repository in format "owner/repo"
        pr_number: PR number to update
        title: New title
        body: New body
        state: "open" or "closed"
        base: New base branch
        reviewers: List of reviewers to add
        labels: List of labels to add
    """
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    g = Github(token)
    repository = g.get_repo(repo)
    pr = repository.get_pull(pr_number)

    # Update basic fields
    update_kwargs = {}
    if title:
        update_kwargs["title"] = title
    if body:
        update_kwargs["body"] = body
    if state:
        update_kwargs["state"] = state
    if base:
        update_kwargs["base"] = base

    if update_kwargs:
        pr.edit(**update_kwargs)
        print(f"✓ Updated PR #{pr_number}")

    # Add reviewers
    if reviewers:
        pr.create_review_request(reviewers=reviewers)
        print(f"✓ Added reviewers: {', '.join(reviewers)}")

    # Add labels
    if labels:
        pr.add_to_labels(*labels)
        print(f"✓ Added labels: {', '.join(labels)}")

    return pr


def merge_pr(
    repo: str,
    pr_number: int,
    merge_method: str = "squash",
    commit_title: str = None,
    commit_message: str = None,
    delete_branch: bool = True,
):
    """
    Merge a pull request.

    Args:
        repo: Repository in format "owner/repo"
        pr_number: PR number to merge
        merge_method: "merge", "squash", or "rebase"
        commit_title: Custom commit title
        commit_message: Custom commit message
        delete_branch: Delete head branch after merge

    Returns:
        PullRequestMergeStatus object
    """
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    g = Github(token)
    repository = g.get_repo(repo)
    pr = repository.get_pull(pr_number)

    # Merge PR
    result = pr.merge(
        merge_method=merge_method,
        commit_title=commit_title,
        commit_message=commit_message,
    )

    if result.merged:
        print(f"✓ Merged PR #{pr_number} using {merge_method} method")
        print(f"  Commit SHA: {result.sha}")

        # Delete branch if requested
        if delete_branch:
            try:
                ref = repository.get_git_ref(f"heads/{pr.head.ref}")
                ref.delete()
                print(f"✓ Deleted branch: {pr.head.ref}")
            except Exception as e:
                print(f"⚠ Could not delete branch: {e}")
    else:
        print(f"✗ Failed to merge PR #{pr_number}: {result.message}")

    return result


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 5:
        print("Usage: python create_pr.py <repo> <title> <head> <base>")
        print("Example: python create_pr.py owner/repo 'feat: Add feature' feature-branch main")
        sys.exit(1)

    repo = sys.argv[1]
    title = sys.argv[2]
    head = sys.argv[3]
    base = sys.argv[4] if len(sys.argv) > 4 else "main"

    pr = create_pull_request(
        repo=repo,
        title=title,
        head=head,
        base=base,
        body_template="default",
    )

    print(f"\nPull request created successfully!")
    print(f"View at: {pr.html_url}")
