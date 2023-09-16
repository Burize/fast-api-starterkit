from dataclasses import dataclass
from typing import List
from uuid import UUID

from sqlalchemy import select

from store.models import Order
from core.database import Session


@dataclass
class OrderView:
    id: UUID
    number: int
    description: str


class OrderQueries:
    async def get_user_orders(self, user_id: UUID, limit: int = 10) -> List[OrderView]:
        query = select(Order).filter(Order.user_id == user_id).order_by(Order.number).limit(limit)
        result = await Session.scalars(query)

        return [OrderView(id=order.id, number=order.number, description=order.description) for order in result]
