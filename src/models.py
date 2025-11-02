from typing import Any, Dict, List, Literal, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field


class TextPart(BaseModel):
    kind: Literal["text"] = "text"
    text: str


class DataPart(BaseModel):
    kind: Literal["data"] = "data"
    data: List[Dict[str, Any]]


class Message(BaseModel):
    role: Literal["user", "agent"]
    parts: List[Dict[str, Any]]
    messageId: str = Field(default_factory=lambda: str(uuid4()))
    kind: Optional[Literal["message"]] = "message"


class TaskStatus(BaseModel):
    state: Literal["submitted", "working", "completed", "failed", "canceled"]
    timestamp: Optional[str] = None


class Artifact(BaseModel):
    artifactId: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    parts: List[TextPart]


class Task(BaseModel):
    id: str
    contextId: Optional[str] = None
    status: TaskStatus
    artifacts: List[Artifact] = []
    history: List[Message] = []
    kind: Literal["task"] = "task"
    metadata: Dict[str, Any] = {}


class JSONRPCRequest(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    method: str
    params: Dict[str, Any]
    id: Union[str, int, None] = None


class JSONRPCResponse(BaseModel):
    jsonrpc: Literal["2.0"] = "2.0"
    id: Union[str, int, None]
    result: Optional[Task] = None
    error: Optional[Dict[str, Any]] = None


class BlogContent(BaseModel):
    """Extracted blog post content"""

    url: str
    title: str
    content: str
    excerpt: str


class SocialPost(BaseModel):
    """Generated social media post"""

    platform: str
    content: str


class ProcessingRequest(BaseModel):
    """Internal processing request"""

    blog_url: str
    platforms: List[str]
    task_id: str
