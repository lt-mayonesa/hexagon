def to_readable_name(key: str) -> str:
    """
    Converts prompt_toolkit key names to human-readable names (for more info see https://python-prompt-toolkit.readthedocs.io/en/master/pages/advanced_topics/key_bindings.html#list-of-special-keys)
    ie:
        - "c-p" -> "CTRL+P"
        - "c-x" -> "CTRL+X"
        - "enter" -> "ENTER"
        - etc

    :param key: the key to convert
    :return: the human-readable key
    """
    if key.startswith("c-"):
        return "CTRL+" + key[2:].upper()
    elif key.startswith("s-"):
        return "SHIFT+" + key[2:].upper()
    elif key.startswith("a-"):
        return "ALT+" + key[2:].upper()
    elif key in ["escape", "enter", "space", "tab", "backspace"]:
        return key.upper()
    elif key.startswith("up"):
        return "↑"
    elif key.startswith("down"):
        return "↓"
    elif key.startswith("left"):
        return "←"
    elif key.startswith("right"):
        return "→"
    else:
        raise ValueError(f"Unknown key {key}")
