---
sidebar_position: 3
---

# Internationalization

Hexagon supports internationalization (i18n), allowing you to make your CLI accessible to users in different languages. This guide explains how to set up and use internationalization in your CLI.

## Understanding Internationalization in Hexagon

Hexagon uses the standard Python `gettext` module for internationalization. This allows you to translate your CLI's messages into different languages.

## Translation Files

Hexagon looks for translation files in the `locales` directory of your project. The directory structure follows the standard `gettext` format:

```
locales/
  ├── en/
  │   └── LC_MESSAGES/
  │       └── hexagon.mo
  ├── es/
  │   └── LC_MESSAGES/
  │       └── hexagon.mo
  └── fr/
      └── LC_MESSAGES/
          └── hexagon.mo
```

Each language has its own directory named with the language code (e.g., `en` for English, `es` for Spanish). Inside each language directory, there's an `LC_MESSAGES` directory containing the compiled message catalog (`hexagon.mo`).

## Creating Translation Files

To create translation files for your CLI:

1. Extract translatable strings from your code into a `.pot` file
2. Create `.po` files for each language
3. Compile `.po` files into `.mo` files

### Extracting Strings

Use the `xgettext` tool to extract translatable strings from your Python code:

```bash
xgettext -d hexagon -o hexagon.pot your_code.py
```

### Creating Language-Specific Files

Create a `.po` file for each language based on the `.pot` file:

```bash
msginit -i hexagon.pot -o locales/es/LC_MESSAGES/hexagon.po -l es
```

### Compiling Message Catalogs

Compile the `.po` files into `.mo` files:

```bash
msgfmt -o locales/es/LC_MESSAGES/hexagon.mo locales/es/LC_MESSAGES/hexagon.po
```

## Marking Strings for Translation

In your Python code, mark strings for translation using the `_` function:

```python
from hexagon.support.output.printer import _

def my_function():
    # Mark a string for translation
    message = _("Hello, World!")
    print(message)
```

## Setting the Language

Hexagon uses the system's locale settings to determine which language to use. You can override this by setting the `LANG` environment variable:

```bash
LANG=es_ES.UTF-8 mycli
```

## Example: Adding Spanish Translation

Here's an example of adding Spanish translation to your CLI:

1. Create the directory structure:

```bash
mkdir -p locales/es/LC_MESSAGES
```

2. Create a `.po` file with translations:

```
# locales/es/LC_MESSAGES/hexagon.po
msgid ""
msgstr ""
"Project-Id-Version: hexagon\n"
"POT-Creation-Date: 2023-01-01 12:00+0000\n"
"PO-Revision-Date: 2023-01-01 12:00+0000\n"
"Last-Translator: Your Name <your.email@example.com>\n"
"Language-Team: Spanish\n"
"Language: es\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"

msgid "Hello, World!"
msgstr "¡Hola, Mundo!"

msgid "Goodbye!"
msgstr "¡Adiós!"
```

3. Compile the `.po` file into a `.mo` file:

```bash
msgfmt -o locales/es/LC_MESSAGES/hexagon.mo locales/es/LC_MESSAGES/hexagon.po
```

4. Test the translation:

```bash
LANG=es_ES.UTF-8 mycli
```

## Best Practices

- **Plan for Internationalization**: Design your CLI with internationalization in mind from the start
- **Use the `_` Function**: Mark all user-facing strings for translation
- **Provide Context**: Add comments for translators to explain the context of strings
- **Test Translations**: Test your CLI with different languages to ensure everything works correctly
- **Keep Translations Updated**: Update translations when you add or change strings in your code

## Next Steps

Now that you've learned about the advanced features of Hexagon, check out the [API Reference](../api) for detailed information about Hexagon's components.
