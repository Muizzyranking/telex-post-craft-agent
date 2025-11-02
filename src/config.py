from typing import List
from decouple import config


class Settings:
    """Configuration settings for PostCraft Agent"""
    
    # Server Configuration
    AGENT_URL: str = str(config("AGENT_URL", default="http://localhost:8000"))
    PORT: int = int(config("PORT", default=8000))

    # AI API Keys (at least one required)
    GEMINI_API_KEY: str = str(config("GEMINI_API_KEY", default=""))
    GROQ_API_KEY: str = str(config("GROQ_API_KEY", default=""))

    # Platform Configuration (always generates for these platforms)
    DEFAULT_PLATFORMS = ["linkedin", "twitter"]
    SUPPORTED_PLATFORMS: List[str] = ["twitter", "linkedin", "facebook", "instagram"]

    @classmethod
    def validate(cls) -> None:
        """Validate required settings"""
        if not cls.GEMINI_API_KEY and not cls.GROQ_API_KEY:
            raise ValueError("At least one AI API key (GEMINI or GROQ) must be set")


settings = Settings()
