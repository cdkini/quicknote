import re
from types import ModuleType
from typing import Dict


class TemplateEngine:
    def __init__(self, modules: Dict[str, ModuleType]) -> None:
        self._modules = modules

    def eval(self, text: str) -> str:
        matches = re.finditer(r"\${(.+)}", text)
        for match in matches:
            pattern = match.group(0)
            expr = match.group(1)
            interpolated = str(eval(expr, self._modules))

            text = text.replace(pattern, interpolated, 1)

        return text
