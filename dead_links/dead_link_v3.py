import sys
from pathlib import Path
import markdown
from bs4 import BeautifulSoup
import requests
from rich.console import Console
from rich.table import Table
from concurrent.futures import ThreadPoolExecutor

try:
    directory = Path(sys.argv[1])
except IndexError:
    directory = Path("./")

console = Console()


def check_directory_links(directory):
    markdown_files = list(directory.glob("*.md"))
    with ThreadPoolExecutor() as executor:
        for markdown_file in markdown_files:
            executor.submit(check_file_links, markdown_file)


def check_file_links(file):
    try:
        input_file = Path(file)
        html = markdown.markdown(input_file.read_text())
        soup = BeautifulSoup(html, "html.parser")
        links = soup.find_all("a")
        hrefs = [link.attrs["href"] for link in links]
        valid = []
        invalid = []
        with ThreadPoolExecutor() as executor:
            for link, result in zip(links, executor.map(handle_link, hrefs)):
                if result[0]:
                    valid.append(link)
                else:
                    invalid.append((link, result[1]))

        valid_links, invalid_links = construct_link_tables(valid, invalid)
        console.print(f"Valid and Invalid links in {input_file}:")
        console.print(valid_links)
        console.print(invalid_links)
    except Exception as e:
        console.print(f"Error processing file {file}: {str(e)}")


def handle_link(href):
    try:
        resp = requests.get(href)
        if str(resp.status_code).startswith("2") or str(resp.status_code).startswith(
            "3"
        ):
            return True, "Valid link"
        return False, "Invalid link for unknown reason"
    except Exception as e:
        return False, str(e)


def construct_link_tables(valid, invalid):
    invalid_table = Table(
        "link", "reason", title="Invalid links in document", show_lines=True
    )
    for link, reason in invalid:
        invalid_table.add_row(link.attrs["href"], reason)

    valid_table = Table("text", "link", title="Valid links in document")
    for link in valid:
        valid_table.add_row(link.text, link.attrs["href"])

    return valid_table, invalid_table


if __name__ == "__main__":
    check_directory_links(directory)
