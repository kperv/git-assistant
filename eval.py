import pandas as pd
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from rag import GitAssistant


class GitAssistantEvaluator:
    model_name: str = "multi-qa-MiniLM-L6-cos-v1"
    

    def __init__(self):
        self.assistant = GitAssistant()
        self.model = SentenceTransformer(model_name)

    def prepare_ground_truth_data(self):
        try:
            pairs = pd.read_csv("ground_truth.csv")
        except FileNotFoundError:
            with open('ground_truth_data.txt', 'r') as file:
                questions = [line.split(', ') for line in file]

            pairs = [{'question': q[0].strip('["\n]'), 'answer': q[1].strip('["\n]')} for q in questions]
            pairs = pd.DataFrame(pairs)
            pairs = pairs.sample(3)
        return pairs

    def add_vectors(self, pairs):
        pairs["answer_vector"] = pairs["answer"].apply(self.model.encode)
        pairs["assistant_answer_vector"] = pairs["assistant_answer"].apply(self.model.encode)
        return pairs

    def get_assistant_answers(self, pairs):
        pairs["assistant_answer"] = pairs["question"].apply(self.assistant.answer)
        return pairs

    def compute_similarity(row):
        similarity = cosine_similarity(row["answer_vector"].reshape(1, -1), row["assistant_answer_vector"].reshape(1, -1))
        return np.squeeze(similarity)

    def evaluate_similarity(self):


def main():
    pairs = prepare_ground_truth_data()
    
    assistant_pairs = get_assistant_answers(pairs, assistant)
    pairs_with_vectors = add_vectors(assistant_pairs)
    pairs_with_vectors["evaluation"] = pairs_with_vectors.apply(compute_similarity, axis=1)
    print(pairs_with_vectors.evaluation.quantile(0.75))




if __name__=="__main__":
    main()