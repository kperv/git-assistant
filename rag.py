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
        book_df = self.load_book()
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
            Analyze Text sections from MANUAL documents and answer the user question: {question}. 
            Generate a concise list of steps to implement. Keep it short. Format code, if necessary.

            Example:
            QUESTION:
            What is git?

            MANUAL:
            Chapter: 1.Getting Started
            Section: Local Version Control Systems
            Text: Many people’s version-control method of choice is to copy files into another directory (perhaps a time-stamped directory, if they’re clever).
This approach is very common because it is so simple, but it is also incredibly error prone.
It is easy to forget which directory you’re in and accidentally write to the wrong file or copy over files you don’t mean to. To deal with this issue, programmers long ago developed local VCSs that had a simple database that kept all the changes to files under revision control. One of the most popular VCS tools was a system called RCS, which is still distributed with many computers today.

            ANSWER: 
            Git is a version control wywtem that helps keep track of changes.
            Look for Chapter 1.Getting Started, Section Local Version Control Systems to learn more.

            
            MANUAL:
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
        prompt = self.build_prompt(question, context)
        answer = self.response(prompt)
        return answer

def main():
    assistant = GitAssistant()
    question = "how to commit a message?"
    answer = assistant.answer(question)
    print(answer)



if __name__ == "__main__":
    main()