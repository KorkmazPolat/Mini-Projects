
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import matplotlib.pyplot as plt

# --- Select 5 different categories --------------------------------
categories_5 = [
    'alt.atheism',
    'comp.sys.mac.hardware',
    'rec.autos',
    'sci.med',
    'talk.politics.guns'
]
train_5 = fetch_20newsgroups(subset='train', categories=categories_5,
                             remove=('headers', 'footers', 'quotes'))
test_5 = fetch_20newsgroups(subset='test', categories=categories_5,
                            remove=('headers', 'footers', 'quotes'))

print(f"Train samples: {len(train_5.data)}, Test samples: {len(test_5.data)}")
print("Categories:", train_5.target_names)


model_5 = make_pipeline(TfidfVectorizer(), MultinomialNB())
model_5.fit(train_5.data, train_5.target)

labels_5 = model_5.predict(test_5.data)

print("\nClassification Report (5 Categories):\n")
print(classification_report(test_5.target, labels_5, target_names=train_5.target_names))

mat_5 = confusion_matrix(test_5.target, labels_5)
plt.figure(figsize=(6, 5))
sns.heatmap(mat_5.T, square=True, annot=True, fmt='d', cbar=False,
            xticklabels=train_5.target_names, yticklabels=train_5.target_names)
plt.xlabel('True label')
plt.ylabel('Predicted label')
plt.title("Confusion Matrix - 5-Category MultinomialNB")
plt.show()