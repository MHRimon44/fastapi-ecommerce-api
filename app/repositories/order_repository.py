from datetime import datetime
from typing import Dict, List, Optional, Tuple

from sqlalchemy import func
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

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

        order.sub_total = total_amount
        order.discount_amount = 0
        order.total_amount = total_amount
        session.add(order)

        session.commit()
        session.refresh(order)

        for item in created_items:
            session.refresh(item)

        return order, created_items

    def get_by_id(
        self,
        session: Session,
        order_id: int,
    ) -> Optional[Order]:
        statement = (
            select(Order)
            .where(Order.order_id == order_id)
            .options(selectinload(Order.items))
        )

        return session.exec(statement).first()

    def list_orders(
        self,
        session: Session,
        customer_id: Optional[int],
        status: Optional[str],
        limit: int,
        offset: int,
    ) -> Tuple[int, List[Order]]:
        statement = select(Order)
        count_statement = select(func.count()).select_from(Order)

        if customer_id is not None:
            statement = statement.where(Order.customer_id == customer_id)
            count_statement = count_statement.where(Order.customer_id == customer_id)

        if status:
            statement = statement.where(Order.order_status == status)
            count_statement = count_statement.where(Order.order_status == status)

        statement = statement.order_by(Order.created_at.desc())

        total = session.exec(count_statement).one()

        statement = statement.offset(offset).limit(limit)

        orders = session.exec(statement).all()

        return total, orders


order_repository = OrderRepository()