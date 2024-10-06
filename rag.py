from openai import OpenAI

from elastic import DocumentsRetriver


class GitAssistant:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1/",
            api_key="ollama",
        )
        self.retriever = DocumentsRetriver()

    def search_book(self, question: str):
        return self.retriever.find_documents(question)

    def build_prompt(self, question: str, context: list[str]):
        context_docs = " \n".join(context)
        prompt = f"""
            Analyze manual documents and answer the user question: {question}. 
            Generate a concise list of steps to implement. Keep it short.
            
            Manual:
            {context_docs}
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
