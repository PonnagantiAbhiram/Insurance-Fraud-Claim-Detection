import pickle
with open("models/label_encoders.pkl", "rb") as f:
    encoders = pickle.load(f)

for k,v in encoders.items():
    print("\n",k)
    print(v.classes_)