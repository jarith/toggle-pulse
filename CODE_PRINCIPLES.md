# Code Principles and Best Practices

This document outlines the coding standards, principles, and best practices for this Python project template.

## Core Principles

### 1. Type Safety First
- **Strict typing**: All functions must have type annotations for parameters and return values
- **Pyright strict mode**: Zero tolerance for type violations
- **Runtime validation**: Use type guards and validation where needed
- **Generic types**: Leverage Python's generic typing system for reusable code

### 2. Code Quality Standards
- **Comprehensive linting**: Follow all enabled Ruff rules without exceptions
- **Consistent formatting**: Use Ruff formatter for uniform code style
- **Import organization**: Automatic import sorting and grouping

### 3. Error Handling
- **Explicit error handling**: Never ignore exceptions silently
- **Specific exceptions**: Use specific exception types, avoid bare `except:`
- **Context preservation**: Use `raise ... from ...` to preserve exception chains
- **Validation**: Validate inputs at boundaries (function entries, API endpoints)

## Development Practices

### Testing Philosophy
- **Test-driven development**: Write tests before implementation when possible
- **Comprehensive coverage**: Aim for high test coverage with meaningful tests
- **Fast feedback**: Tests should run quickly for rapid development cycles
- **Clear assertions**: Use descriptive test names and clear assertion messages

### Code Organization
- **Single responsibility**: Each module, class, and function should have one clear purpose
- **Dependency injection**: Prefer dependency injection over global state
- **Configuration externalization**: Keep configuration separate from code
- **Minimal coupling**: Reduce dependencies between modules

### Performance Considerations
- **Memory efficiency**: Be mindful of memory usage, especially with large datasets
- **Lazy evaluation**: Use generators and lazy evaluation where appropriate
- **Caching strategy**: Implement appropriate caching for expensive operations

## Code Style Guidelines

### Naming Conventions
- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Private members**: Prefix with single underscore `_private`
- **Descriptive names**: Use clear, descriptive names over abbreviations

### Function Design
- **Small functions**: Keep functions focused and under 20 lines when possible
- **Pure functions**: Prefer pure functions without side effects
- **Early returns**: Use early returns to reduce nesting
- **Parameter validation**: Validate parameters at function entry points

### Class Design
- **Composition over inheritance**: Prefer composition to complex inheritance hierarchies
- **Immutable objects**: Make objects immutable where possible
- **Protocol classes**: Use Protocol classes for structural typing
- **Context managers**: Implement context managers for resource management

## Security Practices

### Data Protection
- **No secrets in code**: Never commit secrets, API keys, or sensitive data
- **Input sanitization**: Sanitize and validate all external inputs
- **SQL injection prevention**: Use parameterized queries, not string concatenation
- **Path traversal protection**: Validate file paths to prevent directory traversal

### Dependencies
- **Minimal dependencies**: Only add dependencies that provide significant value
- **Dependency pinning**: Pin dependency versions in production environments
- **Security scanning**: Regularly audit dependencies for vulnerabilities
- **License compliance**: Ensure all dependencies have compatible licenses

## Documentation Standards

### Code Documentation
- Do not include any docstrings at all

### README and Guides
- **Setup instructions**: Clear, step-by-step setup and installation guide
- **Usage examples**: Provide common usage patterns and examples
- **Contributing guidelines**: Document how others can contribute to the project
- **Architecture decisions**: Document significant architectural choices and rationale

## Quality Assurance

### Pre-commit Checks
- **Linting compliance**: Code must pass `poe lint` without warnings
- **Type checking**: Code must pass `poe typecheck` type checking
- **Test execution**: All tests must pass before merging

## Refactoring Guidelines

### When to Refactor
- **Code smells**: Address code smells during regular development
- **Changing requirements**: Refactor to accommodate new requirements cleanly
- **Technical debt**: Regularly allocate time for technical debt reduction

### Refactoring Process
- **Small steps**: Make incremental changes with tests passing at each step
- **Preserve behavior**: Ensure refactoring doesn't change external behavior
- **Update documentation**: Keep documentation in sync with code changes
- **Review impact**: Consider the impact of changes on dependent code
