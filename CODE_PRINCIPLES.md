# Code Principles and Best Practices

This document outlines the coding standards, principles, and best practices for this Python project template.

## Core Principles

- **No docstrings**
- **Minimal comments**: Only add comments for complex, non-obvious logic. Avoid obvious comments
- **Railway-oriented programming**: Follow https://fsharpforfunandprofit.com/rop/ patterns
- **Functional-first**: Pure functions, immutable data, minimal classes
- **Type safety**: Strict Pyright mode, comprehensive type annotations
- **Error handling**: Use functional containers (Result, IOResult, Maybe) instead of try/catch
- **Testing**: Integration tests preferred over unit tests, minimal mocking
- **Service Registry**: Dependency injection via service registry pattern
- **Immutable Data**: Frozen dataclasses for all response models

### 1. Type Safety First
- **Strict typing**: All functions must have type annotations for parameters and return values
- **Pyright strict mode**: Zero tolerance for type violations
- **Runtime validation**: Use type guards and validation where needed
- **Generic types**: Leverage Python's generic typing system for reusable code

### 2. Code Quality Standards
- **Comprehensive linting**: Follow all enabled Ruff rules without exceptions
- **Consistent formatting**: Use Ruff formatter for uniform code style
- **Import organization**: Automatic import sorting and grouping

### 3. Railway-Oriented Error Handling
- **Two-track model**: All operations return container types (Result, IOResult, Maybe) with success/failure tracks
- **No exceptions**: Never use try/catch blocks - use `@safe` and `@impure_safe` decorators instead
- **Explicit error types**: Define specific error types as data, not exceptions
- **Error composition**: Chain operations using `bind`, `map`, `lash`, and `flow`
- **Early returns**: Use container methods like `bind` to short-circuit on errors
- **Context preservation**: Error context is preserved through the container chain

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

### Programming Paradigm Preferences
- **Functional programming first**: MANDATORY - Use functional programming with returns library containers
- **Pure functions**: Wrap all impure operations in IO/IOResult containers
- **Immutable data structures**: Use frozen dataclasses and immutable collections
- **Function composition**: Use `flow` and `pipe` for composing operations
- **Container-based programming**: All functions should return container types (Result, IO, Maybe, etc.)
- **Avoid classes**: Use classes only for protocols, frozen dataclasses, and when required by frameworks
- **Stateless design**: No mutable state - use functional containers for state management
- **Monadic operations**: Use `bind`, `map`, `apply` for chaining computations
- **Railway-oriented patterns**: Every function should handle both success and failure tracks

### Performance Considerations
- **Memory efficiency**: Be mindful of memory usage, especially with large datasets
- **Lazy evaluation**: Use generators and lazy evaluation where appropriate
- **Caching strategy**: Implement appropriate caching for expensive operations

## Railway-Oriented Programming

### Core Concept
Following the patterns from https://fsharpforfunandprofit.com/rop/, all code must be written using the two-track railway model:
- **Success track**: Happy path where operations succeed
- **Failure track**: Error path that propagates through the chain
- **Switch functions**: Operations that can move from success to failure track
- **Single-track functions**: Pure transformations that stay on the current track

### Railway Patterns
1. **Bind pattern**: Connect two-track functions (functions returning containers)
2. **Map pattern**: Lift single-track functions to work with containers
3. **Tee pattern**: Execute side effects while staying on the track
4. **Plus pattern**: Combine parallel validations
5. **Lash pattern**: Move from failure track back to success track

### Composition Rules
- Build pipelines where errors flow naturally without interruption
- Each function in the pipeline handles its own errors
- Errors accumulate or short-circuit based on business logic
- No function should throw exceptions - all errors are data
- Use `flow()` to create readable left-to-right pipelines

## Functional Containers Usage (returns library)

### Container Types and Their Usage
- **Result[Value, Error]**: For pure functions that can fail
- **IOResult[Value, Error]**: For impure functions that can fail (I/O, network, DB)
- **Maybe[Value]**: For optional values, replaces None/Optional
- **IO[Value]**: For impure functions that always succeed
- **Future[Value]**: For async operations that always succeed
- **FutureResult[Value, Error]**: For async operations that can fail

### Mandatory Patterns
1. **Never use try/catch**: Always use `@safe` or `@impure_safe` decorators
2. **Chain with bind**: Use `.bind()` for operations that return containers
3. **Transform with map**: Use `.map()` for pure transformations
4. **Compose with flow**: Build pipelines using `flow()` and `pipe()`
5. **Handle errors with lash**: Use `.lash()` to recover from failures
6. **Collect multiple results**: Use `Fold.collect()` for aggregating containers

### Example Patterns
```python
# WRONG - Imperative style with exceptions
def get_user(user_id: int) -> User:
    try:
        response = requests.get(f'/api/users/{user_id}')
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error(f"Failed to get user: {e}")
        raise

# CORRECT - Functional style with containers
@impure_safe
def get_user(user_id: int) -> IOResult[User, Exception]:
    return flow(
        user_id,
        lambda uid: requests.get(f'/api/users/{uid}'),
        lambda resp: resp.raise_for_status() or resp,
        lambda resp: resp.json(),
    )
```

### Error Type Design
- Define error types as frozen dataclasses, not exception classes
- Use Union types for multiple error possibilities
- Preserve error context through the chain
- Never catch exceptions - let containers handle them

## Code Style Guidelines

### Early Return Pattern (Guard Clauses)

Use early returns to avoid deeply nested conditionals and eliminate else statements:

#### Why Early Returns?
- **Flat code structure**: Reduces indentation levels and cognitive load
- **Clear preconditions**: Invalid cases are handled at the function's beginning
- **Readable happy path**: Main logic becomes more prominent without nesting
- **Mental stack reduction**: Exit early to free mental capacity for main logic

#### Implementation with Containers

In functional programming with containers, early returns are achieved through short-circuiting:

```python
# WRONG - Nested conditionals with else
@safe
def process_user_data(data: dict) -> Result[ProcessedData, str]:
    if data:
        if "user_id" in data:
            if data["user_id"] > 0:
                # Process the data
                return Success(ProcessedData(...))
            else:
                return Failure("Invalid user ID")
        else:
            return Failure("Missing user ID")
    else:
        return Failure("No data provided")

# CORRECT - Guard clauses with early returns
@safe
def process_user_data(data: dict) -> Result[ProcessedData, str]:
    if not data:
        return Failure("No data provided")

    if "user_id" not in data:
        return Failure("Missing user ID")

    if data["user_id"] <= 0:
        return Failure("Invalid user ID")

    # Happy path - main logic without nesting
    return Success(ProcessedData(...))
```

#### Railway-Oriented Early Returns

With railway-oriented programming, use bind operations for automatic early returns:

```python
# WRONG - Manual checking with nested ifs
def fetch_and_process(user_id: int) -> IOResult[User, str]:
    result = fetch_user(user_id)
    if isinstance(result, Success):
        user = result.unwrap()
        if user.is_active:
            processed = process_user(user)
            if isinstance(processed, Success):
                return IOSuccess(processed.unwrap())
            else:
                return IOFailure("Processing failed")
        else:
            return IOFailure("User is inactive")
    else:
        return IOFailure("User not found")

# CORRECT - Railway pattern with automatic early returns
def fetch_and_process(user_id: int) -> IOResult[User, str]:
    return flow(
        fetch_user(user_id),
        bind(lambda user: IOSuccess(user) if user.is_active else IOFailure("User is inactive")),
        bind(process_user),
    )
```

#### Best Practices
- **Guard at the top**: Handle all invalid cases immediately at function entry
- **One return per guard**: Each validation failure should return immediately
- **Avoid else**: Never use else after a return statement
- **Keep guards simple**: Guard conditions should be easy to understand
- **Order by likelihood**: Check most likely failure conditions first

### Naming Conventions
- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `SCREAMING_SNAKE_CASE`
- **Private members**: Prefix with single underscore `_private`
- **Descriptive names**: Use clear, descriptive names over abbreviations

### Function Design
- **Small functions**: Keep functions focused and under 20 lines when possible
- **Container return types**: EVERY function must return a container type
- **Pure by default**: Pure functions return Result or Maybe
- **Impure functions**: Must return IO, IOResult, or FutureResult
- **Early returns with containers**: Use guard clauses with container short-circuiting to avoid nested conditionals
- **No else statements**: Prefer early returns over else branches to keep code flat and readable
- **Parameter validation**: Return Failure instead of raising exceptions
- **Composition-friendly**: Design functions to work with bind/map/flow
- **Single responsibility**: Each function does one thing in the pipeline

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
- **No docstrings**: Do not include any docstrings at all
- **Minimal comments**: Only add comments where complex, non-obvious logic requires explanation
- **Self-documenting code**: Prefer clear naming and structure over comments
- **Avoid obvious comments**: Never comment what the code clearly does (e.g., `# increment counter`)
- **Complex logic only**: Reserve comments for algorithms, workarounds, or business logic that isn't immediately clear

### Comment Examples
```python
# WRONG - Obvious comment
counter += 1  # increment counter

# WRONG - Comment explains what, not why
user_id = data.get("id")  # get user id from data

# CORRECT - Explains non-obvious business logic
# Todoist API returns priority 1 as highest, but we display 4 as highest
display_priority = 5 - api_priority

# CORRECT - Explains complex algorithm
# Using binary search with early termination when variance < threshold
# to optimize for datasets with clustered values
```

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
- **Imperative code**: Convert any try/catch blocks to functional containers
- **Missing containers**: Add container types to functions that can fail
- **Complex nesting**: Flatten nested conditionals using railway patterns
- **Side effects**: Isolate side effects in IO containers
- **Technical debt**: Prioritize converting exception-based code to containers

### Refactoring Process
- **Container introduction**: Start by wrapping existing functions with `@safe`
- **Pipeline creation**: Convert sequential operations to `flow()` pipelines
- **Error type definition**: Replace exceptions with explicit error types
- **Composition improvement**: Break large functions into composable units
- **Test adaptation**: Update tests to work with container types

### Tests
- **Necessary tests**: DO NOT test libraries functionality, only the business logic the code introduces
- **Prefer integration tests**: prefer integration tests over unit tests. Avoid mocks as much as possible
