"""
Data models for peer-to-peer communication
"""

from typing import Literal
from pydantic import BaseModel


class TextMessage(BaseModel):
    """Text message model"""
    type: Literal["text"] = "text"
    sender: str
    content: str


class FileMessage(BaseModel):
    """File transfer message model"""
    type: Literal["file"] = "file"
    sender: str
    filename: str
    filesize: int
    content: bytes  # File data


class ControlMessage(BaseModel):
    """Control messages for connection management"""
    type: Literal["connect", "disconnect", "accept", "reject"] = "connect"
    sender: str
    message: str = ""


class PeerInfo(BaseModel):
    """Peer information from STUN server"""
    username: str
    ip: str
    port: int
