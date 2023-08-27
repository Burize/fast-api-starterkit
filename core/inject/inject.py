import inspect

from fastapi import Depends


def inject(init):
    signature = inspect.signature(init)
    parameters: list[inspect.Parameter] = list(signature.parameters.values())
    self = parameters[0]

    new_parameters = [parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY, default=Depends()) for parameter in parameters[1:]]
    new_signature = signature.replace(parameters=[self, *new_parameters])
    setattr(init, "__signature__", new_signature)

    return init
