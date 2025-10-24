import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import re
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
import mysql.connector

app = Flask(__name__)

UPLOAD_FOLDER = 'D:/python/resume_screening_app/uploads/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load the dataset
df = pd.read_csv('UpdatedResumeDataSet.csv')

# Define a function to clean resume text
def cleanResume(txt):
    cleanText = re.sub(r'http\S+\s', ' ', txt)
    cleanText = re.sub(r'#\S+\s', ' ', cleanText)
    cleanText = re.sub(r'@\S+', '  ', cleanText)
    cleanText = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'\s+', ' ', cleanText)
    return cleanText

# Clean the resume text
df['Resume'] = df['Resume'].apply(lambda x: cleanResume(x))

# Encode the 'Category' column
le = LabelEncoder()
df['Category'] = le.fit_transform(df['Category'])

# Initialize the TfidfVectorizer
tfidf = TfidfVectorizer(stop_words='english')

# Fit the TfidfVectorizer with the vocabulary from the training data
tfidf.fit(df['Resume'])

# Transform the resume text into TF-IDF features
requiredText = tfidf.transform(df['Resume'])

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(requiredText, df['Category'], test_size=0.2, random_state=42)

# Train the classifier
clf = OneVsRestClassifier(KNeighborsClassifier())
clf.fit(X_train, y_train)

# Define the category mapping dictionary
category_mapping = {
    0: "Advocate",
    1: "Arts",
    2: "Automation Testing",
    3: "Blockchain",
    4: "Business Analyst",
    5: "Civil Engineer",
    6: "Data Science",
    7: "Database",
    8: "DevOps Engineer",
    9: "DotNet Developer",
    10: "ETL Developer",
    11: "Electrical Engineering",
    12: "HR",
    13: "Hadoop",
    14: "Health and fitness",
    15: "Java Developer",
    16: "Mechanical Engineer",
    17: "Network Security Engineer",
    18: "Operations Manager",
    19: "PMO",
    20: "Python Developer",
    21: "SAP Developer",
    22: "Sales",
    23: "Testing",
    24: "Web Designing",
}

# Function to get database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        port=3307,  # Adjust port to 3307
        user='root',  # replace with your database user
        password='',  # replace with your database password
        database='job_applications'
    )

# Function to send email
def send_email(to_address, subject, message):
    # Hardcoded email address and password
    email_address = 'cs201230@dsu.edu.pk'
    email_password = 'iqil ktdb bjyz rqyj'  # Use app-specific password if 2-Step Verification is enabled

    msg = MIMEMultipart()
    msg['From'] = email_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_address, email_password)
        text = msg.as_string()
        server.sendmail(email_address, to_address, text)
        server.quit()
        print('Email sent successfully!')
    except smtplib.SMTPAuthenticationError as e:
        print(f'SMTPAuthenticationError: {e}')
    except Exception as e:
        print(f'Exception occurred while sending email: {e}')

# Define route to handle file upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']

        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Read the file with the correct encoding
            with open(file_path, 'r', encoding='latin-1') as f:
                resume_content = f.read()

            # Further processing based on the prediction from resume analyzer
            cleaned_resume = cleanResume(resume_content)
            input_features = tfidf.transform([cleaned_resume])
            prediction_id = clf.predict(input_features)[0]
            category_name = category_mapping.get(prediction_id, "Unknown")

            # If the prediction matches your requirement, save candidate details to the database
            if category_name == "Python Developer":  # Replace "Python Developer" with the actual category name
                # Save candidate details to the database
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO applications (name, email, phone, position, resume_path) VALUES (%s, %s, %s, %s, %s)',
                    (name, email, phone, position, file_path)
                )
                conn.commit()
                cursor.close()
                conn.close()

                # Send email to the candidate
                subject = "Interview Appointment Confirmation"
                message = f"Dear {name},\n\nThank you for applying for the {position} position. We are pleased to inform you that you have been shortlisted for an interview. Please find the details below:\n\nDate: [Date]\nTime: [Time]\nAddress: [Address]\n\nWe look forward to meeting you.\n\nBest regards,\nRecruitment Team"
                send_email(email, subject, message)

                return 'Candidate details saved to the database and email sent successfully!'
            else:
                # Remove the uploaded file if it does not meet requirements
                os.remove(file_path)
                return 'Sorry, your resume does not meet our requirements.'

    return render_template('upload.html')

# Add a basic route for the home page
@app.route('/')
def home():
    return 'Welcome to the Resume Screening App! Go to /upload to upload a resume.'

if __name__ == '__main__':
    app.run(debug=True, port=3307)
