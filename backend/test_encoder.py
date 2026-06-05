import joblib

encoders = joblib.load("models/label_encoders.pkl")
print(type(encoders))
print("Encoders OK")