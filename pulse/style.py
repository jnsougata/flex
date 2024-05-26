from typing import Any


def _cssify(key: str) -> str:
    return key.replace("_", "-")


class CSS:
    def __init__(self, **attrs):
        self.__dict__["_attrs"] = {_cssify(key): value for key, value in attrs.items()}

    def __setattr__(self, key: str, value: Any):
        self.__dict__["_attrs"][_cssify(key)] = value

    def __getattr__(self, key: str) -> Any:
        return self.__dict__["_attrs"].get(_cssify(key))

    def __delattr__(self, key: str):
        del self.__dict__["_attrs"][_cssify(key)]

    def set(self, **attrs) -> "CSS":
        for key, value in attrs.items():
            self.__dict__["_attrs"][_cssify(key)] = value
        return self

    def __str__(self) -> str:
        return "; ".join([f"{key}: {value}" for key, value in self.__dict__["_attrs"].items()])
