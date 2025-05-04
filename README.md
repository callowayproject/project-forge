# Project Forge

<a href="https://pypi.org/project/project-forge/"><img src="https://img.shields.io/pypi/v/project-forge.svg"></a>
<a href="https://pypi.org/project/project-forge/"><img src="https://img.shields.io/pypi/l/project-forge.svg"></a>
<a href="https://pypi.org/project/project-forge/"><img src="https://img.shields.io/pypi/pyversions/project-forge.svg"></a>
<a href="https://github.com/callowayproject/project-forge/actions"><img src="https://github.com/callowayproject/project-forge/workflows/CI/badge.svg"></a>

<!--start-->

Project Forge is an extensible and composable project scaffolding tool.
Developers can quickly generate new projects by only answering a few questions.

- In current project scaffolding, variations in templates magnify complexity.
- Maintainability increases as complexity increases.

A tool that lets platform teams pave a golden path and still allows developers to customize when necessary

## Features

- Create new projects from a composition of several patterns.
- Compose individual files using template blocks.
- *Coming soon.* Add new capabilities to an existing project by applying a pattern.
- *Coming soon.* Update a generated project when its patterns are updated.

## Introduction

Project Forge treats project building like building a sandwich.
A sandwich is a combination of ingredients.
The recipe for a sandwich lists the required ingredients and the assembly instructions.
A person can easily alter the recipe by adding, removing, or substituting ingredients.

Other scaffolding tools treat project building like using a vending machine.
Your choices are limited by what is available in the vending machine.

## Composable project templates

- patterns can contain templates that extend other pattern templates
- developers can customize an existing pattern's definition and still use the original's templates

Project Forge's key feature is that it is designed to generate projects from multiple, smaller templates called _patterns_.

- **Special knowledge, special patterns.**
    Let people with the proper expertise write specific patterns.
    For example, DevOps people create and update Helm or Terraform patterns, which developers can include in compositions that generate projects.
- **Loose coupling.**
    Each pattern has its lifecycle for changes and updates independent of compositions that include it.
    Patterns are treated as installable libraries with version constraints.
- **Increased flexibility using simpler patterns.**
    Other scaffolding solutions must include all possible options in the template.
    This requires complex template logic which increases template maintenance difficulty.
    Using compositions to specify the combination of simple patterns gives developers more flexibility while making pattern maintainers' jobs more manageable.

## Building a project like a sandwich

A _pattern_ is like a sandwich ingredient.
It is the smallest individual part.
You can render a pattern by itself, like eating a sandwich ingredient.

*Pattern questions* are like known ways of preparing sandwich ingredients.
Just like a hamburger is an ingredient in a sandwich, "Doneness" with options of well, medium, and raw is a pattern question.

A *composition* is a recipe.
It includes configuration and instructions only.

*Overlays* and *tasks* are like recipe instructions.
Each _overlay_ references a pattern and how to configure it for the composition, like "Hamburger, well done."
A task performs an action during project generation, like "stir for 3 minutes."

<!--end-->
