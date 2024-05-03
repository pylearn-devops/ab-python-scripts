from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import re

root_directory = "/Users/akashbasa/pylearn/dead_link_checker/"  # Change this to your root directory


def find_links(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
        deep_links = re.findall(r'\[.*?\]\((?!http)(.*?)\)', content)  # Find deep links
        all_links = re.findall(r'\[.*?\]\((https?://.*?)\)', content)  # Find http(s) links

        return deep_links, all_links


def check_link(link):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.get(link)
        return True
    except:
        return False
    finally:
        driver.quit()


def find_broken_links(directory):
    broken_links = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                deep_links, all_links = find_links(filepath)
                for link in all_links:
                    print("link ------------->", link)
                    if not check_link(link):
                        broken_links.append((filepath, link))
    return broken_links


# def check_link(link):
#     try:
#         options = Options()
#         options.add_argument('--headless')
#         options.add_argument('--disable-gpu')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#
#         driver = webdriver.Chrome(options=options)
#         driver.get(link)
#
#         # Check for specific patterns in the page content indicating redirection or "sorry" message
#         if "sorry" in driver.page_source.lower() or "redirect" in driver.page_source.lower():
#             return False
#         else:
#             return True
#     except:
#         return False
#     finally:
#         driver.quit()

broken_links = find_broken_links(root_directory)

if broken_links:
    print("Broken Links:")
    for link_info in broken_links:
        print(f"File: {link_info[0]}, Broken Link: {link_info[1]}")
else:
    print("No broken links found.")
    
