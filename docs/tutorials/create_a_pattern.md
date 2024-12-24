---
title: Create a Pattern
description: Create a pattern
icon:
date: 2024-08-28
comments: true
---

# Create a Pattern

We are going to convert an existing project into a pattern.
This process is going to require _lots_ of search and replace.

In another tutorial, we will break it into several patterns.

## Setup

1. Create a new directory named `patterns.`
1. Download the example project as a `.zip` file from TODO
1. Decompress the file and copy the `todo-manager` project into `patterns/`.
1. Inside the `patterns/` directory, create a file named `core_pattern.toml`

!!! Note

    If you are doing this with an actual project, remove the `.git` directory if it exists.

## Extracting questions

Questions are asked of the user during the project generation.
Each answer is set as the value of a variable used in patterns.
We will go through this example project and highlight information that would or could vary between projects.
We will create questions to get the data from the user,
and then we will replace the existing values in the example project with placeholders.

### Different names in different places

The outer folder is named `todo-manager`,
the code folder is named `todo_manager`,
and the title of the `README.md` file is `Todo Manager`.
Are these three different variables that require three different questions?
Is this one variable with three permutations that only require one question?

We will treat them as three variables. However, we don't necessarily require three answers.

### Project name

Let's start with the title of the `README.md` file. We'll call this the `project_name`.
We want to use this wherever we need a human-friendly name. Add a question to `core_pattern.toml`

```toml title="patterns/core_pattern.toml"
[[questions]]
name = "project_name"
prompt = "What is the human-friendly name of the project?"
type = "str"
default = "My Project"
```

### Package name

Now, let's deal with the outer folder name and the code folder.
Python package names (the package name registered with the Python package index)
are [normalized](https://packaging.python.org/en/latest/specifications/name-normalization/) using hyphens.
However, hyphens are not allowed in [Python identifiers](https://docs.python.org/3.12/reference/lexical_analysis.html#identifiers).

We'll call the name of the code folder the `package_name`. Add this question to `core_pattern.toml`:

```toml title="patterns/core_pattern.toml"
# ... previous question

[[questions]]
name = "package_name"
promp = "What is the name of the Python package?"
type = "str"
default = "{{ project_name|lower|replace(' ', '_') }}"
```

This sets the default answer to a modification of the previous question's answer.
It converts the answer to lowercase and replaces all spaces with underscores.
This is likely what the user wants, and if so, they can accept the default without having to type anything.

### Repo name

We'll call the name of the outer folder the `repo_name`. Add this question to `core_pattern.toml`:

```toml title="patterns/core_pattern.toml"
# ... previous questions

[[questions]]
name = "repo_name"
prompt = "What is the name of the project repository?"
type = "str"
default = "{{ package_name|replace('_', '-') }}"
```

This question modifies the answer from `package_name`, replacing the underscores with hyphens.

### Set the placeholders in files

- Search for `Todo Manager` and replace it with `{{ project_name }}`
- Search for `todo_manager` and replace it with `{{ package_name }}`
- Search for `todo-manager` and replace it with `{{ repo_name }}`

### Renaming files and directories with placeholders

- Rename the `todo-manager` directory to `{{ repo_name }}`
- Rename the `todo_manager` directory to `{{ package_name }}`
