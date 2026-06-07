import os
from gensim import models, corpora
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

lda_model = None
lda_dictionary = None

STOPWORDS = {
    "the","a","an","and","or","in","on","of","to","is","it","this","that",
    "was","for","with","as","at","by","from","be","are","has","have","had",
    "were","been","not","no","but","if","so","do","did","does","its","their",
    "there","about","which","all","also","though","involves","reported",
    "claim","amount",
}

def load_lda_models():
    global lda_model, lda_dictionary
    try:
        lda_model = models.LdaModel.load(os.path.join(MODELS_DIR, 'lda_model.gensim'))
        lda_dictionary = corpora.Dictionary.load(os.path.join(MODELS_DIR, 'lda_dictionary.dict'))
        print("LDA models loaded successfully.")
    except Exception as e:
        print(f"Error loading LDA models: {e}")

load_lda_models()

def clean_text(text: str) -> list:
    text = str(text).lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = [t for t in text.split() if t not in STOPWORDS and len(t) > 2]
    return tokens

def run_lda(processed_df):
    if lda_model is None or lda_dictionary is None:
        raise RuntimeError("LDA models are not loaded.")

    description = processed_df['claim_description'].iloc[0]
    tokens = clean_text(description)
    bow = lda_dictionary.doc2bow(tokens)
    topic_distribution = lda_model.get_document_topics(bow, minimum_probability=0.0)

    num_topics = lda_model.num_topics

    # -------------------------------------------------------
    # FIX: model expects topic_1..topic_5 (1-indexed)
    # but lda returns 0-indexed. Shift by +1.
    # -------------------------------------------------------
    lda_features = {f'topic_{i+1}': 0.0 for i in range(num_topics)}
    for topic_idx, prob in topic_distribution:
        lda_features[f'topic_{topic_idx+1}'] = float(prob)

    # Frontend data (top 3 topics)
    sorted_topics = sorted(topic_distribution, key=lambda x: x[1], reverse=True)[:3]
    topic_names = ["Topic A", "Topic B", "Topic C"]
    lda_frontend_data = []

    for i, (topic_idx, prob) in enumerate(sorted_topics):
        top_words = lda_model.show_topic(topic_idx, topn=4)
        keywords = [word for word, _ in top_words]
        lda_frontend_data.append({
            "title": topic_names[i] if i < len(topic_names) else f"Topic {i+1}",
            "description": f"Dominant narrative pattern detected with {prob:.1%} match.",
            "keywords": keywords,
            "probability": prob
        })

    return lda_features, lda_frontend_data