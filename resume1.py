import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import pickle
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the dataset
df = pd.read_csv('UpdatedResumeDataSet.csv')

# Define a function to clean resume text
# Modify the cleanResume function to accept file content instead of a string path
def cleanResume(content):
    cleanText = re.sub(r'http\S+\s', ' ', content)
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

# Evaluate the classifier
ypred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, ypred))

# Save the trained models
with open('tfidf.pkl', 'wb') as f:
    pickle.dump(tfidf, f)

with open('clf.pkl', 'wb') as f:
    pickle.dump(clf, f)

# Load the trained classifier
with open('clf.pkl', 'rb') as f:
    clf = pickle.load(f)

# Load the cleaned resume
myresume ="""As an accomplished professional with over a decade of experience in diverse industries, I have honed a unique skill set that spans finance, marketing, and technology. My journey began in finance, where I developed a deep understanding of financial markets and investment strategies. Transitioning into marketing, I led successful campaigns that propelled brand awareness and drove significant revenue growth.

In recent years, my focus has shifted towards technology, particularly in the field of artificial intelligence and machine learning. I have spearheaded projects that leverage cutting-edge AI algorithms to solve complex business problems and enhance operational efficiency. My expertise extends to natural language processing, computer vision, and predictive analytics.

I thrive in dynamic environments where innovation is encouraged, and challenges are viewed as opportunities for growth. My ability to adapt quickly to new technologies and methodologies has been instrumental in driving successful outcomes across various projects. I am adept at collaborating with cross-functional teams, communicating technical concepts to non-technical stakeholders, and delivering solutions that exceed expectations.

Beyond my professional endeavors, I am passionate about contributing to the community through mentorship programs and volunteering initiatives. I believe in the power of education to transform lives and am committed to empowering the next generation of leaders in STEM fields.

Contact Information:
Email: johndoe@example.com
Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johndoe
GitHub: github.com/johndoe

Skills:
- Financial Analysis
- Marketing Strategy
- Artificial Intelligence
- Machine Learning
- Natural Language Processing
- Computer Vision
- Predictive Analytics
- Project Management
- Leadership
- Communication


"""



cleaned_resume = cleanResume(myresume)

input_features = tfidf.transform([cleaned_resume])

prediction_id = clf.predict(input_features)[0]


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

category_name = category_mapping.get(prediction_id, "Unknown")
print("Predicted Category:", category_name)
print("Category ID:", prediction_id)


