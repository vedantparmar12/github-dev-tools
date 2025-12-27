# GitHub Search Syntax

Quick reference for GitHub search queries.

## Issue & PR Search

### State Filters
```
is:issue          # Issues only
is:pr             # PRs only
is:open           # Open
is:closed         # Closed
is:merged         # Merged PRs
is:draft          # Draft PRs
```

### People
```
author:username       # Created by
assignee:username     # Assigned to
mentions:username     # Mentions user
involves:username     # Author/assignee/commenter/mentioned
commenter:username    # Has comment from
review:approved       # PR approved
reviewed-by:username  # Reviewed by
review-requested:username
```

### Labels & Milestones
```
label:bug             # Has label
label:"help wanted"   # Label with spaces
-label:wontfix        # Doesn't have label
milestone:"v1.0"      # In milestone
no:milestone          # No milestone
no:label              # No labels
no:assignee           # Unassigned
```

### Dates
```
created:>2024-01-01              # After date
created:2024-01-01..2024-06-01   # Range
updated:>2024-01-01              # Updated after
closed:>2024-01-01               # Closed after
```

### Examples
```
# My open issues
is:issue is:open author:@me

# PRs needing my review
is:pr is:open review-requested:@me

# Open bugs
is:issue is:open label:bug

# Stale issues
is:issue is:open updated:<2024-01-01
```

---

## Code Search

### Filters
```
language:python       # By language
path:src/            # In directory
path:*.py            # File extension
filename:config      # File name
extension:js         # Extension
content:function     # Contains text
```

### Scope
```
repo:owner/repo      # Specific repo
org:orgname          # Organization
user:username        # User's repos
```

### Examples
```
# Find function in org
"process_data" language:python org:myorg

# Config files
filename:config extension:json

# React components
content:"import React" path:src/components/
```

---

## Repository Search

### Filters
```
stars:>1000          # Popular
forks:>100           # Many forks
language:python      # Primary language
topic:react          # Has topic
```

### In Fields
```
in:name keyword      # In repo name
in:description       # In description
in:readme            # In README
```

### Examples
```
# Popular Python repos
language:python stars:>1000

# By topic
topic:machine-learning language:python
```

---

## Boolean Operators

```
keyword1 keyword2    # AND (implicit)
keyword1 OR keyword2 # OR
NOT keyword          # Exclude
-keyword             # Exclude (shorthand)
"exact phrase"       # Exact match
```
