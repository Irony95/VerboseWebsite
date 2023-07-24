import numpy as np
import os
import pickle
import torch
import tensorflow as tf
from keybert import KeyBERT
from sentence_transformers import SentenceTransformer, util


def answer(question, note_text):
    answer_list = []
    embedder = SentenceTransformer('all-MiniLM-L6-v2')

    with open(os.getcwd() + "\\" + "\\pickle_notes\\" + note_text + "_pickle", "rb") as fp:  # Unpickling
        corpus = pickle.load(fp)

    # Corpus with note text
    corpus_embeddings = embedder.encode(corpus, convert_to_tensor=True)

    # Query sentences:
    queries = [question]

    # Find the closest 5 sentences of the corpus for each query sentence based on cosine similarity
    top_k = min(5, len(corpus))
    for query in queries:
        query_embedding = embedder.encode(query, convert_to_tensor=True)

        # We use cosine-similarity and torch.topk to find the highest 5 scores
        cos_scores = util.cos_sim(query_embedding, corpus_embeddings)[0]
        top_results = torch.topk(cos_scores, k=top_k)

        print("\n\n======================\n\n")
        print("Query:", query)
        print("\nTop 5 most similar sentences in corpus:")

        for score, idx in zip(top_results[0], top_results[1]):
            answer_list.append(corpus[idx])
            print(corpus[idx], "(Score: {:.4f})".format(score))

    return answer_list