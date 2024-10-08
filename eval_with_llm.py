from tqdm import tqdm
import pandas as pd
from openai import OpenAI

client = OpenAI()


def llm(prompt, model="gpt-4o-mini"):
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def read_answers():
    answers_df = pd.read_csv("ground_truth_with_assistant.csv")
    answers_dict = answers_df.to_dict(orient="records")
    return answers_dict


def build_prompt(question, answer):
    prompt = f"""
        You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
        Your task is to analyze the relevance of the generated answer to the given question.
        Based on the relevance of the generated answer, you will classify it
        as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

        Here is the data for evaluation:

        Question: {question}
        Generated Answer: {answer}

        Please analyze the content of the generated answer in relation to the question
        and provide your evaluation as a dictionaty with two fields:
        "relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
        "explanation": "[Provide a brief explanation for your evaluation]"
        """.strip()
    return prompt


def llm_as_a_judge():
    answers = read_answers()
    answers_with_evaluations = []

    for doc in tqdm(answers):
        question = doc["question"]
        assistant_answer = doc["assistant_answer"]
        prompt = build_prompt(question, assistant_answer)
        judge_evaluation = llm(prompt)
        print("*" * 10)
        print(judge_evaluation)
        print(dict(judge_evaluation))
        eval_doc = {
            "question": question,
            "assistant_answer": assistant_answer,
            "relevance": judge_evaluation["relevance"],
            "explanation": judge_evaluation["explanation"],
        }
        answers_with_evaluations.append(eval_doc)
        break

    df_evaluations = pd.DataFrame.from_dict(answers_with_evaluations)
    print(df_evaluations.relevance.value_counts())


def main():
    print("Start evaluating ...")
    llm_as_a_judge()


if __name__ == "__main__":
    main()
