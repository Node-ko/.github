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
NEW_README_PATH = './profile/README.md'

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

    # 최대 100명, 한 줄에 12명씩 표시
    contributors_markdown = '''
<a href="https://github.com/Node-ko/learn/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Node-ko/learn" />
</a>
    '''
    update_readme(contributors_markdown)
    print("README.md has been updated with the latest contributors.")

if __name__ == '__main__':
    main()
