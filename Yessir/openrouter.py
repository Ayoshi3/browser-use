import asyncio
import os
from dotenv import load_dotenv
from openai import OpenAI
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig

load_dotenv()

browser = Browser(
    config=BrowserConfig(
        headless=False,
        chrome_instance_path='C:\\Program Files\\BraveSoftware\\Brave-Browser\\Application\\brave.exe',
    )
)

async def main():
    task = (
   'Navigate to NBA section on bet365:\n'
   '1. Go to "https://www.bet365.com"\n'
   '2. Wait for main page to load completely\n'
   '3. Click NBA logo/text in middle scrolling menu (it has NBA basketball logo and text below)\n' 
   '4. If menu option not visible, find and click NBA text in secondary menu below\n'
   '5. Confirm NBA betting section is loaded by checking for NBA teams and games\n'
    )
   
    
    api_key = os.getenv('OPENROUTER_API_KEY')
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set")
        
    model = ChatOpenAI(
        model="openai/gpt-3.5-turbo:free",
        api_key=SecretStr(api_key),
        base_url="https://openrouter.ai/api/v1",
        default_headers={
            "HTTP-Referer": "https://localhost:3000",
            "X-Title": "Local Testing"
        }
    )
    
    agent = Agent(
        task=task,
        llm=model,
        browser=browser,
        generate_gif=False  # Disable GIF creation to avoid font errors
    )

    await agent.run()
    await browser.close()

if __name__ == '__main__':
    asyncio.run(main())