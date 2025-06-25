from ynabmemo.amazon.models import AmazonOrders
from amazonorders.session import AmazonSession


def fetch_orders(session: AmazonSession) -> AmazonOrders:
    """Fetches Amazon orders using the provided session.

    Args:
        session (AmazonSession): An authenticated Amazon session.

    Returns:
        AmazonOrders: A collection of Amazon orders.
    """
    if not session.is_authenticated:
        raise ValueError("Session must be authenticated.")
    
    return AmazonOrders(session)