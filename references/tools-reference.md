# GitHub Dev Tools Reference

Complete reference for core GitHub operations (repos, issues, PRs, collaboration).

## Table of Contents
1. [Context Tools](#context-tools)
2. [Repository Tools](#repository-tools)
3. [Issue Tools](#issue-tools)
4. [Pull Request Tools](#pull-request-tools)
5. [Discussions Tools](#discussions-tools)
6. [Gists Tools](#gists-tools)
7. [Notifications Tools](#notifications-tools)
8. [Labels Tools](#labels-tools)

---

## Context Tools

### get_me
Get authenticated user profile.
- No parameters

### get_teams
Get teams for a user.
- `user` (string, optional): Username (default: authenticated user)

### get_team_members
Get team members.
- `org` (string, required): Organization login
- `team_slug` (string, required): Team slug

---

## Repository Tools

### create_repository
- `name` (string, required): Repo name
- `description` (string, optional)
- `private` (boolean, optional)
- `autoInit` (boolean, optional): Init with README
- `organization` (string, optional): Create in org

### create_branch
- `owner`, `repo` (required)
- `branch` (string, required): New branch name
- `from_branch` (string, optional): Source (default: repo default)

### create_or_update_file
- `owner`, `repo`, `path`, `content`, `message`, `branch` (required)
- `sha` (string, optional): Required for updates

### push_files
Push multiple files in one commit.
- `owner`, `repo`, `branch`, `message` (required)
- `files` (array, required): `[{path, content}, ...]`

### get_file_contents
- `owner`, `repo` (required)
- `path` (string, optional): File or directory path
- `ref` (string, optional): Branch/tag/commit

### delete_file
- `owner`, `repo`, `path`, `message`, `branch` (required)

### list_branches
- `owner`, `repo` (required)
- `page`, `perPage` (optional): Pagination

### list_commits
- `owner`, `repo` (required)
- `sha` (string, optional): Branch/tag to list from
- `author` (string, optional): Filter by author

### get_commit
- `owner`, `repo`, `sha` (required)
- `include_diff` (boolean, optional): Include diffs (default: true)

### search_repositories
- `query` (string, required): Search query
- `sort` (string, optional): stars, forks, updated
- `order` (string, optional): asc, desc

### search_code
- `query` (string, required): Code search query
- `sort`, `order` (optional)

### fork_repository
- `owner`, `repo` (required)
- `organization` (string, optional): Fork to org

### list_releases
- `owner`, `repo` (required)

### get_latest_release
- `owner`, `repo` (required)

### list_tags
- `owner`, `repo` (required)

### get_repository_tree
- `owner`, `repo` (required)
- `tree_sha` (string, optional): SHA or ref
- `recursive` (boolean, optional)
- `path_filter` (string, optional)

---

## Issue Tools

### list_issues
- `owner`, `repo` (required)
- `state` (string, optional): open, closed, all
- `labels` (array, optional): Filter labels
- `orderBy`, `direction` (optional)
- `since` (string, optional): ISO 8601 date

### search_issues
- `query` (string, required): Search syntax
- `owner`, `repo` (optional): Limit to repo
- `sort`, `order` (optional)

### issue_read
- `owner`, `repo`, `issue_number` (required)
- `method` (string, required):
  - `get`: Issue details
  - `get_comments`: Comments
  - `get_sub_issues`: Sub-issues
  - `get_labels`: Labels

### issue_write
- `owner`, `repo`, `method` (required)
- `method`: `create` or `update`
- `title` (required for create)
- `body`, `labels`, `assignees`, `milestone` (optional)
- `issue_number` (required for update)
- `state`: open, closed
- `state_reason`: completed, not_planned, reopened, duplicate

### add_issue_comment
- `owner`, `repo`, `issue_number`, `body` (required)

### sub_issue_write
- `owner`, `repo`, `issue_number`, `sub_issue_id` (required)
- `method`: add, remove, reprioritize
- `before_id`, `after_id` (for reprioritize)

---

## Pull Request Tools

### list_pull_requests
- `owner`, `repo` (required)
- `state`: open, closed, all
- `head`, `base` (optional filters)
- `sort`, `direction` (optional)

### search_pull_requests
- `query` (string, required)
- `owner`, `repo` (optional)

### create_pull_request
- `owner`, `repo`, `title`, `head`, `base` (required)
- `body` (string, optional)
- `draft` (boolean, optional)
- `maintainer_can_modify` (boolean, optional)

### pull_request_read
- `owner`, `repo`, `pullNumber` (required)
- `method` (required):
  - `get`: PR details
  - `get_diff`: Diff content
  - `get_status`: CI status
  - `get_files`: Changed files
  - `get_review_comments`: Review comments
  - `get_reviews`: Reviews
  - `get_comments`: General comments

### update_pull_request
- `owner`, `repo`, `pullNumber` (required)
- `title`, `body`, `state`, `base` (optional)
- `draft` (boolean, optional)
- `reviewers` (array, optional)

### merge_pull_request
- `owner`, `repo`, `pullNumber` (required)
- `merge_method`: merge, squash, rebase
- `commit_title`, `commit_message` (optional)

### update_pull_request_branch
Sync PR branch with base.
- `owner`, `repo`, `pullNumber` (required)
- `expectedHeadSha` (optional)

### pull_request_review_write
- `owner`, `repo`, `pullNumber` (required)
- `method`: create, submit, delete
- `body` (optional)
- `event`: APPROVE, REQUEST_CHANGES, COMMENT

### add_comment_to_pending_review
- `owner`, `repo`, `pullNumber`, `path`, `body` (required)
- `line`, `side`, `startLine`, `startSide` (optional)
- `subjectType`: line, file

---

## Discussions Tools

### list_discussions
- `owner` (required), `repo` (optional for org-level)
- `category` (optional): Category ID filter
- `orderBy`, `direction` (optional)

### get_discussion
- `owner`, `repo`, `discussionNumber` (required)

### get_discussion_comments
- `owner`, `repo`, `discussionNumber` (required)
- Pagination options

### list_discussion_categories
- `owner` (required), `repo` (optional)

---

## Gists Tools

### list_gists
- `username` (optional): Default to auth user
- `since` (optional): ISO 8601 timestamp

### get_gist
- `gist_id` (required)

### create_gist
- `filename`, `content` (required)
- `description` (optional)
- `public` (boolean, optional)

### update_gist
- `gist_id`, `filename`, `content` (required)
- `description` (optional)

---

## Notifications Tools

### list_notifications
- `filter`: default, read, participating
- `owner`, `repo` (optional): Filter by repo
- `since`, `before` (optional)

### get_notification_details
- `notificationID` (required)

### dismiss_notification
- `threadID` (required)
- `state`: read, done

### mark_all_notifications_read
- `owner`, `repo` (optional)
- `lastReadAt` (optional)

### manage_notification_subscription
- `notificationID` (required)
- `action`: ignore, watch, delete

### manage_repository_notification_subscription
- `owner`, `repo` (required)
- `action`: ignore, watch, delete

---

## Labels Tools

### list_label
- `owner`, `repo` (required)

### get_label
- `owner`, `repo`, `name` (required)

### label_write
- `owner`, `repo`, `name`, `method` (required)
- `method`: create, update, delete
- `color` (6-char hex, no #)
- `description` (optional)
- `new_name` (for rename)

---

## Stargazers Tools

### list_starred_repositories
- `username` (optional)
- `sort`: created, updated
- `direction` (optional)

### star_repository
- `owner`, `repo` (required)

### unstar_repository
- `owner`, `repo` (required)

---

## Users Tools

### search_users
- `query` (required)
- `sort`: followers, repositories, joined
- `order` (optional)
