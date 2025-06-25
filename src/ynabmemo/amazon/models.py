from decimal import Decimal
from typing import Any, override

from amazonorders.entity.item import Item as AmazonItemEntity
from amazonorders.entity.order import Order as AmazonOrderEntity

from ynabmemo.orders.bases import ItemBase, OrderBase, OrderBaseRoot


class AmazonItem(ItemBase[AmazonItemEntity]):
    """Amazon item model."""

    @override
    @classmethod
    def _parse_object(cls, obj: AmazonItemEntity) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        price = obj.price or "0.00"
        return {
            "description": obj.title,
            "price": Decimal(price),
            "link": obj.link,
            "quantity": obj.quantity,
        }


class AmazonOrder(OrderBase[AmazonOrderEntity, AmazonItem]):
    """Amazon order model."""

    @override
    @classmethod
    def _parse_object(cls, obj: AmazonOrderEntity) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny]
        return {
            "id": obj.order_number,
            "record_date": obj.order_placed_date,
            "total": Decimal(obj.grand_total),
            "link": obj.order_details_link,
            "items": obj.items,
        }


class AmazonOrders(OrderBaseRoot[AmazonOrder]):
    """Collection of Amazon orders."""
