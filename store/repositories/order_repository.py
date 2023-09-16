from store.models import Order
from core.database import Session


class OrderRepository:
    async def save(self, order: Order):
        Session.add(order)
        await Session.flush()
