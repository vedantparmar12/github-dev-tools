 Key Features

  1. Repository Management: Create repos, branches, push files, search code, fork repos
  2. Issue Tracking: Create, search, update issues with templates and auto-triage
  3. Pull Requests: Create PRs, request reviews, merge with validation
  4. Team Collaboration: Discussions, gists, notifications
  5. Automation: Batch operations, automated workflows, templates

  Quick Start

  1. Installation

  # Option A: Using installer
  cd github-dev-tools
  ./install.sh  # or .\install.ps1 on Windows

  # Option B: Manual
  cp -r github-dev-tools ~/.codex/skills/

  2. Setup GitHub Token

  # Create token at: https://github.com/settings/tokens
  # Scopes needed: repo, read:org, gist, notifications

  export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"
  echo 'export GITHUB_PERSONAL_ACCESS_TOKEN="ghp_your_token_here"' >> ~/.bashrc

  3. Install Dependencies

  pip install -r github-dev-tools/scripts/requirements.txt

  4. Use in Codex

  Create a PR from feature-auth to main
  List all open bugs in owner/repo
  Search for "authentication" in Python files

  Usage Examples

  In Codex (Natural Language)

  Create a pull request from my feature branch to main
  List my open issues
  Create an issue for the login bug

  Python Scripts

  # Create PR
  python scripts/create_pr.py owner/repo "feat: Add auth" feature-auth main

  # Create issue
  python scripts/create_issue.py owner/repo "Bug: Login fails" "Description..."

  # Create repo
  python scripts/repo_operations.py create my-repo --private

  Python API

  from github import Github
  import os

  g = Github(os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"])
  repo = g.get_repo("owner/repo")

  # Create PR
  pr = repo.create_pull(
      title="feat: Add feature",
      head="feature-branch",
      base="main"
  )

  Distribution

  Share with others:
  - Via package: github-dev-tools.skill.tar.gz or github-dev-tools.skill.zip
  - Via GitHub: Push the github-dev-tools/ folder to a repository
  - Direct copy: Share the entire github-dev-tools/ directory

  Next Steps

  1. Read github-dev-tools/README.md for full documentation
  2. Check github-dev-tools/QUICK_REFERENCE.md for command reference
  3. Customize templates in assets/ for your team
  4. Add custom workflows to SKILL.md
  5. Share with your team!

  All files are in:
  - Skill package: C:\Users\vedan\github-dev-tools\
  - Distribution packages: C:\Users\vedan\github-dev-tools.skill.*
  - Summary: C:\Users\vedan\SKILL_CREATION_SUMMARY.md

> where is this skills.tar.gz located can you give me path

● Bash(ls -lh C:/Users/vedan/*.skill.* && pwd)
  ⎿  -rw-r--r-- 1 vedan 197609 17K Dec 27 08:53 C:/Users/vedan/github-dev-tools.skill.tar.gz
     -rw-r--r-- 1 vedan 197609 20K Dec 27 08:54 C:/Users/vedan/github-dev-tools.skill.zip
     /c/Users/vedan

● The skill packages are located at:

  Tar.gz (for Linux/macOS):
  C:\Users\vedan\github-dev-tools.skill.tar.gz

  Zip (for Windows):
  C:\Users\vedan\github-dev-tools.skill.zip

  Source skill directory:
  C:\Users\vedan\github-dev-tools\

  You can use any of these to install or distribute the skills.
