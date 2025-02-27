import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from utils import html2md

async def scrape_azure_pricing():
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

        await page.goto("https://azure.microsoft.com/en-us/pricing/details/cognitive-services/openai-service/", timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)


        # east-us-2 region 선택
        await page.select_option('.region-selector', 'us-east-2')
        await page.wait_for_timeout(1000)
        await page.screenshot(path="azure_pricing_screenshot_east.png", full_page=True)

        html_content = await page.content()
        markdown_content = html2md(html_content)
        # Markdown 파일로 저장
        with open("azure_pricing_data_east.md", "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)

        # north cenrtral region 선택
        await page.select_option('.region-selector', 'us-north-central')
        await page.wait_for_timeout(1000)
        await page.screenshot(path="azure_pricing_screenshot_north.png", full_page=True)

        html_content = await page.content()
        markdown_content = html2md(html_content)
        # Markdown 파일로 저장
        with open("azure_pricing_data_north.md", "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        
        # 브라우저 닫기
        await browser.close()
        
        print(f"스크래핑 완료! 데이터가 'azure_pricing_data.json'과 CSV 파일들로 저장되었습니다.")
        return 0

if __name__ == "__main__":
    asyncio.run(scrape_azure_pricing())
