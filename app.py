import os
import uuid
from datetime import datetime
from flask import Flask,request,jsonify

from tools import PDFSummarizerTool, WebScraperTool, TwitterTool, EmailSenderTool, FileLoggerTool

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor 
from langchain.tools import Tool


from dotenv import load_dotenv
load_dotenv()

app=Flask(__name__)

# Initializing LLM

llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# llm = ChatOpenAI(
#   api_key=os.getenv("OPENROUTER_API_KEY"),
#   base_url=os.getenv("OPENROUTER_BASE_URL"),
#   model="deepseek/deepseek-chat-v3-0324:free")

twitter_post_instance=TwitterTool()
pdf_summarizer_instance = PDFSummarizerTool(llm)
web_scraper_instance = WebScraperTool()
email_sender_instance = EmailSenderTool()
file_logger_instance = FileLoggerTool()

twitter_post_tool= Tool(
    name="twitterPost",
    func=twitter_post_instance.post_tweet,
    description="Post tweets and messages to Twitter/X social media platform"
)

pdf_summarizer_tool = Tool(
    name="summarizer",
    func=pdf_summarizer_instance.summarize_pdf, 
    description="Summarizes a PDF file. Input should be the path to a PDF file."
)

web_scraper_tool = Tool(
    name="scraper",
    func=web_scraper_instance.scrape_website,
    description="Scrapes a website. Input should be a URL."
)

email_sender_tool= Tool(
    name="emailSender",
    func=email_sender_instance.send_email,
    description="Send emails to specified recipients with custom subject and body"
)

file_logger_tool= Tool(
    name="fileLogger",
    func=file_logger_instance.log_to_file,
    description="Save and log information to text files for record keeping"
)

TOOLS = {
    "twitterPost": twitter_post_tool,
    "summarizer": pdf_summarizer_tool,
    "scraper": web_scraper_tool,
    "emailSender": email_sender_tool,
    "fileLogger": file_logger_tool
}

PROMPT_GENERATOR_PROMPT = """
You are an expert AI agent designer. Your task is to create the perfect system prompt for an AI agent and choose the appropriate tools.

The agent has access to these tools:
- twitterPost: Post tweets and messages to Twitter/X social media platform.
- scraper: Scrape and extract content from any website or URL
- summarizer: Read, analyze, and summarize PDF documents
- emailSender: Send emails to specified recipients with custom subject and body.
- fileLogger: Save and log information to text files for record keeping

Guidelines for your generated prompt:
1. Define the agent's role and primary goal clearly
2. Outline a specific step-by-step process for the agent to follow
3. Specify exactly which tools should be used and when to use them
4. Include clear decision-making criteria for tool selection
5. Set constraints and rules (e.g., "Always verify information before proceeding")
6. Define the expected output format and what to include in responses
7. IMPORTANT: For web scraping tasks, always instruct the agent to display the scraped content in the response
8. IMPORTANT: Be specific about when to use each tool based on the task requirements
9. IMPORTANT: For every task,Save and log information to text files for record keeping

Create a system prompt that will help the agent make the right decisions about which tools to use.

Return only a JSON with keys 'tools' (list of tool names) and 'prompt' (system prompt for the agent). Nothing else.
"""

prompt_and_tool=ChatPromptTemplate.from_messages([
    ("system",PROMPT_GENERATOR_PROMPT),
    ("human","{user_request}")
])

created_agents= {}

@app.route("/generate_agent", methods=['POST'])
def create_agent():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        user_query = data.get('query')
        agent_name = data.get('name')
        
        if not user_query or not agent_name:
            return jsonify({'error': 'Both query and name are required'}), 400

        # Generate the custom system prompt
        promptAndTools = prompt_and_tool.format_messages(user_request=user_query)
        generated_json = llm.invoke(promptAndTools).content

        import json
        import re
        raw = generated_json.strip()
        
        
        if raw.startswith("```"):
            raw = re.sub(r"^```[a-zA-Z]*\n?", "", raw)
            raw = re.sub(r"\n?```$", "", raw)
            raw = raw.strip()

        try:
            jsonData = json.loads(raw)
        except json.JSONDecodeError as e:
            return jsonify({'error': f'Invalid JSON generated: {str(e)}'}), 500

        # Validate tools exist
        valid_tools = []
        for tool in jsonData.get("tools", []):
            if tool in TOOLS:
                valid_tools.append(tool)
        
        if not valid_tools:
            return jsonify({'error': 'No valid tools selected'}), 400

        agent_id = str(uuid.uuid4())
        created_agents[agent_id] = {
            'id': agent_id,
            'name': agent_name,
            'query': user_query,
            'generated_system_prompt': jsonData["prompt"],
            'created_at': datetime.now().isoformat(),
            "tools": valid_tools
        }

        return jsonify({
            'message': 'Agent created successfully',
            'id': agent_id,
            'name': agent_name,
            'custom_prompt': jsonData["prompt"],
            "tools": valid_tools
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    




@app.route("/run_agent/<agent_id>", methods=['GET'])  # Should be POST, not GET
def run_agent(agent_id):
    if agent_id not in created_agents:
        return jsonify({'error': 'Agent not found'}), 404
    

    # if "summarizer" in created_agents[agent_id]['tools']:
    #     i
    
    # print(request.json)
    # Get user input from request
    # user_input = request.json.get('input', '')
    user_input=created_agents[agent_id]['query']
    print(user_input)
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400
    
    # Get tools for this agent
    agent_tools = []
    for tool_name in created_agents[agent_id]["tools"]:
        if tool_name in TOOLS:
            agent_tools.append(TOOLS[tool_name])
    
    # Create agent prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", created_agents[agent_id]["generated_system_prompt"]),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Create and execute agent
    agent = create_tool_calling_agent(llm=llm, tools=agent_tools, prompt=prompt)
    executor = AgentExecutor(agent=agent, tools=agent_tools, verbose=True)
    
    # Execute with proper input format
    result = executor.invoke({"input": user_input})
    
    return jsonify({"output": result["output"]})

@app.route("/all_agents",methods=['GET'])
def all_agents():
     return created_agents

if __name__=='__main__':
    app.run(debug=True,port=5000)