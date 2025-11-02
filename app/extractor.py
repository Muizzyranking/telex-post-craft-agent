import re
import httpx
from bs4 import BeautifulSoup

from app.models import BlogContent


class BlogExtractor:
    def __init__(self, timeout: int = 30):
        self.client = httpx.Client(timeout=timeout)

    def extract(self, url: str) -> BlogContent:
        """
        Extract blog post content from URL

        Args:
            url: Blog post URL

        Returns:
            BlogContent with title, content, and excerpt

        Raises:
            Exception: If extraction fails
        """
        try:
            # Fetch the webpage
            response = self.client.get(url, follow_redirects=True)
            response.raise_for_status()

            # Parse HTML
            soup = BeautifulSoup(response.text, "lxml")

            # Extract title
            title = self._extract_title(soup)

            # Extract main content
            content = self._extract_content(soup)

            # Generate excerpt
            excerpt = self._generate_excerpt(content)

            return BlogContent(
                url=url, title=title, content=content, excerpt=excerpt
            )

        except Exception as e:
            raise Exception(f"Failed to extract content from {url}: {str(e)}")

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract title from HTML"""
        title_selectors = [
            "h1",
            "title",
            '[property="og:title"]',
            '[name="twitter:title"]',
            ".post-title",
            ".entry-title",
            ".blog-title",
        ]

        for selector in title_selectors:
            element = soup.select_one(selector)
            if element:
                title = element.get_text(strip=True) or element.get("content", "")
                if title and len(title) > 0:
                    return str(title)

        return "Untitled"

    def _extract_content(self, soup: BeautifulSoup) -> str:
        """Extract main content from HTML"""
        for element in soup(
            ["script", "style", "nav", "footer", "header", "aside", "ads"]
        ):
            element.decompose()

        content_selectors = [
            "article",
            ".post-content",
            ".entry-content",
            ".blog-content",
            ".content",
            "main",
            ".post-body",
            ".entry-body",
        ]

        content_element = None
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                break

        if not content_element:
            content_element = soup.find("body") or soup

        text = content_element.get_text(separator="\n", strip=True)

        return self._clean_text(text)

    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        text = re.sub(r"\n\s*\n", "\n\n", text)
        text = re.sub(r" +", " ", text)
        return text.strip()

    def _generate_excerpt(self, content: str, max_length: int = 200) -> str:
        """Generate excerpt from content"""
        if not content:
            return ""

        content = re.sub(r"\s+", " ", content).strip()

        sentences = re.split(r"[.!?]+", content)
        excerpt = ""

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            if len(excerpt + sentence) <= max_length:
                excerpt += sentence + ". "
            else:
                break

        if not excerpt:
            excerpt = content[:max_length].rstrip()
            if len(content) > max_length:
                excerpt += "..."

        return excerpt.strip()

    def __del__(self):
        self.client.close()
