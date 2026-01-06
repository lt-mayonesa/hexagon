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

## Documentation Structure

The Hexagon website uses Docusaurus with a manually configured sidebar structure. Understanding this structure is critical when adding or updating documentation.

### Directory Structure

```
website/
├── docs/                    # Documentation pages
│   ├── intro.md            # Landing page for docs
│   ├── api.md              # API reference index
│   ├── getting-started/    # Getting started guides
│   ├── guides/             # User guides
│   ├── advanced/           # Advanced topics
│   └── api/                # API reference pages
│       ├── cli.md
│       ├── tool.md
│       ├── env.md
│       ├── runtime-options.md
│       ├── built-in-tools.md
│       ├── actions/        # Action API reference
│       └── support/        # Support module reference
├── blog/                   # Blog posts (tutorials, releases)
├── sidebars.ts             # Sidebar configuration (MUST be updated)
└── docusaurus.config.ts    # Site configuration
```

### Documentation Categories

Documentation is organized into clear categories:

**Configuration APIs:**
- Core configuration objects (CLI, Tool, Env, Runtime Options)
- Used to configure CLIs via YAML

**Built-in Features:**
- Built-in tools (install, get-json-schema, update-hexagon, save-alias, replay, etc.)
- Features available out-of-the-box

**Action APIs:**
- How tools execute (web actions, shell actions, action execution strategy)
- The 3-tier resolution: scripts → modules → inline commands

**Support Modules:**
- Utilities for building CLIs (output, hooks, storage)
- Used by custom tools and plugins

**Advanced Topics:**
- Custom tools, prompting, plugins, internationalization
- Deep dives and extensibility

### Adding New Documentation

**CRITICAL: Always update `sidebars.ts` when adding new documentation pages!** Docusaurus uses manual sidebar configuration, so new pages won't appear in navigation unless explicitly added.

1. **Create the documentation file** in the appropriate directory:
   ```markdown
   ---
   sidebar_position: 5
   ---

   # Page Title

   Content here...
   ```

2. **Update `website/sidebars.ts`** to include the new page:
   ```typescript
   const sidebars: SidebarsConfig = {
     tutorialSidebar: [
       'intro',
       {
         type: 'category',
         label: 'Guides',
         items: [
           'guides/existing-guide',
           'guides/new-guide',  // ADD HERE
         ],
       },
     ],
   };
   ```

3. **Verify with dev server**:
   ```bash
   cd website
   npm start
   # Check that the new page appears in navigation
   ```

### Blog Posts vs Documentation

**Use blog posts for:**
- Tutorials with step-by-step instructions
- Release announcements
- Feature spotlights
- Time-sensitive content

**Use documentation for:**
- API reference
- Configuration guides
- Conceptual explanations
- Reference material

**Blog post frontmatter:**
```markdown
---
slug: building-custom-tool
title: "Tutorial: Building a Custom Tool"
authors: [joaco]
tags: [tutorial, custom-tools, python]
---

# Building a Custom Tool

Introduction paragraph...

<!-- truncate -->

Rest of content...
```

**Documentation frontmatter:**
```markdown
---
sidebar_position: 5
---

# Page Title
```

### Cross-Referencing

**Within documentation:**
```markdown
See [Custom Tools](../advanced/custom-tools) for details.
```

**From docs to blog:**
```markdown
Check out our [Building a Custom Tool](/blog/building-custom-tool) tutorial.
```

**From blog to docs:**
```markdown
See the [Custom Tools reference](/docs/advanced/custom-tools) for the complete API.
```

### Documentation Best Practices

**When updating documentation:**
1. **Fix incorrect information first** - API accuracy is critical
2. **Add missing documentation** - Ensure all features are documented
3. **Organize for discoverability** - Clear categories and navigation
4. **Cross-reference thoroughly** - Link related topics
5. **Update all references** - When moving/renaming pages, update all links
6. **Test with dev server** - Verify navigation and links work
7. **Check for broken links** - Docusaurus will warn about broken internal links

**Documentation workflow:**
1. Identify gaps or errors in current documentation
2. Plan the documentation structure (categories, pages, organization)
3. Create or update documentation pages
4. Update `sidebars.ts` with new pages
5. Update cross-references (intro.md, api.md, etc.)
6. Test with local dev server
7. Commit changes

**Writing style:**
- Clear and concise
- Include code examples
- Use proper markdown formatting
- Add "Key topics" or "What's covered" sections
- Link to related documentation
- Provide troubleshooting tips where relevant

### Large Documentation Updates

When doing comprehensive documentation updates (fixing multiple issues, adding new sections, reorganizing):

**Use a phased approach:**

1. **Phase A - Discovery**: Understand the current state and requirements
   - Read existing documentation
   - Identify errors, gaps, and inconsistencies
   - Use Task tool with multiple code-explorer agents in parallel to understand codebase

2. **Phase B - Planning**: Design the documentation structure
   - List all issues found
   - Ask user for scope and priorities
   - Plan categories and organization
   - Get user approval before proceeding

3. **Phase C - Foundation Fixes**: Fix critical errors first
   - Correct API inaccuracies (wrong function signatures, incorrect behavior)
   - Update outdated information
   - Remove conflicting examples

4. **Phase D - API Completeness**: Add missing documentation
   - Document all undocumented features
   - Complete partial documentation
   - Add missing parameters and options

5. **Phase E - New Comprehensive Guides**: Create new documentation
   - Add deep-dive explanations
   - Create troubleshooting guides
   - Add complete reference pages

6. **Phase F - Navigation**: Update documentation structure
   - Update intro/index pages
   - Update sidebars.ts
   - Update cross-references
   - Convert tutorials to blog posts if appropriate

7. **Phase G - Quality Review**: Final verification
   - Test with local dev server
   - Verify all links work
   - Check navigation is clear
   - Remove any obsolete files

**Commit strategy:**
- Commit after each major phase or after 4-7 related files
- Let user review and commit before continuing
- Keep commits focused on related changes

**Tools and patterns:**
- Use multiple Task tools with code-explorer agents in parallel for efficient codebase understanding
- Use TodoWrite to track progress through phases
- Test frequently with local dev server (`cd website && npm start`)

### Production Build Verification

**CRITICAL: Always run a production build before considering documentation work complete.** The production build catches issues that the dev server doesn't:

1. **Run the production build:**
   ```bash
   cd website
   yarn build
   ```

2. **Common build issues and fixes:**

   **Broken links:**
   - Production build fails on broken internal links (dev server only warns)
   - Error message shows exact broken link and source page
   - Fix: Correct the relative path or use absolute paths from `/docs/`
   - Example: `../api/troubleshooting` should be `troubleshooting` when already in guides/

   **Missing blog tags:**
   - Blog posts can reference tags not defined in `blog/tags.yml`
   - Production build warns but continues (should be fixed)
   - Fix: Add new tags to `blog/tags.yml`:
     ```yaml
     new-tag:
       label: Display Name
       permalink: /tag-url
       description: Tag description
     ```

   **Missing pages in navigation:**
   - Pages won't appear in sidebar unless added to `sidebars.ts`
   - No build error, but users can't discover the pages
   - Fix: Update `sidebars.ts` with new page paths

3. **Verify the production build:**
   ```bash
   # Serve the production build locally
   yarn serve

   # In another terminal, verify key pages
   curl -I http://localhost:3000/hexagon/docs/intro
   curl -I http://localhost:3000/hexagon/docs/api
   # Should return HTTP 200
   ```

4. **Build checklist:**
   - [ ] Production build completes without errors
   - [ ] No broken link warnings
   - [ ] No missing tag warnings
   - [ ] Key pages accessible (docs, API, blog posts)
   - [ ] Navigation includes all new pages
   - [ ] Cross-references work correctly

**When to run production build:**
- Before committing documentation changes
- After adding new pages
- After updating navigation structure
- When converting tutorials to blog posts
- Before deploying to production

**Note:** The dev server (`npm start`) is great for rapid iteration but doesn't catch all issues. Always verify with a production build.

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
- **CRITICAL: Always run Black and Flake8 before wrapping up ANY change**: Code quality checks are mandatory for ALL code changes. Run these commands on the entire project before considering work complete:
  ```bash
  pipenv run black .
  pipenv run flake8 .
  ```
- This applies to:
  - Before committing code
  - Before pushing to CI
  - When wrapping up any bug fix or feature
  - After making any Python code changes
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
  - Run code quality checks: `pipenv run black .` and `pipenv run flake8 .`
  - Run unit tests: `pytest -svv tests/`
  - Build i18n: `.github/scripts/i18n/build.sh`
  - Run E2E tests: `pytest -svv tests_e2e/`
- **CI failures to watch for**:
  - Black formatting: Always run `black .` on entire project before committing
  - Flake8 linting: Always run `flake8 .` on entire project; may need to exclude generated files in `.flake8`
  - i18n validation: Remove fuzzy markers, ensure translations are complete
  - E2E test failures: Often related to tool count changes or output expectations
- **Amending commits**: Use `git commit --amend --no-edit` for small fixes like formatting, then `git push --force-with-lease`
- **Empty commits for CI re-runs**: If tests are flaky and unrelated to changes, create an empty commit to trigger CI again
