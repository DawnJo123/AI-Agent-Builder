# tools/web_scraper.py
from langchain.agents import Tool
import requests
from bs4 import BeautifulSoup

class WebScraperTool:
    def __init__(self):
        self.tool = Tool(
            name="Web Scraper",
            func=self.scrape_website,
            description="Useful for scraping content from websites. Input should be a URL."
        )
    
    def scrape_website(self, url):
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
                
            # Get text and clean up
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:2000]  # Limit to first 2000 characters
        except Exception as e:
            return f"Error scraping website: {str(e)}"
    
    def __call__(self):
        return self.tool