from datetime import date
from unittest.mock import MagicMock

import pytest
from amazonorders.entity.item import Item as AmazonItemEntity
from amazonorders.entity.order import Order as AmazonOrderEntity

from ynabmemo.amazon.models import AmazonOrder


@pytest.fixture
def mock_amazon_order() -> AmazonOrderEntity:
    order = MagicMock(spec=AmazonOrderEntity)

    order.order_number = "123"
    order.order_placed_date = date(2022, 1, 1)
    order.grand_total = 100.00
    order.order_details_link = None
    order.items = []

    return order


@pytest.fixture
def mock_amazon_item():
    item = MagicMock(spec=AmazonItemEntity)

    item.id = "item123"
    item.description = "Test Item"
    item.price = 10.00
    item.taxable = True

    return item


def test_create_order(mock_amazon_order: AmazonOrderEntity) -> None:
    """Test creating an Amazon order from an order object."""
    order = AmazonOrder.model_validate(mock_amazon_order)

    assert order.id == "123"
    assert order.record_date == date(2022, 1, 1)
    assert order.total == 100.00
    assert order.link is None  # Assuming link is not set in the mock
