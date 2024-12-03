import requests
import os

# 설정: 조직과 리포지토리 이름을 여기에 입력하세요
ORGANIZATION = 'Node-ko'       # 예: 'facebook'
REPOSITORY = 'learn'            # 예: 'react'

# GitHub API URL
API_URL = f'https://api.github.com/repos/{ORGANIZATION}/{REPOSITORY}/contributors'

# Contributors 섹션을 대체할 플레이스홀더
PLACEHOLDER = '<!-- CONTRIBUTOR PLACEHOLDER -->'

# README 파일 경로
README_PATH = './README.md'
NEW_README_PATH = '.github/profile/README.md'

# GitHub Personal Access Token (필요 시)
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')  # 환경 변수에서 토큰을 읽어옵니다.

def fetch_contributors():
    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    if GITHUB_TOKEN:
        headers['Authorization'] = f'token {GITHUB_TOKEN}'
    
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_contributors_markdown(contributors, top_n=None):
    if top_n:
        contributors = contributors[:top_n]
    
    markdown = '<div align="center">\n'
    for contributor in contributors:
        markdown += f'  <a href="{contributor["html_url"]}" target="_blank">\n'
        markdown += f'    <img src="{contributor["avatar_url"]}" width="80" height="80" style="border-radius:50%; margin:5px;" alt="{contributor["login"]}"/>\n'
        markdown += '  </a>\n'
    markdown += '</div>\n'
    return markdown

def update_readme(contributors_markdown):
    with open(README_PATH, 'r', encoding='utf-8') as file:
        readme_content = file.read()
    
    new_readme = readme_content.replace(PLACEHOLDER, contributors_markdown)
    
    with open(NEW_README_PATH, 'w', encoding='utf-8') as file:
        file.write(new_readme)

def main():
    try:
        contributors = fetch_contributors()
    except Exception as e:
        print(f"Error fetching contributors: {e}")
        return

    if not contributors:
        print("No contributors found.")
        return

    # 원하는 상위 N명만 표시하려면 top_n 설정
    contributors_markdown = generate_contributors_markdown(contributors, top_n=None)
    update_readme(contributors_markdown)
    print("README.md has been updated with the latest contributors.")

if __name__ == '__main__':
    main()
