import time
from tqdm import tqdm
import pandas as pd
import requests
from bs4 import BeautifulSoup


class BookParser:
    url: str = "https://git-scm.com/book/en/v2"
    base_url: str = "https://git-scm.com"

    def parse_url(self, url: str):
        """Read contents of the url"""
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        return soup


    def get_links(self, soup: BeautifulSoup):
        """Collect links to all chapters"""
        chapter_links = []
        toc = soup.find("ol", class_="book-toc")
        for chapter in toc.find_all("li", class_="chapter"):
            chapter_link = chapter.find("h2").find("a")
            if chapter_link and "href" in chapter_link.attrs:
                full_url = requests.compat.urljoin(self.base_url, chapter_link["href"])
                chapter_links.append(full_url)

            subchapters = chapter.find("ol")
            if subchapters:
                for subchapter in subchapters.find_all("a"):
                    if "href" in subchapter.attrs:
                        full_url = requests.compat.urljoin(self.base_url, subchapter["href"])
                        chapter_links.append(full_url)
        return chapter_links


    def parse_chapter(self, chapter_url: str):
        """Find text and return each paragraph with chapter name in a dict"""
        ch_soup = self.parse_url(chapter_url)
        chapter = ch_soup.find("h1")
        chapter_name = chapter.get_text(strip=True)
        main_content_div = ch_soup.find("div", class_="book edition2")

        chapter_contents = []
        for paragraph in main_content_div.find_all("p"):
            paragraph_text = paragraph.get_text(strip=True)
            chapter_contents.append({"chapter": chapter_name, "text": paragraph_text})

        # respect
        time.sleep(1)
        return chapter_contents
    
    def parse(self):
        """Collect all book chapters"""
        soup = self.parse_url(self.url)
        chapters = self.get_links(soup)

        total_steps = len(chapters)
        book_contents = []
        for chapter in tqdm(chapters, total=total_steps):
            chapter_contents = self.parse_chapter(chapter)
            book_contents.extend(chapter_contents)
        return book_contents


def main():
    parser = BookParser()
    book = parser.parse()
    book_df = pd.DataFrame.from_dict(book)
    book_df.to_csv("book.csv", index=False)


if __name__ == "__main__":
    main()
