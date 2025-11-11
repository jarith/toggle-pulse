# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

YOU MUST Read these files for detailed information:

- ARCHITECTURE.md - complete project architecture, module organization, dependency management strategy, development workflow, testing architecture, and deployment considerations
- CODE_PRINCIPLES.md - coding standards, best practices, security guidelines, documentation requirements, and quality assurance processes

## Essential Commands

All commands use uv for package management and task execution:

- `poe run` - Run the main application
- `poe typecheck` - Run types check
- `poe lint` - Run linting
- `poe format` - Run formatting
- `poe test` - Run tests quietly

## Tool Documentation Acces## Tool Documentation Access

When working with project tools, use the following Context7 library IDs to access current documentation:
- uv: `/astral-sh/uv` - Fast Python package installer and resolver
- Ruff: `/astral-sh/ruff` - Extremely fast Python linter and code formatter
- Pyright: `/microsoft/pyright` - Static type checker for Python
- pytest: `/pytest-dev/pytest` - Testing framework for Python
- Docker: `/docker/docs` - Platform for developing, shipping, and running applications in containers
- returns: `/dry-python/returns` - Functional programming library with typed, safe return values (Maybe, Result, IO containers)

MANDATORY: DO NOT look for library IDs. Use the ones provided here

MANDATORY: ALWAYS FETCH the aiogram documentation from context7 using the provided libraryID EVERY TIME before working with aiogram code - no exceptions
MANDATORY: ALWAYS FETCH the pytest documentation from context7 using the provided libraryID EVERY TIME before writing any test - no exceptions
MANDATORY: ALWAYS FETCH the aiohttp documentation from context7 using the provided libraryID EVERY TIME before working with aiohttp HTTP clients - no exceptions
MANDATORY: ALWAYS FETCH the aioresponses documentation from context7 using the provided libraryID EVERY TIME before mocking HTTP requests in tests - no exceptions
MANDATORY: ALWAYS FETCH the pytest-asyncio documentation from context7 using the provided libraryID EVERY TIME before writing async tests - no exceptions
MANDATORY: ALWAYS FETCH the todoist-api-python documentation from context7 using the provided libraryID EVERY TIME before working with Todoist API - no exceptions
MANDATORY: ALWAYS FETCH the returns documentation from context7 using the provided libraryID EVERY TIME before writing async tests - no exceptions

MANDATORY: ALWAYS call suitable agents for performing tasks
