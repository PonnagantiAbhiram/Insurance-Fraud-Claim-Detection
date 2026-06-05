## Installation Guide

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Fraud-claim-detector
```

### 2. Backend Setup

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

Start the Flask backend server:

```bash
cd backend
python app.py
```

Backend runs on:

```text
http://localhost:5000
```

---

### 3. Frontend Setup

Navigate to frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

### 4. Run the Application

1. Start the Flask backend.
2. Start the React frontend.
3. Open the frontend URL in your browser.
4. Submit an insurance claim for fraud analysis.
