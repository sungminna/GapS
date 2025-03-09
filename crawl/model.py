import os
import openai
from dotenv import load_dotenv
import json
load_dotenv()
# Set your API key
client = openai.OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# Get models information
models = client.models.list()
print(models)