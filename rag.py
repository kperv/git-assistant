import pandas as pd
from openai import OpenAI

from parse_book import BookParser
from elastic import DocumentsRetriver


class GitAssistant:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1/",
            api_key="ollama",
        )
        try:
            book_df = pd.read_csv("book.csv")
        except FileNotFoundError:
            book_df = self.load_book()
            book_df.to_csv("book.csv", index=False)
        self.retriever = DocumentsRetriver(book_df)

    def load_book(self):
        parser = BookParser()
        book = parser.parse()
        book_df = pd.DataFrame.from_dict(book)
        book_df.dropna(inplace=True)
        return book_df

    def search_book(self, question: str):
        return self.retriever.find_documents(question)

    def build_prompt(self, question: str, context: list[str]):
        context_docs = []
        for context_item in context:
            context_doc = f"""
                Chapter: {context_item["chapter"]}
                Section: {context_item["section"]}
                Text: {context_item["text"]}
            """
            context_docs.append(context_doc)

        context_for_prompt = " \n\n###".join(context_docs)

        prompt = f"""
            You are provided a section of a BOOK, analyze text in the 'Text' section and answer the question. 
            Make it short and easy to understand. 

            QUESTION: {question}

            BOOK:
            {context_for_prompt}
        """
        return prompt

    def response(self, prompt: str):
        response = self.client.chat.completions.create(
            model="llama3",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        return response.choices[0].message.content

    def answer(self, question: str):
        context = self.search_book(question)
        print("New question: ")
        print(question)
        prompt = self.build_prompt(question, context)
        answer = self.response(prompt)
        print(answer)
        return answer


def main():
    assistant = GitAssistant()
    question = "how to commit a message?"
    answer = assistant.answer(question)
    print(answer)


if __name__ == "__main__":
    main()
