from datetime import datetime
from typing import List
from uuid import uuid4

from src.extractor import BlogExtractor
from src.generator import AIGenerator
from src.message_parser import MessageParser
from src.models import (
    Artifact,
    JSONRPCRequest,
    JSONRPCResponse,
    Message,
    ProcessingRequest,
    Task,
    TaskStatus,
    TextPart,
)

from .models import BlogContent, SocialPost


class PostProcessor:
    """Main processor for blog to social media conversion.
    
    Always generates Twitter threads and comprehensive LinkedIn posts
    from blog content regardless of input platform specifications.
    """

    def __init__(self):
        self.extractor = BlogExtractor()
        self.generator = AIGenerator()

    def process(self, request: ProcessingRequest) -> List[SocialPost]:
        """
        Process blog URL and generate social media posts for LinkedIn and Twitter.

        Args:
            request: Processing request with URL (platforms are ignored, always generates for LinkedIn and Twitter)

        Returns:
            List of generated social posts (Twitter thread and LinkedIn post)
        """
        print(f"📝 Processing blog: {request.blog_url}")
        print("🎯 Generating for: LinkedIn and Twitter (always)")

        print("📥 Extracting blog content...")
        blog: BlogContent = self.extractor.extract(request.blog_url)
        print(f"✅ Extracted: {blog.title}")

        print("🤖 Generating social media posts...")
        posts: List[SocialPost] = self.generator.generate_posts(
            blog, request.platforms
        )
        print(f"✅ Generated {len(posts)} posts")

        return posts

    def format_response(self, posts: List[SocialPost]) -> str:
        """Format posts into response text"""
        lines: List[str] = ["# 🎉 Social Media Posts Generated\n"]

        platform_emojis = {
            "twitter": "🐦",
            "linkedin": "💼",
            "facebook": "👥",
            "instagram": "📸",
        }

        for post in posts:
            emoji = platform_emojis.get(post.platform, "📱")
            lines.append(f"## {emoji} {post.platform.title()}\n")
            lines.append(f"{post.content}\n")
            lines.append("---\n")

        return "\n".join(lines)

    async def handle_message_send(self, rpc_request: JSONRPCRequest):
        """
        Process incoming A2A messages

        Args:
            rpc_request: JSON-RPC request

        Returns:
            JSON-RPC response dict
        """
        params = rpc_request.params
        task_id = params.get("id", str(uuid4()))

        try:
            message_data = params.get("message", {})
            user_message = Message(**message_data)

            print("=" * 60)
            print(f"📨 New request - Task ID: {task_id}")

            blog_url, platforms = MessageParser.extract_blog_url_and_platforms(
                user_message
            )

            print(f"🔗 Blog URL: {blog_url}")
            print("🎯 Platforms: LinkedIn and Twitter (always generated)")

            # Process
            request = ProcessingRequest(
                blog_url=blog_url, platforms=platforms, task_id=task_id
            )

            posts = self.process(request)
            response_text = self.format_response(posts)

            print("✅ Processing completed")
            print("=" * 60)

            task = Task(
                id=task_id,
                contextId=str(uuid4()),
                status=TaskStatus(
                    state="completed", timestamp=datetime.utcnow().isoformat() + "Z"
                ),
                artifacts=[
                    Artifact(
                        name="social_media_posts",
                        parts=[TextPart(text=response_text)],
                    )
                ],
                history=[
                    user_message,
                    Message(
                        role="agent",
                        parts=[{"kind": "text", "text": response_text}],
                        messageId=str(uuid4()),
                    ),
                ],
            )

            return JSONRPCResponse(id=rpc_request.id, result=task).dict(
                exclude_none=True
            )

        except Exception as e:
            print("=" * 60)
            print(f"❌ Error processing request: {e}")
            print("=" * 60)

            # Create failed task response
            error_text = f"Failed to process blog post: {str(e)}"

            task = Task(
                id=task_id,
                contextId=str(uuid4()),
                status=TaskStatus(
                    state="failed", timestamp=datetime.utcnow().isoformat() + "Z"
                ),
                artifacts=[
                    Artifact(
                        name="error_response", parts=[TextPart(text=error_text)]
                    )
                ],
                history=[],
            )

            return JSONRPCResponse(id=rpc_request.id, result=task).dict(
                exclude_none=True
            )
