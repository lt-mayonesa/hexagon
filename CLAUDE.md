# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Hexagon is a Python CLI framework that enables teams to build custom command-line tools configured via YAML. It allows users to create team CLIs with tools, environments, and actions without writing code, while also supporting custom Python modules, shell scripts, and plugins for extensibility.

## Development Commands

### Setup
```bash
# Install pipenv if not already installed
pip install pipenv

# Start a pipenv shell
pipenv shell

# Install dependencies (including dev dependencies)
pipenv install --dev

# Run hexagon directly from source
python -m hexagon
```

### Testing

```bash
# Run unit tests
pytest -svv tests/

# Run E2E tests (requires translation files to be built first)
.github/scripts/i18n/build.sh
pytest -svv tests_e2e/

# Run a single test file
pytest -svv tests/path/to/test_file.py

# Run a single test
pytest -svv tests/path/to/test_file.py::test_function_name

# Run tests in parallel (faster)
pytest -svv tests/ -n auto
```

### Code Quality

```bash
# Format code with black (runs automatically on commit)
black hexagon tests tests_e2e

# Run linter
flake8 hexagon

# Check types (if applicable)
pytest -svv tests/runtime/test_typing.py
```

### Internationalization (i18n)

```bash
# Build translation files (required before running E2E tests)
.github/scripts/i18n/build.sh

# Translation files are in locales/ directory
# - locales/hexagon.pot: Template file
# - locales/en/LC_MESSAGES/*.mo: Compiled English translations
# - locales/es/LC_MESSAGES/*.mo: Compiled Spanish translations
```

### Website (Docusaurus)

```bash
cd website

# Start development server
npm start

# Build static site
npm run build

# Serve built site locally
npm run serve
```

## Architecture

### Core Components

**Domain Layer** (`hexagon/domain/`)
- `tool/__init__.py`: Tool type definitions (ActionTool, GroupTool, FunctionTool)
  - `ToolType` enum: misc, web, shell, hexagon, group, function, separator
  - Tools can have actions (strings/lists), functions (callables), or nested tools (groups)
- `cli.py`: CLI configuration model (name, command, entrypoint, plugins, options)
- `env.py`: Environment definitions for multi-environment deployments
- `hexagon_error.py`: Custom exception types

**Runtime Layer** (`hexagon/runtime/`)
- `singletons.py`: Global instances of configuration, tools, envs, and options
  - Configuration reads from `HEXAGON_CONFIG_FILE` env var or defaults to `app.yaml`
- `configuration.py`: YAML config loading and tool registration
  - Handles recursive group loading from separate YAML files
  - Manages custom tools directory registration
  - Provides default hexagon tools (save-alias, replay, create-tool)
- `execute/action.py`: Tool execution engine
  - Executes Python modules, shell scripts (.sh, .js), or inline commands
  - Python modules: Looks for action in custom_tools_dir first, then hexagon.actions.external
  - Scripts: Relative to project path, executed via interpreter (sh/node)
  - Inline: Direct shell command execution
  - All actions receive: tool, env, env_args, cli_args
- `execute/tool.py`: Tool selection and orchestration
- `plugins/__init__.py`: Plugin loading system
  - Imports all Python files from configured plugin directories
  - Each plugin must have a `main()` function
- `update/`: CLI and hexagon version checking and update mechanisms

**Actions** (`hexagon/actions/`)
- `internal/`: Built-in hexagon tools
  - `install_cli.py`: Install a custom CLI from YAML config
  - `create_new_tool.py`: Interactive tool creation wizard
  - `save_new_alias.py`: Save command aliases
  - `replay.py`: Re-run last command
- `external/`: Extensible action library (can be extended by users)
  - `open_link.py`: Open URLs in browser
- `__templates/`: Templates for creating custom tools

**Support Layer** (`hexagon/support/`)
- `output/printer/`: Rich terminal output with theming (default, disabled, result_only)
- `input/`: User input handling (InquirerPy prompts, argument parsing)
- `hooks/`: Event hooks (HexagonHooks.start, HexagonHooks.end)
- `storage/`: User data persistence
- `tracer.py`: Command tracing for replay functionality

### Configuration Flow

1. `hexagon/__main__.py` initializes from `singletons.py`
2. `Configuration.init_config()` reads YAML (app.yaml by default)
3. Tools are recursively loaded, including group tools from separate files
4. Custom tools directory is registered to Python path if specified
5. Plugins are collected and imported
6. Tool selection happens via interactive menu or command-line args
7. `execute_action()` dispatches to appropriate execution method

### Tool Execution Patterns

**Python Module Actions:**
- Module path: `action: "module.submodule"` or `action: "hexagon.actions.external.action_name"`
- Must have `main(tool, env, env_args, cli_args)` function
- Optional `Args` class for custom argument parsing (inherits from ToolArgs)
- Can import from custom_tools_dir or hexagon.actions

**Shell Script Actions:**
- Path relative to project: `action: "scripts/deploy.sh"`
- Supported extensions: .sh (sh), .js (node)
- Receives args as command-line parameters
- Environment variables: HEXAGON_EXECUTION_TOOL (JSON), HEXAGON_EXECUTION_ENV (JSON)

**Inline Command Actions:**
- Direct shell commands: `action: "echo Hello World"`
- Can use format strings: `{tool.name}`, `{env.name}`, `{env_args}`, `{cli_args}`

**Action Lists:**
- Multiple commands: `action: ["cmd1", "cmd2", "cmd3"]`
- Joined with newlines for execution

### Custom Tools Directory

Set `custom_tools_dir` in YAML to enable:
1. Custom Python modules that can be imported by tools
2. Relative script paths for shell/node actions
3. Custom tool templates

The directory is added to Python sys.path, allowing tools to import custom modules.

### Plugin System

Plugins extend hexagon functionality:
1. Specify plugin paths in `cli.plugins` list (relative to project path)
2. Each plugin file must have a `main()` function
3. Plugins are imported at startup before tool execution
4. Use plugins for: custom hooks, tool registration, environment setup

## Testing Conventions

### Test Structure (from .windsurfrules)

**Naming:**
- File pattern: `tests/*.py` or `tests_e2e/__specs/*.py`
- Function format: `test_[function_being_tested]_[current_scenario_under_test]()`
- Use BDD-style docstrings:
  ```python
  """
  Given [precondition]
  When [action]
  Then [expected outcome]
  """
  ```
- Use "And" for multiple steps
- End each step with a period

**Implementation:**
- Use pytest (not unittest)
- Direct assert statements (not assertEqual)
- Named parameters for clarity
- One behavior per test
- Always check existing tests for project conventions before writing new ones

**E2E Tests:**
- Located in `tests_e2e/__specs/`
- Use test resources from `tests_e2e/__test_resources/`
- Two categories: `_parallel/` (can run concurrently) and `_sequential/` (must run in order)
- Must build i18n files before running: `.github/scripts/i18n/build.sh`
- New features should include E2E test suites

**E2E Testing Best Practices:**
- **CRITICAL: Status/loader messages are NOT visible in E2E test output**
  - Messages like "Checking for...", "Loading...", "Updating..." are hidden by the status display
  - Only check for actual result messages: "New version available", "already up to date", "Update cancelled", etc.
  - This is the #1 reason E2E tests fail when first written - don't check for status messages!

- **Study existing patterns FIRST**: Before writing new E2E tests, find and examine similar existing tests
  - Look for tests that do similar operations (e.g., check existing update tests before writing new update tests)
  - Understand what messages are actually visible vs. what gets hidden
  - Copy helper function patterns (e.g., `_write_last_check()` for simulating previous checks, `_prepare()` for git repo setup)
  - Understand environment variable patterns for mocking behavior
  - Don't guess - verify what works by looking at passing tests

- **Output matching techniques**:
  - Use `discard_until_first_match=True` to skip variable initialization output
  - Match on multiple word fragments rather than exact phrases: `["New", "version available"]` works better than exact strings
  - Be aware of dynamic content: CLI name, version numbers, branch names get interpolated into messages

- **Test resource management**:
  - Keep mock files minimal - trim large files like CHANGELOGs to only essential content
  - Use realistic version numbers in mock files (e.g., 0.61.0, not 999.0.0)
  - Structure test resources to match what the test needs:
    - Remove app.yml when testing bare hexagon mode (initial setup tools)
    - Include app.yml when testing CLI project mode (default tools)
  - Copy test resources from similar existing tests rather than creating from scratch

- **Test execution context**:
  - Understand the test framework automatically sets certain env vars
  - Tests in `_parallel/` can run concurrently - ensure no shared state
  - Test directory is temporary - use `spec.test_dir` to get the path
  - The test framework may automatically set `HEXAGON_CONFIG_FILE` if app.yml exists

## Code Style

- **Formatting:** Black is used for auto-formatting (target Python 3.7+)
  - Do not manually change formatting; black runs after commits
  - Line length: 88 characters
- **Linting:** flake8 with configuration in `.flake8`
  - Max complexity: 10
  - Ignores: E203, E501, W503, B950, W605 (for black compatibility)
- **Python Version:** Requires Python >=3.9
- **Built-in i18n:** Use `_("msg.key")` for translatable strings
  - Translations are in `locales/` directory
  - The `_` function is available as a builtin throughout the codebase

## Key Environment Variables

- `HEXAGON_CONFIG_FILE`: Path to YAML config (default: `app.yaml`)
- `HEXAGON_THEME`: UI theme (default, disabled, result_only)
- `HEXAGON_EXECUTION_TOOL`: JSON tool object passed to shell actions
- `HEXAGON_EXECUTION_ENV`: JSON environment object passed to shell actions

## Common Patterns

### Creating a New Tool Action

1. Add Python module in custom_tools_dir or hexagon/actions/external/
2. Implement `main(tool, env, env_args, cli_args)` function
3. Optional: Define `Args` class for custom argument parsing
4. Reference in YAML: `action: "module.name"` or `action: "hexagon.actions.external.name"`

### Working with Environments

Tools can specify different values per environment:
```yaml
tools:
  - name: deploy
    type: shell
    envs:
      dev: "./deploy.sh dev-server"
      prod: "./deploy.sh prod-server"
    action: # fallback if env not specified
```

### Tool Groups

Organize related tools:
```yaml
tools:
  - name: database
    type: group
    tools: "tools/database.yaml"  # or inline list
```

External group files should have `tools: []` at root level.

## Development Workflow Best Practices

### Code Quality & Formatting
- **CRITICAL: Always run Black before committing**: Black formatting is mandatory for ALL Python code changes, not just tests. Run it before every commit:
  ```bash
  pipenv run black hexagon tests tests_e2e
  ```
- After running black, if you already committed, amend the commit rather than creating a new one
- Build i18n files before running E2E tests: `.github/scripts/i18n/build.sh`

### Implementation Strategy
- **Commit working code first, then refactor**: Don't try to do everything in one large commit
  - Get the feature working
  - Commit it
  - Then refactor to improve code quality in a separate commit
- **Prefer using existing files/modules over creating new ones**:
  - When implementing new functionality, check if there's already a file where it belongs
  - Example: Use `shared.py` for shared helper functions rather than creating a new `helpers.py`
- **E2E tests are part of the feature, not optional**:
  - New features should include E2E tests in the same PR
  - Don't defer E2E tests to a follow-up PR

### Understanding Architecture
- **Study the architecture before implementing**:
  - Understand the distinction between initial setup config vs default tools
  - Initial setup tools: Available when running bare `hexagon` without config (e.g., `install`, `update-hexagon`)
  - Default tools: Available when running a CLI project with app.yml (e.g., `save-alias`, `replay`, `update-cli`)
- **Follow existing patterns**:
  - If other similar code doesn't check for something, your new code shouldn't either
  - Example: If other default tools don't check `if self.__config`, your new default tool shouldn't either
- **Simplify logic**:
  - Remove unnecessary conditional checks
  - Trust the architecture - if you're in `__defaults`, there's always a config

### Impact Analysis
- **When adding new built-in tools, update existing E2E tests**:
  - Tests that check tool counts will need updates
  - Search for patterns like "4/4", "5/5" in test expectations
  - Update both the count and the list of expected tools

### Code Organization & Refactoring
- **DRY (Don't Repeat Yourself)**:
  - When you notice duplicate code between automatic and manual flows, extract shared helper functions
  - Place helpers in the most appropriate existing file (e.g., `shared.py` for update-related helpers)
- **Refactoring approach**:
  - Implement the feature with its own logic first
  - Once it works, identify duplication with existing code
  - Extract shared helpers
  - Refactor both old and new code to use the helpers
  - Keep refactoring commits separate from feature commits

### User Interaction & Feedback
- **Ask clarifying questions early**: When requirements are ambiguous, ask questions upfront rather than making assumptions
- **Take user feedback literally**: When user points to an existing file or pattern, use it
- **Iterate based on feedback**: User may catch issues in multiple rounds - that's normal and expected
  - First round: Architecture issues
  - Second round: Logic simplification
  - Third round: Code quality (formatting, tests)

### Testing Best Practices Beyond E2E
- **CRITICAL: Test overrides can hide bugs**
  - Environment variables like `HEXAGON_CHANGELOG_FILE_PATH_TEST_OVERRIDE` bypass production code paths
  - Always ensure unit tests cover BOTH the override path AND the production path
  - Example: The `RemoteChangelogFile` decode bug was missed because all tests used the local file override
  - When adding test overrides, create specific unit tests for the production code path
- **Test all code branches**:
  - If code has an `if/else` for test vs production, test BOTH branches
  - Mock external dependencies (like `urlopen`) to test production paths in isolation
  - Don't rely solely on E2E tests with overrides
- **When adding test helpers**:
  - Document what code path the helper bypasses
  - Create corresponding unit tests for the bypassed path
  - Example: If adding `SOME_API_OVERRIDE`, create unit tests that mock the real API

### Git & CI Workflow
- **Before pushing**:
  - Run black on all Python changes
  - Run unit tests: `pytest -svv tests/`
  - Build i18n: `.github/scripts/i18n/build.sh`
  - Run E2E tests: `pytest -svv tests_e2e/`
- **CI failures to watch for**:
  - Black formatting: Always run black before committing
  - Flake8 linting: May need to exclude generated files in `.flake8`
  - i18n validation: Remove fuzzy markers, ensure translations are complete
  - E2E test failures: Often related to tool count changes or output expectations
- **Amending commits**: Use `git commit --amend --no-edit` for small fixes like formatting, then `git push --force-with-lease`
- **Empty commits for CI re-runs**: If tests are flaky and unrelated to changes, create an empty commit to trigger CI again
