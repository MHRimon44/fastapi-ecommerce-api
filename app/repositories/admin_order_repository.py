from typing import List, Optional, Tuple

from sqlmodel import Session, select

from app.models.customer_model import Customer
from app.models.order_model import Order, OrderItem
from app.models.product_model import Product


class AdminOrderRepository:
    def list_orders(
        self,
        session: Session,
        search: Optional[str],
        order_status_filter: Optional[str],
        customer_id: Optional[int],
        page: int,
        page_size: int,
    ) -> Tuple[List[Order], int]:
        statement = select(Order)

        if search:
            search_pattern = f"%{search}%"
            statement = statement.where(Order.order_no.ilike(search_pattern))

        if order_status_filter:
            statement = statement.where(Order.order_status == order_status_filter)

        if customer_id is not None:
            statement = statement.where(Order.customer_id == customer_id)

        statement = statement.order_by(Order.order_id.desc())

        all_matching_orders = session.exec(statement).all()
        total = len(all_matching_orders)

        offset = (page - 1) * page_size

        paginated_statement = statement.offset(offset).limit(page_size)
        orders = session.exec(paginated_statement).all()

        return orders, total

    def get_order_by_id(
        self,
        session: Session,
        order_id: int,
    ) -> Optional[Order]:
        statement = select(Order).where(Order.order_id == order_id)
        return session.exec(statement).first()

    def get_customer_by_id(
        self,
        session: Session,
        customer_id: int,
    ) -> Optional[Customer]:
        statement = select(Customer).where(Customer.customer_id == customer_id)
        return session.exec(statement).first()

    def list_order_items(
        self,
        session: Session,
        order_id: int,
    ) -> List[OrderItem]:
        statement = select(OrderItem).where(OrderItem.order_id == order_id)
        return session.exec(statement).all()

    def get_products_by_ids(
        self,
        session: Session,
        product_ids: List[int],
    ) -> List[Product]:
        if not product_ids:
            return []

        statement = select(Product).where(Product.product_id.in_(product_ids))
        return session.exec(statement).all()

    def update_order_status(
        self,
        session: Session,
        order: Order,
        order_status: str,
    ) -> Order:
        order.order_status = order_status

        session.add(order)
        session.commit()
        session.refresh(order)

        return order


admin_order_repository = AdminOrderRepository()
