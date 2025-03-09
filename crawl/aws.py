import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from utils import html2md
import re

async def scrape_aws_pricing():
    async with async_playwright() as p:
        # 브라우저 시작 (헤드리스 불가 - Open AI)
        browser = await p.chromium.launch(
            headless=False,
            args=[
            ]
        )

        # Open AI 요청 Agent 설정 -> Chrome Devtools에서 수동으로 복붙
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
            extra_http_headers={
                "referer": "https://platform.openai.com/docs/pricing",
                "sec-ch-ua": "\"Not(A:Brand\";v=\"99\", \"Google Chrome\";v=\"133\", \"Chromium\";v=\"133\"",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "\"Windows\""
            }
        )

        # 새 페이지 생성
        page = await context.new_page()

        await context.add_cookies([
            {
                "name": "aws_pricing_region_name",
                "value": "%7B%22reg%22%3A%22US%20East%20(N.%20Virginia)%22%7D",  # 리전 지정
                "domain": "aws.amazon.com", 
                "path": "/",
            }
        ])

        await page.goto("https://aws.amazon.com/bedrock/pricing/", timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)

        await page.click('li[role="tab"]:has-text("Stability AI")')
        total_height = await page.evaluate("document.body.scrollHeight")
        half_height = total_height // 2
        await page.evaluate(f"window.scrollTo(0, {half_height})")
        await page.wait_for_timeout(1000)
        # await page.screenshot(path="aws_pricing_screenshot_stability.png", full_page=True)
        
        html_content = await page.content()
        markdown_content = await html2md(html_content)

        h2_name="Stability AI"
        pattern = rf"(?<=##  {h2_name}\n)(.*?)(?=##  |\n#  |\Z)"
        match = re.search(pattern, markdown_content, re.DOTALL)
        res = match.group(0).strip() if match else None

        markdown_content = str(res)
        
        # Markdown 파일로 저장
        with open("dump/aws_pricing_data_stability.md", "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)


        await page.click('li[role="tab"]:has-text("Amazon")')
        await page.wait_for_timeout(1000)
        await page.click('li[role="tab"]:has-text("Amazon Titan")')
        total_height = await page.evaluate("document.body.scrollHeight") # Amazon data fetch 로직 대응(동적)
        half_height = total_height // 2
        await page.evaluate(f"window.scrollTo(0, {half_height})")
        await page.wait_for_timeout(1000)
        # await page.screenshot(path="aws_pricing_screenshot_titan.png", full_page=True)
        await page.wait_for_timeout(1000)
        

        html_content = await page.content()
        markdown_content = await html2md(html_content)
        
        h2_name="Amazon Titan"
        pattern = rf"(?<=##  {h2_name}\n)(.*?)(?=##  |\n# |\Z)"
        match = re.search(pattern, markdown_content, re.DOTALL)
        res = match.group(0).strip() if match else None

        markdown_content = str(res)
        
        # Markdown 파일로 저장
        with open("dump/aws_pricing_data_titan.md", "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        
        # 브라우저 닫기
        await browser.close()
        
        print(f"스크래핑 완료! 데이터가 'aws_pricing_data.json'과 CSV 파일들로 저장되었습니다.")
        return 0

if __name__ == "__main__":
    asyncio.run(scrape_aws_pricing())
