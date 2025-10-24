**🧠 AI Resume Screening App
📌 Overview**

This project is an AI-powered Resume Classification Web App that automatically analyzes and categorizes resumes based on skills and content.
It uses Machine Learning (with Scikit-learn and TF-IDF vectorization) to predict the relevant job domain or skill category for uploaded resumes.

**⚙️ Features**

📂 Upload resume files (PDF/DOCX)

🧠 Automatically analyze and classify resumes using ML

📊 Uses TF-IDF and a trained classification model (clf.pkl)

🌐 Simple Flask-based web interface

💾 Stores uploaded resumes in the uploads/ directory

🔐 Supports environment variable configuration via .env file

**🧩 Project Structure**

├── Mydatabase/                 # Database files or local storage
├── templates/                  # HTML templates for Flask
├── uploads/                    # Uploaded resume files
├── venv/                       # Virtual environment
├── UpdatedResumeDataSet.csv    # Training dataset
├── app.py                      # Flask web app entry point
├── clf.pkl                     # Trained classification model
├── tfidf.pkl                   # TF-IDF vectorizer
├── resume1.py                  # Model training / preprocessing script
├── hrcredentials.env.txt       # Environment variable configuration
├── tempCodeRunnerFile.py       # Temp / test file
├── tuutuu.c                    # Unrelated C test file

**🚀 How to Run

1️⃣ Clone the Repository**
``bash
git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>``

**2️⃣ Create and Activate Virtual Environment**
``bash
python -m venv venv
venv\Scripts\activate    # On Windows
source venv/bin/activate # On Mac/Linux
``
**3️⃣ Install Dependencies**
``
pip install -r requirements.txt
``

(If you don’t have a requirements.txt, generate one using pip freeze > requirements.txt.)

**4️⃣ Run the App**
``
python app.py
``

Then open the browser and go to:
``
http://127.0.0.1:5000
``
**🧠 Model Details**

Vectorizer: TF-IDF (tfidf.pkl)

Classifier: Likely Logistic Regression / Random Forest (clf.pkl)

Dataset: UpdatedResumeDataSet.csv used for training

**🧾 Environment Variables**

Use the hrcredentials.env.txt file to store sensitive data like API keys or credentials.

Example:
``
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_password
SECRET_KEY=some_secret_key
``

**📈 Future Improvements**

Add multi-class support for more job categories

Improve preprocessing (NER, lemmatization)

Integrate database for better resume management

Add dashboard for analytics
