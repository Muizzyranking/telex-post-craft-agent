from app import settings

settings.validate()

if __name__ == "__main__":
    import uvicorn

    print("🚀 Starting POST CRAFT AGENT")
    print(f"📍 URL: {settings.AGENT_URL}")
    print(f"🔑 Gemini: {'✅' if settings.GEMINI_API_KEY else '❌'}")
    print(f"🔑 Groq: {'✅' if settings.GROQ_API_KEY else '❌'}")
    print(f"🎯 Default platforms: {', '.join(settings.DEFAULT_PLATFORMS)}")
    print("=" * 60)

    uvicorn.run("app.api:app", host="0.0.0.0", port=settings.PORT, reload=True)
