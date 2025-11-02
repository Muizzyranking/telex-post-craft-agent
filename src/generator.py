from typing import List, Optional

from google.genai import Client, types

from src.config import settings
from src.models import BlogContent, SocialPost


class AIGenerator:
    """AI-powered content generator for social media posts.
    
    Always generates Twitter threads and comprehensive LinkedIn posts
    from blog content regardless of input platform specifications.
    """
    
    def __init__(self):
        self.gemini_client: Optional[Client] = None
        self._initialize_gemini()

    def _initialize_gemini(self):
        """Initialize Gemini AI client if API key is available"""
        if settings.GEMINI_API_KEY:
            try:
                self.gemini_client = Client(api_key=settings.GEMINI_API_KEY)
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
                self.gemini_client = None

    def generate_posts(
        self, blog_content: BlogContent, platforms: List[str] | str
    ) -> List[SocialPost]:
        """
        Generate social media posts for LinkedIn and Twitter.

        Args:
            blog_content: Extracted blog content
            platforms: List of platforms (always generates for LinkedIn and Twitter)

        Returns:
            List of SocialPost objects with Twitter threads and LinkedIn posts
        """

        posts: List[SocialPost] = []
        if not isinstance(platforms, List):
            platforms = [platforms]

        # Always generate for LinkedIn and Twitter
        target_platforms = ["linkedin", "twitter"]

        for platform in target_platforms:
            try:
                content = self._generate_platform_content(blog_content, platform)
                posts.append(SocialPost(platform=platform, content=content))
            except Exception as e:
                print(f"Failed to generate post for {platform}: {e}")
                posts.append(
                    SocialPost(
                        platform=platform,
                        content=f"Failed to generate content for {platform}",
                    )
                )

        return posts

    def _generat_with_gemini(self, prompt):
        if not self.gemini_client:
            raise Exception("Gemini client not initialized")

        response = self.gemini_client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7, max_output_tokens=500
            ),
        )
        if response is None or not response.text:
            raise Exception("No response from Gemini API")
        return response.text.strip()

    def _generate_platform_content(
        self, blog_content: BlogContent, platform: str
    ) -> str:
        prompt = self._create_prompt(blog_content, platform)
        if self.gemini_client:
            try:
                return self._generat_with_gemini(prompt)
            except Exception as e:
                print(f"⚠️ Gemini failed, trying Groq: {e}")

        raise Exception("No AI client available for content generation")

    def _create_prompt(self, blog_content: BlogContent, platform: str) -> str:
        """Create platform-specific prompts for social media content generation."""
        
        if platform == "twitter":
            prompt = f"""
            Create a Twitter thread based on the following blog content. The thread should tell a complete story and provide value to the reader.

            Blog Title: {blog_content.title}
            Blog Content: {blog_content.content}
            Blog URL: {blog_content.url}

            Requirements:
            - Create a multi-tweet thread (3-5 tweets)
            - Each tweet should be numbered as "1/n", "2/n", etc.
            - First tweet should hook the reader and introduce the topic
            - Middle tweets should develop the main points and insights
            - Final tweet should provide a call-to-action or key takeaway
            - Include relevant hashtags in the final tweet
            - Ensure smooth flow between tweets
            - Each tweet should be complete and make sense on its own
            - Use proper Twitter formatting with line breaks where needed

            Format the response as:
            Tweet 1/n: [content]
            Tweet 2/n: [content]
            Tweet 3/n: [content]
            ...

            Generate only the thread content without any additional text or explanations.
            """
        elif platform == "linkedin":
            prompt = f"""
            Create a comprehensive LinkedIn post based on the following blog content. This should be a full social media version that provides substantial value to professionals.

            Blog Title: {blog_content.title}
            Blog Content: {blog_content.content}
            Blog URL: {blog_content.url}

            Requirements:
            - Write a detailed, professional post (300-800 words)
            - Start with a strong hook that grabs attention
            - Include 3-5 key insights or takeaways from the blog
            - Add personal perspective or professional commentary
            - Use proper formatting with paragraphs and bullet points where appropriate
            - Include relevant hashtags at the end (3-5 hashtags)
            - End with a question to encourage engagement
            - Focus on providing real value and actionable insights
            - Maintain a professional but conversational tone
            - Include the original blog URL for reference

            Generate only the LinkedIn post content without any additional text or explanations.
            """
        else:
            prompt = f"""
            Create an engaging social media post for {platform} based on the following blog content.

            Blog Title: {blog_content.title}
            Blog Content: {blog_content.content}
            Blog URL: {blog_content.url}

            Generate appropriate content for the platform that provides value and engagement.
            """

        return prompt
