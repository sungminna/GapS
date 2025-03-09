import asyncio

from anthropic import scrape_anthropic_pricing
from aws import scrape_aws_pricing
from azure import scrape_azure_pricing
from gemini import scrape_gemini_pricing
from openai_browser import scrape_openai_pricing
from perplexity import scrape_perplexity_pricing
from vertex import scrape_vertex_pricing

from compare import compare_and_report
from utils import move_files

async def main():
    print("Start")
    
    # Run all scraping functions concurrently
    tasks = [
        scrape_anthropic_pricing(),
        scrape_aws_pricing(),
        scrape_azure_pricing(),
        scrape_gemini_pricing(),
        scrape_openai_pricing(),
        scrape_perplexity_pricing(),
        scrape_vertex_pricing()
    ]
    
    await asyncio.gather(*tasks)
    
    print("hey!")
    await compare_and_report()
    print("cmp done")
    await move_files()
    

# Run the main function
asyncio.run(main())