import os
import markdown
import requests
import re

def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.RequestException:
        return False

def find_links(content):
    # Regular expression to find Markdown links
    link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
    return re.findall(link_pattern, content)

def check_md_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    links = find_links(content)
                    for title, url in links:
                        if url.startswith('https://'):
                            if is_valid_url(url):
                                print(f"Valid HTTPS link: {url} (in {file})")
                            else:
                                print(f"Invalid HTTPS link: {url} (in {file})")

# Change 'directory' to the directory containing your Markdown files
directory = '/path/to/your/directory'
check_md_files(directory)
