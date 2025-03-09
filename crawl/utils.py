from bs4 import BeautifulSoup
import html2text
import re

import difflib
import shutil
import os


async def html2md(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    for script in soup(["script", "style", "svg", "noscript", "iframe"]):
        script.decompose()
    
    # 네비게이션, 헤더, 푸터, 사이드바 등 제거
    for nav in soup.select('nav, header, footer, aside, .sidebar, .navigation, .menu, .ads, .banner'):
        nav.decompose()
    
    # 불필요한 속성 제거
    for tag in soup.find_all(True):
        # 유지할 속성 목록
        keep_attrs = ['href', 'src'] if tag.name in ['a', 'img'] else []
        
        # href 속성은 유지하되 값은 "#"로 치환
        if tag.name == 'a' and tag.has_attr('href'):
            tag['href'] = '#'
        
        # 모든 기존 속성을 복사
        attrs = dict(tag.attrs)
        
        # 유지할 속성을 제외한 나머지 모든 속성 제거
        for attr in attrs:
            if attr not in keep_attrs:
                del tag[attr]

    # 정제된 HTML
    cleaned_html = str(soup)
    
    # HTML을 Markdown으로 변환
    h = html2text.HTML2Text()
    h.ignore_links = False
    h.ignore_images = True  # 이미지는 무시
    h.ignore_tables = False
    h.body_width = 0
    
    markdown_content = h.handle(cleaned_html)
    
    # 불필요한 링크 표기 정리 (예: [텍스트](#) -> 텍스트)
    markdown_content = re.sub(r'\[(.*?)\]\(#\)', r'\1', markdown_content)
    
    # 연속된 빈 줄 제거
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)

    return markdown_content


async def find_diff(old_file, new_file):
    with open(old_file, 'r') as f:
        old_lines = f.readlines()
    with open(new_file, 'r') as f:
        new_lines = f.readlines()

    diff = difflib.unified_diff(old_lines, new_lines, fromfile=old_file, tofile=new_file)
    diff_text = ''.join(diff)
    return diff_text

async def move_files():
    src = "dump"
    dest = "legacy"
    try:
        if os.path.exists(dest):
            shutil.rmtree(dest)

        shutil.copytree(src, dest)
        print("move complete")
    except Exception as e:
        print(f"복사 중 오류가 발생했습니다: {e}")

