import inspect

from fastapi import Depends


def controller(cls):
    methods_with_init = inspect.getmembers(cls, inspect.isfunction)
    methods = (method for name , method  in methods_with_init if name != '__init__' )
    for method in methods:
        signature = inspect.signature(method)
        parameters: list[inspect.Parameter] = list(signature.parameters.values())

        self = parameters[0]
        injected_self = self.replace(default=Depends(cls))

        new_parameters = [parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY) for parameter in parameters[1:]]
        new_signature = signature.replace(parameters=[injected_self, *new_parameters])
        setattr(method, "__signature__", new_signature)

    return cls
