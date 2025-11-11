# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Read these files for detailed information:

- @ARCHITECTURE.md - complete project architecture, module organization, dependency management strategy, development workflow, testing architecture, and deployment considerations
- @CODE_PRINCIPLES.md - coding standards, best practices, security guidelines, documentation requirements, and quality assurance processes
- @.claude/agents - agents configuration for Claude Code

## Essential Commands

All commands use uv for package management and task execution:

- `poe run` - Run the main application
- `poe typecheck` - Run types check
- `poe lint` - Run linting
- `poe format` - Run formatting
- `poe test` - Run tests quietly

## Tool Documentation Access

When working with project tools, use the following Context7 library IDs to access current documentation:
- uv: `/astral-sh/uv`
- Ruff: `/astral-sh/ruff`
- Pyright: `/microsoft/pyright`
- pytest: `/pytest-dev/pytest`

DO NOT look for library IDs. Use the ones provided here
