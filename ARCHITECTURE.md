## Core Architectural Principles

### 1. Modern Python Standards
- **Python 3.13+**: Targets the latest Python version for access to newest language features and performance improvements
- **Type Safety**: Strict type checking with Pyright to catch errors early and improve code reliability
- **Code Quality**: Comprehensive linting with Ruff covering style, complexity, security, and best practices

### 2. Simplified Dependency Management
- **uv**: Ultra-fast Python package manager that replaces pip, poetry, and pipenv
- **Lock File**: `uv.lock` ensures reproducible builds across different environments
- **Development Dependencies**: Separate dependency groups for clean separation of concerns

### 3. Developer Experience Focus
- **Single Command Setup**: `uv sync` installs all dependencies and creates virtual environment
- **Task Automation**: poethepoet (poe) tasks for common development workflows
- **Consistent Tooling**: All tools configured to work harmoniously together

## Configuration Management

### Centralized Configuration
All tool configuration is centralized in `pyproject.toml` following PEP 518 standards:

```toml
[tool.pyright]              # Type checking configuration
[tool.ruff]                 # Linting and formatting rules
[tool.poe.tasks]            # Task automation
```

### Pyright Configuration
- **Strict Mode**: `typeCheckingMode = "strict"` catches maximum number of type issues
- **Virtual Environment**: Automatically detects `.venv` for proper import resolution
- **Performance**: Configured for optimal IDE integration

### Ruff Configuration
- **Comprehensive Rules**: 15+ rule categories covering style, bugs, complexity, and security
- **Google Docstrings**: Standardized documentation format
- **Per-File Ignores**: Relaxed rules for test files
- **Target Version**: Python 3.12+ compatibility

## Development Workflow Integration

### Task Automation with poethepoet
```toml
[tool.poe.tasks]
run = "uv run --env-file .env -m src.python_starter_template" # Execute main application
lint = "ruff check"                                           # Run linter
typecheck = "pyright"                                         # Run type checker
format = "ruff format"                                        # Format code
test = "pytest -q"                                            # Run tests
```

## Code Quality and Standards

### Type Safety
- **Strict Type Checking**: All code must pass Pyright strict mode
- **Type Annotations**: Required for all public APIs
- **Gradual Typing**: Start with basic types, refine over time

### Code Style
- **Line Length**: 100 characters (modern standard for readability)
- **Import Sorting**: Automatic import organization with isort rules
- **Docstring Convention**: Google-style docstrings for consistency

### Linting Rules
The template enables comprehensive rule sets:
- **Error Prevention**: pycodestyle, pyflakes, bugbear
- **Code Modernization**: pyupgrade, simplify
- **Best Practices**: naming conventions, argument usage
- **Security**: exception handling, path operations
- **Documentation**: docstring requirements and style
