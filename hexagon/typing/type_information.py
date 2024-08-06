from typing import Any, get_args, Annotated, get_origin


class TypeInformation:
    def __init__(self, type_info: Any):
        self.type_info = type_info
        self.base_type = (
            get_args(type_info)[0] if get_origin(type_info) is Annotated else type_info
        )

    @property
    def is_bool(self):
        return self.base_type == bool

    @property
    def is_directory_path(self):
        return get_args(self.type_info)[1].path_type == "dir"
