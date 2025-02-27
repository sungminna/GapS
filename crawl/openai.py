import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from utils import html2md

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
        await context.add_cookies([
            {
                "name": "cf_clearance",
                "value": "IRlcf70hsIOVnajrd4CpysLvOCfYKM2nJYZmkbh8UqQ-1740667753-1.2.1.1-RA3tyg9PPDti9rdSGyqCzB_4WUIwxys72ahUQck01dgXe78_dPJWGJf3hmNaJxM92HYVdGZVui.pvJuQwocGt6EEB.AQ4dwi_jCiQA2bT0p.ZAQS4pt9EAYbjjA0N2.J9Iy0tcR4Q1ylASu3GJ.6AQFIj5ReoTyMIUp5hA5JfD1MlAMeyZT4VfYR7rKtwXCictp1ZreABA_oS9t0k8yXWfWrBi0GzmTrXHFvmsVD2w6tNt85iGahB_MdKsMANCftdbbdeugSxP_2i.t35xQloGvXLBDJYhl448VEhU4biQg",  # 실제 cf_clearance 값으로 교체
                "domain": ".openai.com", 
                "path": "/",
                "secure": True,
                "httpOnly": True
            }
        ])

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

        await page.screenshot(path="openai_pricing_screenshot.png", full_page=True)

        html_content = await page.content()
        markdown_content = html2md(html_content)
        
        # Markdown 파일로 저장
        with open("openai_pricing_data.md", "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)
        
        # 브라우저 닫기
        await browser.close()
        
        print(f"스크래핑 완료! 데이터가 'openai_pricing_data.json'과 CSV 파일들로 저장되었습니다.")
        return 0

if __name__ == "__main__":
    asyncio.run(scrape_openai_pricing())
