import json

import pandas as pd
from tqdm import tqdm
from openai import OpenAI


class LLMEvaluator:
    client = OpenAI()

    def llm(self, prompt, model="gpt-4o-mini"):
        response = self.client.chat.completions.create(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def read_answers(self):
        return pd.read_csv("data/ground_truth_with_assistant.csv")

    def build_prompt(self, question, answer):
        prompt = f"""
            You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
            Your task is to analyze the relevance of the generated answer to the given question.
            Based on the relevance of the generated answer, you will classify it
            as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

            Here is the data for evaluation:

            Question: {question}
            Generated Answer: {answer}

            Please analyze the content of the generated answer in relation to the question
            and provide your evaluation your evaluation in parsable JSON without using code blocks:

            {{
              "relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
              "explanation": "[Provide a brief explanation for your evaluation]"
            }}
            """.strip()
        return prompt

    def collect_evaluations(self):
        answers = self.read_answers()
        answers_dict = answers.to_dict(orient="records")
        evaluations = []

        for doc in tqdm(answers_dict):
            question = doc["question"]
            assistant_answer = doc["assistant_answer"]
            prompt = self.build_prompt(question, assistant_answer)
            evaluation = self.llm(prompt)
            evaluations.append(evaluation)
        return evaluations

    def llm_as_a_judge(self):
        evaluations = self.collect_evaluations()

        json_evaluations = []

        for i, str_eval in enumerate(evaluations):
            json_eval = json.loads(str_eval)
            json_evaluations.append(json_eval)
        df_evaluations = pd.DataFrame(json_evaluations)
        df_evaluations.to_csv('data/df_evaluations.csv', index=False)
        print("LLM evaluation results:")
        print(df_evaluations.relevance.value_counts())


def main():
    evaluator = LLMEvaluator()
    evaluator.llm_as_a_judge()


if __name__ == "__main__":
    main()
