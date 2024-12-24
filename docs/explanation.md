---
title: Explanations
summary: Why Project Forge is the way it is!
date: 2024-08-26
---

This page explains why Project Forge is the way it is.

Explanation is **discussion** that clarifies and illuminates a particular topic. Explanation is **understanding-oriented.**

- Give context and background on your library
- Explain why you created it
- Provide multiple examples and approaches of how to work with it
- Help the reader make connections
- Avoid writing instructions or technical descriptions here
- [More Information](https://diataxis.fr/explanation/)

## Overview

Project Forge is a scaffolding tool. A scaffolding tool allows developers to generate a new project by answering a few questions. Developers can go from idea to coding very quickly.

Additional needs:

- Combine several templates using composition.
- Projects can update themselves with updates from their dependent templates.
- Can use blocks within files to compose parts of files
- Don't ask the same question twice

Issues to be aware of:

- Context collisions
    - The question variable names match in two or more patterns, but their values and use are different.
- Patterns with similar questions but different names.
    - `project_name` vs. `name_of_project`
- Storage location of pattern configuration and pattern template
    - Local-Local
    - Local-Remote
    - Remote-Local
    - Remote-Remote
