import os
from gensim import models, corpora
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')

lda_model = None
lda_dictionary = None

def load_lda_models():
    global lda_model, lda_dictionary
    try:
        lda_model = models.LdaModel.load(os.path.join(MODELS_DIR, 'lda_model.gensim'))
        lda_dictionary = corpora.Dictionary.load(os.path.join(MODELS_DIR, 'lda_dictionary.dict'))
        print("LDA models loaded successfully.")
    except Exception as e:
        print(f"Error loading LDA models: {e}")

load_lda_models()

def preprocess_text(text):
    # Simple tokenization: lowercase, remove punctuation, split by space
    text = str(text).lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text.split()

def run_lda(processed_df):
    """
    Extract LDA topic distributions and format data for the frontend.
    Returns: (lda_features_dict, lda_frontend_data)
    """
    if lda_model is None or lda_dictionary is None:
        raise RuntimeError("LDA models are not loaded.")

    description = processed_df['claim_description'].iloc[0]
    tokens = preprocess_text(description)
    
    bow = lda_dictionary.doc2bow(tokens)
    topic_distribution = lda_model.get_document_topics(bow, minimum_probability=0.0)
    
    # Extract probabilities into a feature dictionary
    # Assuming the model has a fixed number of topics (e.g., 3 or 5)
    num_topics = lda_model.num_topics
    lda_features = {f'topic_{i}': 0.0 for i in range(num_topics)}
    
    for topic_idx, prob in topic_distribution:
        lda_features[f'topic_{topic_idx}'] = float(prob)
        
    # Generate data for frontend narrative analysis cards
    # Provide top 3 topics
    sorted_topics = sorted(topic_distribution, key=lambda x: x[1], reverse=True)[:3]
    
    lda_frontend_data = []
    topic_names = ["Topic A", "Topic B", "Topic C"]
    
    for i, (topic_idx, prob) in enumerate(sorted_topics):
        # Get top words for this topic
        top_words = lda_model.show_topic(topic_idx, topn=4)
        keywords = [word for word, _ in top_words]
        
        lda_frontend_data.append({
            "title": topic_names[i] if i < len(topic_names) else f"Topic {i+1}",
            "description": f"Dominant narrative pattern detected with {prob:.1%} match.",
            "keywords": keywords,
            "probability": prob
        })

    return lda_features, lda_frontend_data
