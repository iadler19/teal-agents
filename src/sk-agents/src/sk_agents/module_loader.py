import importlib.util
import sys
from typing import Any


class ModuleLoader:
    @staticmethod
    def _parse_module_name(types_module: str) -> str:
        return types_module.split("/")[-1].split(".")[0]

    @staticmethod
    def load_module(module: str) -> Any:
        module_name = ModuleLoader._parse_module_name(module)
        spec = importlib.util.spec_from_file_location(module_name, module)
        custom_module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = custom_module
        spec.loader.exec_module(custom_module)
        return custom_module
