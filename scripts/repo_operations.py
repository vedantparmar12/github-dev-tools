#!/usr/bin/env python3
"""
GitHub Repository Operations utilities.

Usage:
    from repo_operations import create_repository, push_multiple_files

    repo = create_repository("my-project", private=True)
    push_multiple_files(repo, files=[...], message="Initial commit")
"""

from github import Github, GithubException, InputGitTreeElement
import os
from typing import List, Dict, Optional


def get_github_client():
    """Get authenticated GitHub client."""
    token = os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN")
    if not token:
        raise ValueError("GITHUB_PERSONAL_ACCESS_TOKEN environment variable not set")
    return Github(token)


def create_repository(
    name: str,
    description: str = "",
    private: bool = False,
    auto_init: bool = True,
    gitignore_template: str = None,
    license_template: str = None,
    organization: str = None,
):
    """
    Create a new GitHub repository.

    Args:
        name: Repository name
        description: Repository description
        private: Create as private repository
        auto_init: Initialize with README
        gitignore_template: .gitignore template (e.g., "Python", "Node")
        license_template: License template (e.g., "mit", "apache-2.0")
        organization: Create in organization (otherwise creates for user)

    Returns:
        Repository object
    """
    g = get_github_client()

    try:
        if organization:
            org = g.get_organization(organization)
            repo = org.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=auto_init,
                gitignore_template=gitignore_template,
                license_template=license_template,
            )
            print(f"✓ Created repository: {organization}/{name}")
        else:
            user = g.get_user()
            repo = user.create_repo(
                name=name,
                description=description,
                private=private,
                auto_init=auto_init,
                gitignore_template=gitignore_template,
                license_template=license_template,
            )
            print(f"✓ Created repository: {user.login}/{name}")

        print(f"  URL: {repo.html_url}")
        return repo

    except GithubException as e:
        print(f"✗ Error creating repository: {e.data.get('message', str(e))}")
        raise


def create_branch(repo_name: str, branch_name: str, from_branch: str = None):
    """
    Create a new branch in a repository.

    Args:
        repo_name: Repository in format "owner/repo"
        branch_name: Name of the new branch
        from_branch: Source branch (defaults to repository default branch)

    Returns:
        GitRef object for the new branch
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)

    # Get source branch
    if from_branch:
        source = repo.get_branch(from_branch)
    else:
        source = repo.get_branch(repo.default_branch)

    # Create new branch
    ref = repo.create_git_ref(
        ref=f"refs/heads/{branch_name}",
        sha=source.commit.sha
    )

    print(f"✓ Created branch '{branch_name}' from '{source.name}'")
    return ref


def push_multiple_files(
    repo_name: str,
    files: List[Dict[str, str]],
    message: str,
    branch: str = None,
):
    """
    Push multiple files in a single commit using Git Trees API.

    Args:
        repo_name: Repository in format "owner/repo"
        files: List of dicts with 'path' and 'content' keys
               Example: [{"path": "src/app.py", "content": "print('hi')"}]
        message: Commit message
        branch: Branch name (defaults to repository default branch)

    Returns:
        Commit object
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)

    # Get branch reference
    if not branch:
        branch = repo.default_branch

    ref = repo.get_git_ref(f"heads/{branch}")
    latest_commit = repo.get_git_commit(ref.object.sha)

    # Create tree elements
    tree_elements = []
    for file in files:
        tree_elements.append(
            InputGitTreeElement(
                path=file["path"],
                mode="100644",  # Regular file
                type="blob",
                content=file["content"]
            )
        )

    # Create new tree
    tree = repo.create_git_tree(tree_elements, base_tree=latest_commit.tree)

    # Create commit
    commit = repo.create_git_commit(
        message=message,
        tree=tree,
        parents=[latest_commit]
    )

    # Update branch reference
    ref.edit(sha=commit.sha)

    print(f"✓ Pushed {len(files)} files to {branch}")
    print(f"  Commit: {commit.sha[:7]} - {message}")

    return commit


def delete_file(repo_name: str, path: str, message: str, branch: str = None):
    """
    Delete a file from the repository.

    Args:
        repo_name: Repository in format "owner/repo"
        path: Path to file to delete
        message: Commit message
        branch: Branch name (defaults to repository default branch)

    Returns:
        Commit info dict
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)

    if not branch:
        branch = repo.default_branch

    # Get file to get its SHA
    contents = repo.get_contents(path, ref=branch)

    # Delete file
    result = repo.delete_file(
        path=path,
        message=message,
        sha=contents.sha,
        branch=branch
    )

    print(f"✓ Deleted {path} from {branch}")
    return result


def get_file_contents(repo_name: str, path: str, ref: str = None):
    """
    Get file contents from repository.

    Args:
        repo_name: Repository in format "owner/repo"
        path: Path to file or directory
        ref: Branch, tag, or commit SHA (defaults to default branch)

    Returns:
        ContentFile or list of ContentFile objects
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)

    contents = repo.get_contents(path, ref=ref or repo.default_branch)

    # If it's a single file, decode and return content
    if not isinstance(contents, list):
        print(f"✓ Retrieved {path}")
        return contents.decoded_content.decode('utf-8')

    # If it's a directory, return list of files
    print(f"✓ Retrieved directory {path} ({len(contents)} items)")
    return contents


def search_code(query: str, repo: str = None):
    """
    Search for code across repositories.

    Args:
        query: Search query (supports GitHub code search syntax)
        repo: Optional repo to limit search to "owner/repo"

    Returns:
        List of ContentFile objects
    """
    g = get_github_client()

    # Add repo filter if provided
    full_query = query
    if repo:
        full_query = f"{query} repo:{repo}"

    # Search code
    results = g.search_code(query=full_query)

    print(f"Found {results.totalCount} code results for: {full_query}")
    return list(results)


def fork_repository(repo_name: str, organization: str = None):
    """
    Fork a repository.

    Args:
        repo_name: Repository to fork in format "owner/repo"
        organization: Optional organization to fork to

    Returns:
        Repository object of the fork
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)

    if organization:
        fork = repo.create_fork(organization=organization)
        print(f"✓ Forked {repo_name} to {organization}/{fork.name}")
    else:
        fork = repo.create_fork()
        print(f"✓ Forked {repo_name} to {fork.full_name}")

    print(f"  URL: {fork.html_url}")
    return fork


def list_branches(repo_name: str):
    """
    List all branches in a repository.

    Args:
        repo_name: Repository in format "owner/repo"

    Returns:
        List of Branch objects
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)

    branches = list(repo.get_branches())
    print(f"Found {len(branches)} branches in {repo_name}")

    for branch in branches:
        marker = " (default)" if branch.name == repo.default_branch else ""
        print(f"  - {branch.name}{marker}")

    return branches


def get_repository_tree(
    repo_name: str,
    tree_sha: str = None,
    recursive: bool = True,
    path_filter: str = None
):
    """
    Get repository file tree structure.

    Args:
        repo_name: Repository in format "owner/repo"
        tree_sha: Tree SHA or ref (defaults to default branch)
        recursive: Get full tree recursively
        path_filter: Optional path prefix filter

    Returns:
        List of tree elements
    """
    g = get_github_client()
    repo = g.get_repo(repo_name)

    if not tree_sha:
        tree_sha = repo.default_branch

    tree = repo.get_git_tree(tree_sha, recursive=recursive)

    items = tree.tree
    if path_filter:
        items = [item for item in items if item.path.startswith(path_filter)]

    print(f"Retrieved tree with {len(items)} items")
    return items


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) < 2:
        print("Available commands:")
        print("  create <name> [--private] [--org ORG]")
        print("  branch <repo> <branch-name> [from-branch]")
        print("  search <query>")
        print("  fork <repo> [--org ORG]")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        name = sys.argv[2]
        private = "--private" in sys.argv
        org = sys.argv[sys.argv.index("--org") + 1] if "--org" in sys.argv else None
        create_repository(name, private=private, organization=org)

    elif command == "branch":
        repo = sys.argv[2]
        branch = sys.argv[3]
        from_branch = sys.argv[4] if len(sys.argv) > 4 else None
        create_branch(repo, branch, from_branch)

    elif command == "search":
        query = sys.argv[2]
        results = search_code(query)
        for r in results[:10]:  # Show first 10
            print(f"  {r.repository.full_name}/{r.path}")

    elif command == "fork":
        repo = sys.argv[2]
        org = sys.argv[sys.argv.index("--org") + 1] if "--org" in sys.argv else None
        fork_repository(repo, organization=org)
