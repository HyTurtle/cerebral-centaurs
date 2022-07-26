from enum import Enum
from typing import Union

from pydantic import BaseModel, validator


class TopicEnum(Enum):
    """Available topics types."""

    GAME = "GAME"
    DRAW = "DRAW"
    CHAT = "CHAT"
    ERROR = "ERROR"


class GameOperations(Enum):
    """Available game operations."""

    CREATE = "CREATE"
    JOIN = "JOIN"
    LEAVE = "LEAVE"
    END = "END"


class DrawOperations(Enum):
    """Available draw operations."""

    LINE = "LINE"
    RECT = "RECT"


class ChatOperations(Enum):
    """Available chat operations."""

    SAY = "SAY"


class ErrorOperations(Enum):
    """Available error operations."""

    BROADCAST = "BROADCAST"


class Topic(BaseModel):
    """Message's Topic consisting of type and operation."""

    type: TopicEnum
    operation: Union[GameOperations, DrawOperations, ChatOperations, ErrorOperations]

    class Config:
        use_enum_values = True

    @validator("operation")
    def operation_match_type(cls, v, values, **kwargs):
        """Verifies that provided operation is of a correct type."""
        allowed_operations = {
            TopicEnum.GAME.value: GameOperations,
            TopicEnum.DRAW.value: DrawOperations,
            TopicEnum.CHAT.value: ChatOperations,
            TopicEnum.ERROR.value: ErrorOperations,
        }
        expected_operations = allowed_operations.get(values.get("type"))
        if not expected_operations or v not in set(x.value for x in expected_operations):
            raise ValueError(f"Not allowed operations for {values.get('type')}")
        return v
