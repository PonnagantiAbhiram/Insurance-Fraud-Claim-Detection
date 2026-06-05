import joblib
from gensim import models, corpora

encoders = joblib.load("models/label_encoders.pkl")
print("Encoders Loaded")

lda = models.LdaModel.load("models/lda_model.gensim")
print("LDA Loaded")

dictionary = corpora.Dictionary.load(
    "models/lda_dictionary.dict"
)
print("Dictionary Loaded")