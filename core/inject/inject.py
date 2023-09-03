import inspect
from core.inject.dependency_container import DependencyContainer


def inject(init):
    signature = inspect.signature(init)
    parameters: list[inspect.Parameter] = list(signature.parameters.values())
    self = parameters[0]

    new_parameters = [parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY, default=DependencyContainer.get_annotation(parameter.annotation)) for parameter in parameters[1:]]
    new_signature = signature.replace(parameters=[self, *new_parameters])
    setattr(init, "__signature__", new_signature)

    return init
