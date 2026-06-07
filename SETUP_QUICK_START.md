# Quick Setup Guide - Insurance Fraud Detection Model

## 📌 What Was Done

✅ **Backend updated** to match `Insurance_model_fixed.ipynb`
✅ **Frontend verified** - No changes needed  
✅ **All modules aligned** - LDA, preprocessing, graph features, XGBoost
✅ **No existing logic changed** - Only enhancements

---

## 🎯 What You Need to Do

### Step 1: Run the Notebook
Execute the `Insurance_model_fixed.ipynb` to generate models:

```bash
# Navigate to the notebook location
cd backend/models/.ipynb_checkpoints/

# Open in Jupyter and run all cells
jupyter notebook Insurance_model_fixed.ipynb
```

⏱️ **Time**: ~5-10 minutes

### Step 2: Copy Generated Models
After notebook execution, copy models to backend:

```bash
# From project root
cp backend/models/.ipynb_checkpoints/Insurance_model_fixed_files/saved_models/* backend/models/
```

Or manually copy these 7 files to `backend/models/`:
- `xgboost_fraud_model.pkl`
- `scaler.pkl`
- `lda_model.gensim`
- `lda_dictionary.dict`
- `insurance_graph.pkl`
- `feature_columns.pkl`
- `target_classes.pkl` (optional)

### Step 3: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 4: Run Backend
```bash
# Terminal 1: Backend
cd backend
python app.py
# Server runs on: http://localhost:5000
```

### Step 5: Run Frontend
```bash
# Terminal 2: Frontend
cd frontend
npm install
npm run dev
# Server runs on: http://localhost:5173
```

### Step 6: Test
1. Open http://localhost:5173 in browser
2. Fill in claim form with sample data
3. Click "Analyze" button
4. View prediction results

---

## 📊 Expected Output

**Prediction Results Show:**
- ✅ Fraud/Genuine classification
- ✅ Probability percentage (0-100%)
- ✅ Risk level (High/Medium/Low)
- ✅ Confidence score
- ✅ Top contributing factors
- ✅ LDA narrative analysis
- ✅ Network visualization

---

## 🔧 Backend Modules Modified

| Module | Changes | Notes |
|--------|---------|-------|
| `lda_analysis.py` | Added stopwords, text cleaning | ✅ Matches notebook exactly |
| `preprocessing.py` | Updated scaling approach | ✅ Uses scaler.pkl |
| `xgboost_classifier.py` | Fixed prediction format | ✅ Returns percentages |
| `fusion.py` | Verified feature order | ✅ No changes needed |
| `graph_features.py` | No changes | ✅ Already correct |
| `app.py` | No changes | ✅ Already correct |

---

## ⚠️ Troubleshooting

**Models not found error:**
```
Error: No such file or directory: 'models/xgboost_fraud_model.pkl'
```
→ Solution: Run notebook and copy saved models to `backend/models/`

**CORS error:**
```
Access to XMLHttpRequest blocked by CORS
```
→ Solution: Flask backend already has CORS enabled, ensure it's running on port 5000

**Python import errors:**
```
ModuleNotFoundError: No module named 'gensim'
```
→ Solution: Run `pip install -r requirements.txt` in backend directory

**Port already in use:**
```
Address already in use: port 5000
```
→ Solution: Kill existing process or change port in `app.py` line 145

---

## 📝 File Locations

```
Fraud-claim detector/
├── VERIFICATION_REPORT.md          ← Read this for detailed info
├── SETUP_QUICK_START.md            ← You are here
├── backend/
│   ├── app.py                      ✅ No changes
│   ├── requirements.txt            ✅ All packages present
│   ├── models/
│   │   ├── .ipynb_checkpoints/
│   │   │   └── Insurance_model_fixed.ipynb  ← RUN THIS
│   │   ├── xgboost_fraud_model.pkl         ← COPY HERE
│   │   ├── scaler.pkl                      ← COPY HERE
│   │   ├── lda_model.gensim                ← COPY HERE
│   │   ├── lda_dictionary.dict             ← COPY HERE
│   │   ├── insurance_graph.pkl             ← COPY HERE
│   │   └── feature_columns.pkl             ← COPY HERE
│   └── pipeline/
│       ├── preprocessing.py        ✅ UPDATED
│       ├── lda_analysis.py         ✅ UPDATED
│       ├── xgboost_classifier.py   ✅ UPDATED
│       ├── graph_features.py       ✅ VERIFIED
│       └── fusion.py               ✅ VERIFIED
├── frontend/
│   ├── src/
│   │   ├── App.jsx                 ✅ No changes
│   │   ├── components/             ✅ No changes
│   │   └── services/api.js         ✅ No changes
│   └── package.json                ✅ All packages present
└── README.md                       (original documentation)
```

---

## 🎓 Understanding the Flow

1. **User submits claim form**
   - Frontend: React collects form data

2. **API request sent to backend**
   - Request: POST `/api/analyze` with claim details

3. **Backend processes claim**
   - Preprocess: Normalize features using scaler.pkl
   - LDA: Extract topic distributions from description
   - Graph: Calculate network centrality metrics
   - Fuse: Combine all features in order
   - Predict: XGBoost generates prediction

4. **Response returned to frontend**
   - Response: JSON with prediction, probability, risk, factors

5. **Frontend displays results**
   - Shows prediction cards, charts, network graph

---

## ✅ Verification Checklist

Before submitting claim:
- [ ] Notebook has been executed
- [ ] 7 model files exist in `backend/models/`
- [ ] `pip install -r requirements.txt` completed
- [ ] Flask running: `python app.py` (no errors)
- [ ] Frontend running: `npm run dev` (no errors)
- [ ] Browser shows form at http://localhost:5173

After first test:
- [ ] Form submits without errors
- [ ] Prediction appears (Fraud/Genuine)
- [ ] Probability shows as percentage
- [ ] Risk level displays correctly
- [ ] Contributing factors appear
- [ ] LDA analysis shows topics
- [ ] Network graph renders

---

## 📞 Need Help?

See **VERIFICATION_REPORT.md** for:
- Detailed module explanations
- Expected data formats
- Feature descriptions
- Troubleshooting tips

---

**Ready to go!** 🚀
