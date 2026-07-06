from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')


def get_embedding(text):
    return model.encode(text).tolist()


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def search_top_k(query, notes, k=5):
    query_embedding = np.array(get_embedding(query))

    results = []

    for note in notes:
        if not note.embedding:
            continue

        note_embedding = np.array(note.embedding)

        score = cosine_similarity(
            [query_embedding],
            [note_embedding]
        )[0][0]

        results.append({
            "title": note.title,
            "content": note.content,
            "score": float(score)
        })

    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:k]

CATEGORY_DESCRIPTIONS = {
    "AI": "artificial intelligence machine learning neural networks intelligent systems",
    "ML": "machine learning supervised unsupervised regression classification",
    "DL": "deep learning cnn rnn transformer pytorch tensorflow",
    "NLP": "natural language processing bert llm chatbot token embedding text",
    "CV": "computer vision yolo object detection segmentation images",
    "Programming": "python java c++ javascript coding algorithm software",
    "Other": "general notes"
}

category_embeddings = {
    name: np.array(get_embedding(text))
    for name, text in CATEGORY_DESCRIPTIONS.items()
}


def suggest_category(text):
    note_embedding = np.array(get_embedding(text))

    best_category = "Other"
    best_score = -1

    for category, embedding in category_embeddings.items():

        score = cosine_similarity(
            [note_embedding],
            [embedding]
        )[0][0]

        if score > best_score:
            best_score = score
            best_category = category

    return best_category


from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

def summarize_text(text):

    parser = PlaintextParser.from_string(
        text,
        Tokenizer("english")
    )

    summarizer = LsaSummarizer()

    summary = summarizer(
        parser.document,
        2
    )

    summary_text = " ".join(str(sentence) for sentence in summary)

    if summary_text.strip() == "":
        return text

    return summary_text