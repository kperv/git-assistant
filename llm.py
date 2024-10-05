from openai import OpenAI


class GitAssistant:
    def __init__(self):
        client = OpenAI(
            base_url='http://localhost:11434/v1/',
            api_key='ollama',
        )

    def build_prompt(self, texts: list[str]):
        prompt = """
            Answer the 

        """