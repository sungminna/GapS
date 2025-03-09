import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from utils import html2md
import json


async def scrape_openai_pricing():
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
        
        
        # Open AI Cloudflare cookie 설정 -> Chrome Devtools에서 수동으로 복붙붙
        cf_clearance=""
        with open("cf_clearance.txt", "r", encoding="utf-8") as cf:
            cf_clearance = cf.read()

        print(cf_clearance)
        await context.add_cookies([
            {
                "name": "cf_clearance",
                "value": cf_clearance,  # 실제 cf_clearance 값으로 교체
                "domain": ".openai.com", 
                "path": "/",
                "secure": True,
                "httpOnly": True
            }
        ])

        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
        await context.add_cookies(cookies)


        # 새 페이지 생성
        page = await context.new_page()

        await page.goto("https://platform.openai.com/docs/pricing", timeout=60000)
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(1000)


        # 숨겨진 pricing 정보 표시시
        expand_buttons = await page.query_selector_all('button[data-variant="bare"]')        
        for button in expand_buttons:
            try:
                await button.click()
                await page.wait_for_timeout(1000)
            except Exception as e:
                print(f"버튼 클릭 중 오류 발생: {e}")

        # await page.screenshot(path="openai_pricing_screenshot.png", full_page=True)

        html_content = await page.content()
        markdown_content = await html2md(html_content)
        
        # Markdown 파일로 저장
        with open("dump/openai_pricing_data.md", "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        
        cookies_list = await context.cookies()
        for cookie in cookies_list:
            if cookie['name'] == 'cf_clearance':
                cf_clearance = cookie['value']
                break

        if cf_clearance:
            print("cf_clearance value:", cf_clearance)
            with open("cf_clearance.txt", "w", encoding="utf-8") as cf:
                cf.write(cf_clearance)
        else:
            print("cf_clearance cookie not found")


        cookies = await context.cookies()
        with open('cookies.json', 'w') as f:
            json.dump(cookies, f)

        # 브라우저 닫기
        await browser.close()
        
        print(f"스크래핑 완료! 데이터가 'openai_pricing_data.json'과 CSV 파일들로 저장되었습니다.")

        return cf_clearance

if __name__ == "__main__":
    asyncio.run(scrape_openai_pricing())
