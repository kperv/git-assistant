import time
import tqdm
import requests
from bs4 import BeautifulSoup


def parse_url(url: str):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return soup


def get_links(soup: BeautifulSoup, base_url: str):
    chapter_links = []
    toc = soup.find("ol", class_="book-toc")
    for chapter in toc.find_all("li", class_="chapter"):
        chapter_link = chapter.find("h2").find("a")
        if chapter_link and "href" in chapter_link.attrs:
            full_url = requests.compat.urljoin(base_url, chapter_link["href"])
            chapter_links.append(full_url)

        subchapters = chapter.find("ol")
        if subchapters:
            for subchapter in subchapters.find_all("a"):
                if "href" in subchapter.attrs:
                    full_url = requests.compat.urljoin(base_url, subchapter["href"])
                    chapter_links.append(full_url)
    return chapter_links


def parse_chapter(chapter_url):
    ch_soup = parse_url(chapter_url)
    chapter = ch_soup.find("h1")
    chapter_name = chapter.get_text(strip=True)

    main_content_div = ch_soup.find("div", class_="book edition2")
    chapter_contents = []
    for paragraph in main_content_div.find_all("p"):
        paragraph_text = paragraph.get_text(strip=True)
        chapter_contents.append({"chapter": chapter_name, "text": paragraph_text})
    time.sleep(1)
    return chapter_contents


def main():
    url = "https://git-scm.com/book/en/v2"
    base_url = "https://git-scm.com"
    soup = parse_url(url)
    chapters = get_links(soup, base_url)
    total_steps = len(chapters)
    book_contents = []
    for chapter in tqdm(chapters, total=total_steps):
        chapter_contents = parse_chapter(chapter)
        book_contents.append(chapter_contents)


if __name__ == "__main__":
    main()
