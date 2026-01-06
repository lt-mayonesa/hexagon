---
sidebar_position: 4
---

# Prompting System

Hexagon provides a powerful and flexible prompting system that allows you to create interactive command-line interfaces with rich input capabilities. This guide explains how the prompting system works and how to use it in your custom tools.

## Overview

Hexagon's prompting system leverages two key Python libraries:

1. **InquirerPy**: Provides the interactive prompts with features like autocomplete, validation, and different input types
2. **Pydantic**: Handles type validation and conversion of user input

The system allows you to define command-line arguments with type hints, which Hexagon uses to determine what kind of prompt to show and how to validate the input.

## Defining Arguments

Arguments are defined using a class that inherits from `ToolArgs` and uses type hints to specify the expected data types:

```python
from hexagon.support.input.args import ToolArgs, PositionalArg, OptionalArg, Arg

class Args(ToolArgs):
    # Required positional argument
    name: PositionalArg[str] = Arg(
        None, prompt_message="Enter your name"
    )
    
    # Optional argument with default value
    age: OptionalArg[int] = Arg(
        30, prompt_message="Enter your age"
    )
    
    # Optional argument with custom prompt suggestions
    country: OptionalArg[str] = Arg(
        "USA", 
        prompt_message="Select your country",
        prompt_suggestions=["USA", "Canada", "Mexico", "Other"]
    )
```

### Argument Types

Hexagon supports two main types of arguments:

1. **PositionalArg**: Required arguments that can be provided positionally on the command line
2. **OptionalArg**: Optional arguments that have default values

## The Arg Function

The `Arg` function is used to configure how arguments are prompted and validated. It accepts several parameters:

```python
Arg(
    default,                # Default value for the argument
    *,
    alias=None,             # Alternative name for the argument
    title=None,             # Title displayed in help text
    description=None,       # Description displayed in help text
    prompt_default=None,    # Default value shown in the prompt
    prompt_message=None,    # Message displayed when prompting
    prompt_instruction=None,# Additional instructions for the prompt
    prompt_suggestions=None,# Suggestions for text input autocomplete
    choices=None,           # Options for selection prompts
    searchable=False,       # Whether the prompt supports searching
    # Additional validation parameters
)
```

## Prompt Types

Hexagon automatically selects the appropriate prompt type based on the argument's type hint:

### Text Input

For `str` type arguments, Hexagon displays a text input prompt:

```python
name: PositionalArg[str] = Arg(None, prompt_message="Enter your name")
```

This will display a simple text input field where users can type their response.

### Text Input with Autocomplete

For text inputs where you want to provide autocomplete suggestions, use the `prompt_suggestions` parameter:

```python
username: PositionalArg[str] = Arg(
    None, 
    prompt_message="Enter a username",
    prompt_suggestions=["admin", "user", "guest", "developer"]
)
```

When typing, users can press `CTRL+SPACE` to see and select from available suggestions that match their input. Unlike `choices`, these are just suggestions and users can still enter any text they want.

### Numeric Input

For `int` and `float` type arguments, Hexagon displays a numeric input prompt with validation:

```python
age: OptionalArg[int] = Arg(30, prompt_message="Enter your age")
height: OptionalArg[float] = Arg(1.75, prompt_message="Enter your height in meters")
```

These prompts will validate that the input can be converted to the specified numeric type.

### Boolean Input

For `bool` type arguments, Hexagon displays a yes/no prompt:

```python
confirm: OptionalArg[bool] = Arg(True, prompt_message="Do you want to proceed?")
```

Users can select Yes or No, which will be converted to `True` or `False`.

### List Selection

For arguments with a list of choices, Hexagon displays a selection prompt:

```python
country: OptionalArg[str] = Arg(
    "USA", 
    prompt_message="Select your country",
    choices=["USA", "Canada", "Mexico", "Other"]
)
```

Users can navigate through the options and select one. The `choices` parameter defines the available options in the selection list.

### Multiple Selection

For `List` type arguments, Hexagon displays a checkbox prompt:

```python
from typing import List

# List of strings
selected_items: OptionalArg[List[str]] = Arg(
    [],
    prompt_message="Select items",
    choices=["Item 1", "Item 2", "Item 3", "Item 4"]
)

# List of integers
selected_numbers: OptionalArg[List[int]] = Arg(
    [],
    prompt_message="Select port numbers",
    choices=[8000, 8080, 3000, 5000]
)

# List without predefined choices (user enters values)
tags: OptionalArg[List[str]] = Arg(
    [],
    prompt_message="Enter tags (comma-separated)"
)
```

Users can select multiple items using the space bar to toggle selections. The `choices` parameter defines the available options in the checkbox list.

### Path Selection

Hexagon supports three path-related types with autocomplete:

```python
from pathlib import Path
from hexagon.support.input.args import FilePath, DirectoryPath

# Generic path (files or directories)
file_path: OptionalArg[Path] = Arg(
    None,
    prompt_message="Select a file or directory"
)

# File path only (validates that path is a file)
config_file: OptionalArg[FilePath] = Arg(
    None,
    prompt_message="Select a configuration file"
)

# Directory path only (validates that path is a directory)
output_dir: OptionalArg[DirectoryPath] = Arg(
    None,
    prompt_message="Select output directory"
)
```

All path prompts provide autocomplete for filesystem paths. `FilePath` and `DirectoryPath` add validation to ensure the path is the correct type.

### Enum Selection

For `Enum` type arguments, Hexagon displays a selection prompt with the enum values:

```python
from enum import Enum

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"

color: OptionalArg[Color] = Arg(
    Color.RED, 
    prompt_message="Select a color"
)
```

Users can select one of the enum values.

## Supported Argument Types

Hexagon supports a wide range of argument types:

| Type | Prompt Style | Example | Notes |
|------|--------------|---------|-------|
| `str` | Text input | `name: PositionalArg[str]` | Basic text input |
| `int` | Numeric input | `age: OptionalArg[int]` | Validates integer input |
| `float` | Numeric input | `height: OptionalArg[float]` | Validates float input |
| `bool` | Yes/No prompt | `confirm: OptionalArg[bool]` | Returns True/False |
| `List[str]` | Multi-select/text | `tags: OptionalArg[List[str]]` | Multiple strings |
| `List[int]` | Multi-select | `ports: OptionalArg[List[int]]` | Multiple integers |
| `Path` | Path autocomplete | `path: OptionalArg[Path]` | File or directory |
| `FilePath` | Path autocomplete | `file: OptionalArg[FilePath]` | File only (validated) |
| `DirectoryPath` | Path autocomplete | `dir: OptionalArg[DirectoryPath]` | Directory only (validated) |
| `Enum` | Selection prompt | `color: OptionalArg[Color]` | Enum values as choices |
| Custom Pydantic models | Varies | `config: OptionalArg[Config]` | Complex nested structures |

## Complete Arg() Parameters Reference

The `Arg()` function supports the following parameters:

```python
Arg(
    default,                     # Required: Default value for the argument
    *,
    # CLI Configuration
    alias: str = None,           # Short flag alias (e.g., "v" for --verbose)
    description: str = None,     # Help text description
    title: str = None,           # Title shown in help

    # Prompting Configuration
    prompt_message: str = None,  # Message shown when prompting user
    prompt_default: Any = None,  # Default value shown in prompt (can differ from default)
    prompt_instruction: str = None,  # Additional instructions below prompt
    prompt_suggestions: Union[List, Callable] = None,  # Autocomplete suggestions
    searchable: bool = False,    # Enable fuzzy search for choices

    # Selection Configuration
    choices: Union[List, Callable] = None,  # Available options for selection prompts
)
```

### Parameter Details

| Parameter | Type | Description | Works With |
|-----------|------|-------------|------------|
| `default` | `Any` | Default value if not provided | All types |
| `alias` | `str` | Short flag (e.g., `-v` for `--verbose`) | OptionalArg only |
| `description` | `str` | Help text shown in `--help` | All types |
| `title` | `str` | Title in help output | All types |
| `prompt_message` | `str` | Question shown to user | All types |
| `prompt_default` | `Any` | Default in prompt (overrides `default` for display) | All types |
| `prompt_instruction` | `str` | Additional instructions below prompt | All types |
| `prompt_suggestions` | `List` or `Callable` | Autocomplete suggestions (NOT choices) | Text inputs |
| `searchable` | `bool` | Enable fuzzy search filtering | Selection prompts |
| `choices` | `List` or `Callable` | Options for selection (restricts input) | All types |

### Choices vs Suggestions

- **`choices`**: Restricts input to only the provided options (selection prompt)
- **`prompt_suggestions`**: Provides autocomplete hints but allows any input (text prompt with autocomplete)

```python
# Choices: User MUST select from list
environment: OptionalArg[str] = Arg(
    "dev",
    choices=["dev", "staging", "prod"]  # User cannot enter other values
)

# Suggestions: User CAN enter any value
username: OptionalArg[str] = Arg(
    None,
    prompt_suggestions=["admin", "user", "guest"]  # Hints, but any value allowed
)
```

## Accessing Argument Values

When working with arguments in your `main()` function, always use the `.value` property:

```python
def main(tool, env, env_args, cli_args: Args):
    # Correct: Use .value to get the actual value
    name = cli_args.name.value

    # Check if value exists before prompting
    if cli_args.name.value is None:
        cli_args.name.prompt()

    # Now use the value
    log.info(f"Hello, {cli_args.name.value}!")
```

**Why `.value`?** The argument object (`cli_args.name`) contains metadata, validation logic, and prompting methods. The `.value` property returns the actual user input.

## Using Prompts in Custom Tools

When implementing a custom tool, you define the arguments class and then access the values in your `main` function:

```python
from hexagon.support.output.printer import log
from hexagon.support.input.args import ToolArgs, PositionalArg, OptionalArg, Arg

class Args(ToolArgs):
    name: PositionalArg[str] = Arg(
        None, prompt_message="Enter your name"
    )
    age: OptionalArg[int] = Arg(
        30, prompt_message="Enter your age"
    )

def main(tool, env, env_args, cli_args):
    # Only prompt if values weren't provided as command-line arguments
    if not cli_args.name.value:
        cli_args.name.prompt()
    
    if not cli_args.age.value:
        cli_args.age.prompt()
    
    # Access the values directly from cli_args
    log.info(f"Name: {cli_args.name.value}")
    log.info(f"Age: {cli_args.age.value}")
    
    # Return results
    return [
        f"Name: {cli_args.name.value}",
        f"Age: {cli_args.age.value}"
    ]
```

## Advanced Prompting Features

### Conditional Prompting

You can implement conditional prompting based on previous inputs:

```python
from hexagon.support.input.args import ToolArgs, PositionalArg, OptionalArg, Arg

class Args(ToolArgs):
    has_car: OptionalArg[bool] = Arg(
        False, prompt_message="Do you have a car?"
    )
    car_brand: OptionalArg[str] = Arg(
        None, prompt_message="What brand is your car?"
    )

def main(tool, env, env_args, cli_args):
    if not cli_args.has_car.value:
        cli_args.has_car.prompt()
    
    # Only prompt for car brand if user has a car
    if cli_args.has_car.value and not cli_args.car_brand.value:
        cli_args.car_brand.prompt()
    
    # Process inputs
    if cli_args.has_car.value:
        log.info(f"You have a {cli_args.car_brand.value} car")
    else:
        log.info("You don't have a car")
```

### Dynamic Choices and Suggestions

You can provide dynamic choices or suggestions based on runtime data. Both `choices` and `prompt_suggestions` can accept a function that returns a list:

```python
def get_available_projects():
    # This could fetch data from an API or local storage
    return ["Project A", "Project B", "Project C"]

class Args(ToolArgs):
    # For selection prompts, use choices
    project_select: PositionalArg[str] = Arg(
        None, 
        prompt_message="Select a project",
        choices=get_available_projects
    )
    
    # For text input with autocomplete, use prompt_suggestions
    project_name: PositionalArg[str] = Arg(
        None, 
        prompt_message="Enter a project name",
        prompt_suggestions=get_available_projects
    )
```

The function will be called when the prompt is displayed, ensuring that the choices or suggestions are up-to-date.

### Searchable Prompts

For long lists of choices, you can enable searching:

```python
class Args(ToolArgs):
    country: PositionalArg[str] = Arg(
        None, 
        prompt_message="Select your country",
        choices=["Afghanistan", "Albania", "Algeria", /* ... */],
        searchable=True
    )
```

When the `searchable` parameter is set to `True`, users can type to filter the available choices. This is particularly useful for long lists of options.

### Custom Validation

You can add custom validation to ensure inputs meet specific requirements:

```python
from pydantic import validator

class Args(ToolArgs):
    email: PositionalArg[str] = Arg(
        None, prompt_message="Enter your email"
    )
    
    @validator("email")
    def validate_email(cls, v):
        if "@" not in v:
            raise ValueError("Invalid email address")
        return v
```

## Keyboard Shortcuts and Hints

Hexagon provides helpful keyboard shortcuts and hints for different prompt types:

### Text Input
- `CTRL+SPACE`: Autocomplete (if available)
- `ENTER`: Confirm input
- `CTRL+C`: Cancel
- `CTRL+Z`: Skip (use default value)

### Selection Prompts
- `↑/↓` or `CTRL+P/CTRL+N`: Navigate options
- `ENTER`: Confirm selection
- `CTRL+C`: Cancel

### Multiple Selection (Checkbox)
- `SPACE`: Toggle selection
- `CTRL+I`: Toggle and move down
- `SHIFT+TAB`: Toggle and move up
- `CTRL+R` or `ALT+R`: Toggle all
- `ENTER`: Confirm selections

## Examples from Hexagon Core

Hexagon's core tools provide excellent examples of how to use the prompting system effectively:

- `hexagon/actions/internal/create_new_tool.py`: Demonstrates complex prompting with multiple argument types
- `hexagon/actions/internal/install_cli.py`: Shows path selection and validation

## Best Practices

1. **Clear Prompt Messages**: Provide clear and concise prompt messages
2. **Appropriate Defaults**: Set sensible default values when possible
3. **Conditional Prompting**: Only prompt for information that's relevant based on previous inputs
4. **Check Before Prompting**: Always check if a value was provided via command line before prompting
5. **Validation**: Use appropriate type hints and validators to ensure data integrity
6. **Suggestions**: Provide suggestions when the set of valid inputs is known
7. **Searchable**: Enable searching for long lists of options

## Next Steps

Learn how to use [Hooks](hooks) to extend your CLI's functionality further.
