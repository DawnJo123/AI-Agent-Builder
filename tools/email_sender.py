# tools/email_sender.py
from langchain.agents import Tool

class EmailSenderTool:
    def __init__(self):
        self.tool = Tool(
            name="Email Sender",
            func=self.send_email,
            description="Useful for sending emails. Input should be in the format: 'to:recipient@example.com;subject:Email Subject;body:Email body text'."
        )
    
    def send_email(self, email_data):
        try:
            data_parts = email_data.split(';')
            email_info = {}
            for part in data_parts:
                if ':' in part:
                    key, value = part.split(':', 1)
                    email_info[key.strip()] = value.strip()
            
            # Mock implementation
            print(f"[MOCK] Sent email to {email_info.get('to', 'unknown')}")
            print(f"Subject: {email_info.get('subject', 'No subject')}")
            print(f"Body: {email_info.get('body', 'No body')}")
            
            return f"Email sent successfully to {email_info.get('to', 'unknown')}"
        except Exception as e:
            return f"Error sending email: {str(e)}"
    
    def __call__(self):
        return self.tool