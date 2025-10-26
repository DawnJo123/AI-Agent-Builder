# tools/file_logger.py
from langchain.agents import Tool
import datetime
import os

class FileLoggerTool:
    def __init__(self):
        self.tool = Tool(
            name="File Logger",
            func=self.log_to_file,
            description="Useful for logging information to a file. Input should be the text you want to log."
        )
    
    def log_to_file(self, log_data):
        try:
            log_file = "agent_logs.txt"
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            with open(log_file, "a") as f:
                f.write(f"[{timestamp}] {log_data}\n")
            
            return f"Logged successfully to {log_file}"
        except Exception as e:
            return f"Error logging to file: {str(e)}"
    
    def __call__(self):
        return self.tool