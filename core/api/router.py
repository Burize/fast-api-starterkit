from fastapi import APIRouter as FastAPIRouter
from fastapi import Depends

from core.dependencies.authoroized import authorized


class APIRouter(FastAPIRouter):
    def get(
        self,
        path: str,
        no_authetication: bool = False,
        **kwargs,
    ):
        return self._base_route(method='get', path=path, no_authetication=no_authetication, **kwargs)

    def post(
        self,
        path: str,
        no_authetication: bool = False,
        **kwargs,
    ):
        return self._base_route(method='post', path=path, no_authetication=no_authetication, **kwargs)

    def put(
        self,
        path: str,
        no_authetication: bool = False,
        **kwargs,
    ):
        return self._base_route(method='put', path=path, no_authetication=no_authetication, **kwargs)

    def delete(
        self,
        path: str,
        no_authetication: bool = False,
        **kwargs,
    ):
        return self._base_route(method='delete', path=path, no_authetication=no_authetication, **kwargs)


    def _base_route(
        self,
        method: str,
        path: str,
        no_authetication: bool = False,
        **kwargs,
    ):
        auth_dependencies = [] if no_authetication else [Depends(authorized)]
        args_dependencies = kwargs.pop('dependencies', [])
        dependencies = auth_dependencies + args_dependencies
        return getattr(super(),method)(path=path, dependencies=dependencies, **kwargs)
