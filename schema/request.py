from typing import Optional

from pydantic import BaseModel, Field


class ParseRequest(BaseModel):
    """
    Input model for parse requests.
    """

    command_output: str = Field(..., description="Raw CLI output to parse")
    command_name: Optional[str] = Field(
        None, description="Optional command name: e.g., 'show ip route'"
    )
    user_instruction: Optional[str] = Field(
        None, description="Optional additional instruction for the parser"
    )
