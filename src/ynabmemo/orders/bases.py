import abc
from datetime import date
from decimal import Decimal
from enum import StrEnum
from typing import Any, ClassVar, Generic, Self, TypedDict, TypeVar

from attrmagic import ClassBase, SimpleRoot
from pydantic import AnyUrl, ValidationError, model_validator


class ParsableBase(ClassBase, abc.ABC):
    @classmethod
    @abc.abstractmethod
    def _parse_object(cls, obj: Any) -> dict[str, Any]:  # pyright: ignore[reportExplicitAny, reportAny]
        """Parse the object into a dictionary."""
        raise NotImplementedError("Subclasses must implement this method.")


class ObjectTypes(StrEnum):
    """Enumeration of object types."""

    ITEM = "item"
    ORDER = "order"
    TRANSACTION = "transaction"


class ObjectAttrMap(ClassBase, abc.ABC):
    vendor: ClassVar[str]
    object_type: ClassVar[ObjectTypes]


class OrderCreator(ClassBase, abc.ABC):
    """Interface for creating orders."""

    attrmap: ClassVar[ObjectAttrMap]

    @property
    def vendor(self) -> str:
        """Return the vendor name."""
        return self.attrmap.vendor

    def create_order(
        self,
        order_obj: object,
    ) -> "OrderBase":
        """Create an order from the given order object."""
        raise NotImplementedError("Subclasses must implement this method.")


ItemObject = TypeVar("ItemObject", bound=object)


class ItemBase(ParsableBase, Generic[ItemObject], abc.ABC):
    id: str | None = None
    description: str
    price: Decimal
    quantity: int | None = None
    taxable: bool | None = None
    link: AnyUrl | None = None

    @classmethod
    def create_item(cls, item_obj: ItemObject) -> Self:
        """Create an item from the given item object."""
        return cls.model_validate(item_obj)


ItemT = TypeVar("ItemT", bound=ClassBase)


class ItemBaseRoot(SimpleRoot[ItemT], Generic[ItemT], abc.ABC):
    """Root class for a collection of items."""


OrderObject = TypeVar("OrderObject", bound=object)


class OrderBase(ParsableBase, Generic[OrderObject, ItemT], abc.ABC):
    id: str
    record_date: date
    total: Decimal
    link: AnyUrl | None = None
    items: ItemBaseRoot[ItemT] | None = None

    @model_validator(mode="before")
    @classmethod
    def validate_order(cls, data: Any) -> Any:  # pyright: ignore[reportExplicitAny, reportAny]
        """Validate the order data before creating an instance."""
        try:
            return cls._parse_object(data)
        except ValidationError:
            return data  # pyright: ignore[reportAny]


OrderT = TypeVar("OrderT", bound=ClassBase)


class OrderBaseRoot(SimpleRoot[OrderT], Generic[OrderT], abc.ABC):
    """Root class for a collection of orders."""

    pass


class Transaction(ClassBase, abc.ABC):
    id: str
    record_date: date
    amount: Decimal
    order_id: str | None = None

    @property
    def is_ordered(self) -> bool:
        """Check if the transaction is associated with an order."""
        return self.order_id is not None
