import tqdm
import json
from openai import OpenAI

client = OpenAI()

def llm(prompt, model='gpt-4o-mini'):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def read_answers():
    answers_df = pd.read_csv('ground_truth_with_assistant.csv')
    answers_dict = answers_df.to_dict(orient='records')
    print(answers_dict)
    return answers_dict

def build_prompt(question, answer):
    prompt = """
        You are an expert evaluator for a Retrieval-Augmented Generation (RAG) system.
        Your task is to analyze the relevance of the generated answer to the given question.
        Based on the relevance of the generated answer, you will classify it
        as "NON_RELEVANT", "PARTLY_RELEVANT", or "RELEVANT".

        Here is the data for evaluation:

        Question: {question}
        Generated Answer: {answer_llm}

        Please analyze the content and context of the generated answer in relation to the question
        and provide your evaluation in parsable JSON without using code blocks:

        {{
        "Relevance": "NON_RELEVANT" | "PARTLY_RELEVANT" | "RELEVANT",
        "Explanation": "[Provide a brief explanation for your evaluation]"
        }}
        """.strip()
    return prompt

def llm_as_a_judge():
    answers = read_answers()
    evaluations = []

    for doc in tqdm(answers):
        question = doc['question']
        assistant_answer = doc['assistant_answer']
        prompt = build_prompt(question, assistant_answer)
        judge_evaluation = llm(prompt)
        print(judge_evaluation)
        break
        evaluations.append(judge_evaluation)

    df_evaluations = pd.DataFrame(evaluations)
    print(df_evaluations.Relevance.value_counts())


def main():
    print("Start evaluating ...")
    llm_as_a_judge()


if __name__=='__main__':
    main()
