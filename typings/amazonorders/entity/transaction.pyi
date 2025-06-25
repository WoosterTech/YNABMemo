from datetime import date
from typing import override

from amazonorders.conf import AmazonOrdersConfig
from amazonorders.entity.parsable import Parsable
from bs4 import Tag

__copyright__: str = "Copyright (c) 2024-2025 Alex Laird"
__license__: str = "MIT"

class Transaction(Parsable):
    completed_date: date
    payment_method: str
    grand_total: float
    is_refund: bool
    order_number: str
    order_details_link: str
    seller: str
    """
    An Amazon Transaction.
    """
    def __init__(
        self, parsed: Tag, config: AmazonOrdersConfig, completed_date: date
    ) -> None: ...
    @override
    def __repr__(self) -> str: ...
    @override
    def __str__(self) -> str: ...
