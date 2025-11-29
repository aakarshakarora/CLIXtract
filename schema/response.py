from typing import Any, Union

from pydantic import BaseModel


class ParseResponse(BaseModel):
    """
    Response model. parsed_output can be a dict, list, or a string (if error/raw).
    """

    parsed_output: Union[dict, list, str, None]
