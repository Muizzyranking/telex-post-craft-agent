import re
from typing import List, Optional

from app.models import Message


class MessageParser:
    """Parse message from telex a2a and extract blog URL.
    
    Always generates content for LinkedIn and Twitter platforms regardless of message content.
    """

    @classmethod
    def extract_blog_url_and_platforms(cls, message: Message):
        """Extract blog URL from message and return fixed platforms.
        
        Args:
            message: Message object containing blog URL
            
        Returns:
            Tuple of (blog_url, ["linkedin", "twitter"])
        """
        text_parts: List[str] = []

        for part in message.parts:
            part_dict = part if isinstance(part, dict) else part.model_dump()
            kind = part_dict.get("kind")
            
            if kind == "text":
                text = part_dict.get("text", "")
                if not text.startswith("<") and "assist you" not in text.lower():
                    text_parts.append(text)
            elif kind == "data":
                # Handle data parts that contain text content
                data_items = part_dict.get("data", [])
                for item in data_items:
                    if isinstance(item, dict) and item.get("kind") == "text":
                        text = item.get("text", "")
                        if not text.startswith("<") and "assist you" not in text.lower():
                            text_parts.append(text)

        if not text_parts:
            raise ValueError("No text parts found in the message")

        full_text = " ".join(text_parts)
        url = cls._extract_blog_url(full_text)
        if not url:
            raise ValueError("No valid blog URL found in the message")

        platforms = ["linkedin", "twitter"]
        return url, platforms

    @classmethod
    def _extract_blog_url(cls, text: str) -> Optional[str]:
        url_pattern = r'https?://[^\s<>"]+'
        matches = re.findall(url_pattern, text)

        if matches:
            return matches[0]

        return None


