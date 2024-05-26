from typing import Any


class CSS:
    def __init__(self, **attrs):
        self.__dict__["_attrs"] = attrs

    def __setattr__(self, key: str, value: Any):
        self.__dict__["_attrs"][key.replace("_", "-")] = value

    def __getattr__(self, key: str) -> Any:
        return self.__dict__["_attrs"].get(key.replace("_", "-"))

    def __delattr__(self, key: str):
        del self.__dict__["_attrs"][key.replace("_", "-")]

    def set(self, **attrs) -> "CSS":
        self.__dict__["_attrs"].update(attrs)
        return self

    def __str__(self) -> str:
        return "; ".join([f"{key}: {value}" for key, value in self.__dict__["_attrs"].items()])
