# tools/twitter_tool.py
from langchain.agents import Tool
import os

class TwitterTool:
    def __init__(self):
        self.tool = Tool(
            name="Twitter Tool",
            func=self.post_tweet,
            description="Useful for posting tweets to Twitter. Input should be the text of the tweet you want to post."
        )
    
    def post_tweet(self, tweet_text):
        # Mock implementation
        print(f"[MOCK] Posted tweet: {tweet_text}")
        return f"Successfully posted tweet: {tweet_text}"
    
    def __call__(self):
        return self.tool