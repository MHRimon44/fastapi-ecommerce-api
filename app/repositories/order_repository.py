from datetime import datetime
from typing import Dict, List, Tuple

from sqlmodel import Session

from app.models.order_model import Order, OrderItem


class OrderRepository:
    def create_order(
        self,
        session: Session,
        customer_id: int,
        order_items_data: List[Dict],
    ) -> Tuple[Order, List[OrderItem]]:
        order_no = "ORD-" + datetime.utcnow().strftime("%Y%m%d%H%M%S%f")

        order = Order(
            order_no=order_no,
            customer_id=customer_id,
            order_status="PLACED",
            total_amount=0,
        )

        session.add(order)
        session.flush()

        total_amount = 0
        created_items: List[OrderItem] = []

        for item_data in order_items_data:
            order_item = OrderItem(
                order_id=order.order_id,
                product_id=item_data["product_id"],
                quantity=item_data["quantity"],
                unit_price=item_data["unit_price"],
                line_total=item_data["line_total"],
            )

            total_amount += item_data["line_total"]

            session.add(order_item)
            created_items.append(order_item)

        order.total_amount = total_amount
        session.add(order)

        session.commit()
        session.refresh(order)

        for item in created_items:
            session.refresh(item)

        return order, created_items


order_repository = OrderRepository()