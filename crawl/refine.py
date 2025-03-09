import os 
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

class OpenAIManager:
    def __init__(self):
        load_dotenv()
        self.client = AsyncOpenAI(
            api_key=os.environ.get('OPENAI_API_KEY')
        )
        
    async def completions(self, msg):
        chat_completion = await self.client.chat.completions.create(
            messages = [
                {
                    "role": "developer", 
                    "content": """
                        You are a helpful assistant.
                        You will be given LLM pricing information in markdown. 
                        
                        Your role is to parse the pricing of every LLM API pricing information. 
                        
                        Return your response only in json format. 
                        Look carefully and do not miss any information. 
                    """
                },
                {
                    "role": "user", 
                    "content": str(msg), 
                }
            ], 
            model="gpt-4o-mini"
        )
        return chat_completion.choices[0].message.content



if __name__ == "__main__":

    with open("openai_pricing_data.md", "r", encoding="utf-8") as md_file:
        content = md_file.read()
    
    manager = OpenAIManager()
    res = asyncio.run(manager.completions(content))
    print(res)