# PostCraft Agent

A powerful AI agent that transforms blog posts into engaging social media content. Automatically generates Twitter threads and comprehensive LinkedIn posts from any blog URL.

## Features

- **Twitter Thread Generation**: Creates multi-tweet threads (3-5 tweets) with proper numbering and narrative flow
- **LinkedIn Post Generation**: Produces comprehensive 300-800 word professional posts with detailed insights
- **Automatic Platform Detection**: Always generates for both LinkedIn and Twitter regardless of input
- **AI-Powered**: Uses Google Gemini AI for intelligent content generation
- **FastAPI Integration**: Built with FastAPI for high-performance API endpoints
- **JSON-RPC 2.0 Protocol**: Standardized communication protocol

## Quick Start

### Prerequisites

- Python 3.8+
- `uv` package manager
- Google Gemini API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd postcraft-agent
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.sample .env
   # Edit .env with your API keys
   ```

4. **Run the application**
   ```bash
   uv run python main.py
   ```

The agent will be available at `http://localhost:8000`

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required: Google Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Groq API Key (fallback)
GROQ_API_KEY=your_groq_api_key_here

# Optional: Server Configuration
AGENT_URL=http://localhost:8000
PORT=8000
```

### API Keys

You need at least one AI API key:
- **Google Gemini** (recommended): Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- **Groq** (fallback): Get your API key from [Groq Console](https://console.groq.com/)

## Usage

### API Endpoints

#### Agent Information
```bash
GET /.well-known/agent.json
```

Returns agent metadata and capabilities.

#### Health Check
```bash
GET /health
```

Returns service health status and API key availability.

#### Generate Social Media Posts
```bash
POST /
Content-Type: application/json
```

**Request Body:**
```json
{
  "jsonrpc": "2.0",
  "method": "message/send",
  "params": {
    "id": "unique-task-id",
    "message": {
      "role": "user",
      "parts": [
        {
          "kind": "text",
          "text": "https://example.com/blog/my-awesome-post"
        }
      ]
    }
  },
  "id": 1
}
```

**Response:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "id": "unique-task-id",
    "status": {
      "state": "completed",
      "timestamp": "2024-01-01T12:00:00.000Z"
    },
    "artifacts": [
      {
        "artifactId": "artifact-id",
        "name": "social_media_posts",
        "parts": [
          {
            "kind": "text",
            "text": "# 🎉 Social Media Posts Generated\n\n## 🐦 Twitter\nTweet 1/3: [First tweet content]\nTweet 2/3: [Second tweet content]\nTweet 3/3: [Third tweet content]\n\n---\n\n## 💼 LinkedIn\n[Comprehensive LinkedIn post content]\n\n---"
          }
        ]
      }
    ]
  }
}
```

### Development

#### Running with Uvicorn
```bash
uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### Running Tests
```bash
uv run python test_generator.py
uv run python test_message_parser.py
```

## Output Format

### Twitter Threads
- 3-5 tweets per thread
- Proper numbering (1/n, 2/n, etc.)
- Hook → Development → Call-to-action structure
- Relevant hashtags in final tweet
- Smooth narrative flow

### LinkedIn Posts
- 300-800 words comprehensive posts
- Professional tone with actionable insights
- Structured content with bullet points
- 3-5 relevant hashtags
- Engagement-focused questions
- Original blog URL included

## Architecture

```
src/
├── api.py           # FastAPI endpoints and agent info
├── config.py        # Configuration and settings
├── extractor.py     # Blog content extraction
├── generator.py     # AI-powered content generation
├── message_parser.py # Message parsing and URL extraction
├── models.py        # Pydantic data models
└── processor.py     # Main processing logic
```

## Error Handling

The agent gracefully handles:
- Invalid blog URLs
- Network connectivity issues
- AI API failures
- Malformed requests
- Missing API keys

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the repository
- Check the health endpoint for service status
- Verify API key configuration in logs