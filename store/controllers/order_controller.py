from dataclasses import dataclass
from http import HTTPStatus
from typing import Annotated
from typing import List
from typing import Optional
from uuid import UUID

from fastapi import Query
from injector import inject

from core.api import APIRouter
from core.api import controller
from core.dependencies import get_user_id
from store.models import Order
from store.queries import OrderQueries
from store.repositories import OrderRepository

router = APIRouter()


@dataclass
class CreateOrderDTO:
    description: str


@dataclass
class OrderDTO:
    id: UUID
    number: int
    description: str


@controller
class OrderController:
    @inject
    def __init__(
        self,
        order_repository: OrderRepository,
        order_queries: OrderQueries,
    ):
        self._order_repository = order_repository
        self._order_queries = order_queries

    @router.get('')
    async def list(
        self,
        user_id=get_user_id,
        limit: Annotated[Optional[int], Query()] = 10,
    ) -> List[OrderDTO]:
        orders = await self._order_queries.get_user_orders(user_id, limit=limit)
        return [OrderDTO(id=order.id, number=order.number, description=order.description) for order in orders]

    @router.post('',  status_code=HTTPStatus.CREATED)
    async def create(self, dto: CreateOrderDTO, user_id=get_user_id) -> OrderDTO:
        order = Order(user_id=user_id, description=dto.description)
        await self._order_repository.save(order)

        return OrderDTO(id=order.id, description=order.description, number=order.number)
