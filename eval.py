import pandas as pd
from tqdm import tqdm
from sentence_transformers import SentenceTransformer


model_name: str = "multi-qa-MiniLM-L6-cos-v1"
model = SentenceTransformer(model_name)

def prepare_ground_truth_data():
    with open('ground_truth_data.txt', 'r') as file:
        questions = [line.split(', ') for line in file]

    print(len(questions))
    pairs = [{'id': i, 'question': q[0].strip('["\n]'), 'answer': q[1].strip('["\n]')} for i, q in enumerate(questions)]
    return pairs

def add_vectors(pairs):
    for pair in pairs:
        pair["question_vector"] = model.encode(pair["question"])
        pair["question_answer"] = model.encode(pair["answer"])
    return pairs

def main():
    pairs = prepare_ground_truth_data()
    pairs_with_vectors = add_vectors(pairs)
    for pair in pairs_with_vectors:
        print(pair)



if __name__=="__main__":
    main()