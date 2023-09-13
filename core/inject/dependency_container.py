from typing import Callable
from typing import Dict
from typing import Type
from typing import Union

from fastapi import Depends

Provider = Union[Callable, object]


class DependencyContainer:
    _configuration: Dict[Type, Provider] = dict()

    @classmethod
    def add(cls, dependency: Type, provider: Provider):
        cls._configuration[dependency] = provider

    @classmethod
    def get_annotation(cls, dependency: Type) -> Provider:
        provider = cls._configuration.get(dependency, None)
        if not provider:
            return Depends()
        if callable(provider):
            return Depends(provider)
        return provider
