from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.models import (
    JSONRPCRequest,
)
from app.processor import PostProcessor


app = FastAPI(title="POST CRAFT AGENT")
processor = PostProcessor()


@app.get("/.well-known/agent.json")
async def agent_info():
    """Agent card endpoint"""
    return {
        "name": "POST CRAFT AGENT",
        "description": "Transforms blog posts into engaging social media content. Automatically generates Twitter threads and comprehensive LinkedIn posts from any blog URL.",
        "url": settings.AGENT_URL,
        "version": "1.0.0",
        "provider": {"organization": "PostCraft", "url": settings.AGENT_URL},
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
            "stateTransitionHistory": True,
        },
        "authentication": {"schemes": [], "credentials": None},
        "defaultInputModes": ["text/plain"],
        "defaultOutputModes": ["text/plain"],
        "skills": [
            {
                "id": "generate_social_posts",
                "name": "Generate Social Media Posts",
                "description": "Analyzes a blog post URL and creates Twitter threads and comprehensive LinkedIn posts",
                "tags": ["social-media", "content", "blog", "twitter", "linkedin"],
                "examples": [
                    "https://example.com/blog/my-post",
                    "Convert https://techblog.com/ai-trends to social media",
                    "Create posts from https://medium.com/my-article",
                ],
                "inputModes": ["text/plain"],
                "outputModes": ["text/plain"],
            }
        ],
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent": "POST CRAFT AGENT",
        "gemini_available": bool(settings.GEMINI_API_KEY),
        "groq_available": bool(settings.GROQ_API_KEY),
    }


@app.post("/")
async def handle_request(request: Request):
    """Main A2A endpoint"""
    try:
        body = await request.json()
        print(body)
        rpc_request = JSONRPCRequest(**body)

        if rpc_request.method == "message/send":
            return await processor.handle_message_send(rpc_request)

        elif rpc_request.method == "tasks/get":
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": rpc_request.id,
                    "error": {
                        "code": -32601,
                        "message": "Task polling not implemented",
                    },
                }
            )

        else:
            return JSONResponse(
                content={
                    "jsonrpc": "2.0",
                    "id": rpc_request.id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {rpc_request.method}",
                    },
                }
            )

    except Exception as e:
        print(f"❌ Request handling error: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"},
            },
        )
