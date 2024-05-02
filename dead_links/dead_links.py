import os
import re
import requests

root_directory = "./"  # Change this to your root directory

def find_links(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        deep_links = re.findall(r'\[.*?\]\((?!http)(.*?)\)', content)  # Find deep links
        all_links = re.findall(r'\[.*?\]\((.*?)\)', content)  # Find all links

        return deep_links, all_links

def check_link(link):
    try:
        response = requests.head(link)
        if response.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def find_broken_links(directory):
    broken_links = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                deep_links, all_links = find_links(filepath)
                for link in all_links:
                    if not check_link(link):
                        broken_links.append((filepath, link))
    return broken_links

broken_links = find_broken_links(root_directory)

if broken_links:
    print("Broken Links:")
    for link_info in broken_links:
        print(f"File: {link_info[0]}, Broken Link: {link_info[1]}")
else:
    print("No broken links found.")
