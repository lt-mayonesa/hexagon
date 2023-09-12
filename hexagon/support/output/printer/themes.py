import os
from dataclasses import dataclass, fields, field


@dataclass
class PromptsTheme:
    questionmark: str = "#e5c07b"
    answer: str = "#61afef"
    input: str = "#98c379"
    question: str = ""
    instruction: str = "#6bb4b4"
    long_instruction: str = "orange"
    pointer: str = "#61afef"
    checkbox: str = "#98c379"
    separator: str = ""
    skipped: str = "#5c6370"
    validator: str = ""
    marker: str = ""
    fuzzy_prompt: str = "#c678dd"
    fuzzy_info: str = "#56b6c2"
    fuzzy_border: str = "#4b5263"
    fuzzy_match: str = "#c678dd"


@dataclass
class LoggingTheme:
    show_colors: bool = True
    result_only: bool = False
    prompt_border: bool = True
    start: str = ""
    border: str = ""
    border_result: str = ""
    process_out: str = ""
    process_in: str = ""
    finish: str = ""
    prompts: PromptsTheme = field(default_factory=PromptsTheme)

    def __getitem__(self, item: str):
        if item.startswith("prompts."):
            return (
                getattr(self.prompts, item.replace("prompts.", ""))
                if self.show_colors
                else ""
            )
        return getattr(self, item)


def load_theme(theme: str):
    __themes = {
        "default": LoggingTheme(
            start="╭╼ ",
            border="│ ",
            border_result="├ ",
            process_out="┆",
            process_in="┆",
            finish="╰╼ ",
        ),
        "no_border": LoggingTheme(
            prompt_border=False,
            start="╭╼ ",
            border="│ ",
            border_result="├ ",
            process_out="┆",
            process_in="┆",
            finish="╰╼ ",
        ),
        "disabled": LoggingTheme(show_colors=False, prompt_border=False),
        "result_only": LoggingTheme(
            result_only=True, show_colors=False, prompt_border=False
        ),
    }

    t = __themes[theme]

    for f in fields(t.prompts):
        n = f"INQUIRERPY_STYLE_{f.name.upper()}"
        os.environ[n] = os.getenv(n, t[f"prompts.{f.name}"])

    return t
