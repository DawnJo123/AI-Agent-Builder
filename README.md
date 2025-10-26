# AI Agent Builder

## Features

- **Dynamic Agent Creation**: Generate custom AI agents based on natural language descriptions
- **Multiple Tools**: Web scraper, PDF summarizer, email sender, Twitter poster, file logger
- **Dual LLM Support**: Groq (primary) and OpenRouter integration
- **RESTful API**: Easy integration with any frontend or service
- **Postman Collection**: Pre-configured API testing collection included

## Setup Instructions

### File Structure
agent-builder/
  -tools/
    -email_sender.py
    -file_logger.py
    -pdf_summarizer.py
    -twitter_tool.py
    -web_scraper.py
  -uploads/
    -document.pdf
  -.env
  -app.py
  -requirements.txt

### Installation

1. **Clone or download the project**

2. **Create and activate a virtual environment** (recommended):

   **Windows:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

   **macOS/Linux:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**:
   Create a `.env` file with your API keys:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   OPENROUTER_API_KEY=your_openrouter_api_key_here
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```
   
   The server will start on `http://localhost:5000`

## API Endpoints

### 1. Create Agent
**POST** `/generate_agent`

Creates a new AI agent with custom capabilities.

```json
{
  "name": "My Web Scraper Agent",
  "query": "Create an agent that scrapes {website URL} and sends summaries via email to abc@example.com"
}
```

**Response**:
```json
{
  "message": "Agent created successfully",
  "id": "agent-uuid",
  "name": "My Web Scraper Agent",
  "custom_prompt": "Generated system prompt...",
  "tools": ["scraper", "emailSender", "fileLogger"]
}
```

### 2. Run Agent
**GET** `/run_agent/<agent_id>`

Executes the created agent with its original query.

**Response**:
```json
{
  "output": "Agent execution results..."
}
```

### 3. Get All Agents
**GET** `/all_agents`

Returns all created agents and their configurations.

## Example Usage

### Example 1: News Scraper & Email Agent
```json
{
  "name": "BBC News Emailer",
  "query": "Scrape BBC news homepage, extract top headlines, and send them via email to admin@company.com"
}
```

### Example 2: PDF Document Processor
```json
{
  "name": "Document Summarizer",
  "query": "Read PDF files from uploads folder, create bullet-point summaries, and post key insights to Twitter"
}
```

### Example 3: Social Media Content Creator
```json
{
  "name": "Twitter Content Bot",
  "query": "Generate engaging Twitter posts about technology trends and post them automatically"
}
```

## Available Tools
**Web Scraper** 
**PDF Summarizer** 
**Email Sender**
**Twitter Tool**
**File Logger**

## LLM Providers

### Groq
- **Model**: `meta-llama/llama-4-maverick-17b-128e-instruct`

### OpenRouter
- **Model**: `deepseek/deepseek-chat-v3-0324:free`


To switch to OpenRouter, uncomment the OpenRouter LLM initialization in `app.py` and comment out the Groq initialization.

## Integration Notes

### Mocked vs Real Integrations

#### Mocked (Demo Purpose)
- **Email Sender**: Prints email details to console instead of sending real emails
- **Twitter Tool**: Prints tweet content to console instead of posting to Twitter
- **PDF Summarizer**: Uses default upload folder path

#### Real Integrations
- **Web Scraper**: Actually fetches and parses web content using requests and BeautifulSoup
- **File Logger**: Creates real log files (`agent_logs.txt`)
- **LLM Services**: Real API calls to Groq/OpenRouter


## Postman Collection

The included `Agent Builder APIs.postman_collection.json` contains:
- Pre-configured requests for all endpoints
- Example request bodies
- Environment variables setup
- Test scenarios for different agent types

### Import Instructions
1. Open Postman
2. Click "Import" 
3. Select the JSON file
4. Set `baseURL` variable to `http://localhost:5000`

## Upload Folder

The `agent-builder/uploads` folder is used by the PDF Summarizer tool. Keep existing content in this folder for demo purposes. The tool will process any PDF files found in this directory.


