from typing import Any, Dict, List, Optional

from amazonorders.conf import AmazonOrdersConfig
from amazonorders.forms import AuthForm
from amazonorders.util import AmazonSessionResponse
from requests import Response, Session

__copyright__: str = "Copyright (c) 2024-2025 Alex Laird"
__license__: str = "MIT"
logger = ...

class IODefault:
    """
    Handles input/output from the application. By default, this uses console commands, but
    this class exists so that it can be overridden when constructing an :class:`AmazonSession`
    if input/output should be handled another way.
    """
    def echo(self, msg: str, **kwargs: Any) -> None:
        """
        Echo a message to the console.

        :param msg: The data to send to output.
        :param kwargs: Unused by the default implementation.
        """
        ...

    def prompt(self, msg: str, type: Optional[Any] = ..., **kwargs: Any) -> Any:
        """
        Prompt to the console for user input.

        :param msg: The data to use as the input prompt.
        :param type: Unused by the default implementation.
        :param kwargs: Unused by the default implementation.
        :return: The user input result.
        """
        ...

class AmazonSession:
    config: AmazonOrdersConfig
    auth_forms: list[AuthForm]
    username: str | None = None
    password: str | None = None
    otp_secret_key: str | None = None
    debug: bool
    io: IODefault
    session: Session
    is_authenticated: bool = False
    def __init__(
        self,
        username: str | None = None,
        password: str | None = None,
        debug: bool = ...,
        io: IODefault = ...,
        config: AmazonOrdersConfig | None = None,
        auth_forms: list[AuthForm] | None = None,
        otp_secret_key: str | None = None,
    ) -> None: ...
    def request(
        self, method: str, url: str, persist_cookies: bool = ..., **kwargs: Any
    ) -> AmazonSessionResponse: ...
    def get(self, url: str, **kwargs: Any) -> AmazonSessionResponse: ...
    def post(self, url: str, **kwargs: Any) -> AmazonSessionResponse: ...
    def auth_cookies_stored(self) -> bool: ...
    def login(self) -> None: ...
    def logout(self) -> None: ...
    def build_response_error(self, response: Response) -> str: ...
    def check_response(
        self,
        amazon_session_response: AmazonSessionResponse,
        meta: Optional[Dict[str, Any]] = ...,
    ) -> None:
        """
        Check the response to ensure it appears to be returning a valid response, and that it is still authenticated.
        We detect if authentication has expired by checking for redirects to the login page. Raise an error if the
        response is not going to contain the requested data for parsing.

        :param amazon_session_response: The response to check.
        :param meta: Metadata to be added to any errors raised.
        """
        ...
