"""
mbti.py
Topic: Predicting Myers-Briggs Personality Type From Online Language Style
"""

import pandas as pd
from google.colab import files
uploaded = files.upload()

import io
df = pd.read_csv(io.BytesIO(uploaded["mbti_1.csv"]))

df.isna().sum()
df.loc[:,"posts"].replace(r'\||||', '', regex=True, inplace=True)
df.loc[:, "posts"].replace(r'\_____|', '', regex=True, inplace=True)
df.loc[:, "posts"].replace(r'@.@|', '', regex=True, inplace=True)
df.loc[:, "posts"].replace(r'\a|', '', regex=True, inplace=True)
df.loc[:, "posts"].replace(r'\an|', '', regex=True, inplace=True)
df.loc[:, "posts"].replace(r'\the|', '', regex=True, inplace=True)


df["type"].unique()
df["type"].value_counts()

#Bar graph of the original distribution
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize = (15, 5))
cnt = df["type"].value_counts()
sns.barplot(x=cnt.index, y=cnt.values,alpha=0.8, palette="rainbow")

plt.title("Original Distribution of Personality Types")
plt.xlabel("Personality Type")
plt.ylabel("Number of Each Type")

import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
label = preprocessing.LabelEncoder()
df["label"] = label.fit_transform(df["type"])
df[df["label"]==12]

import seaborn as sns
import matpltotal_posts = df.groupby(["type"]).count()*50
otlib.pyplot as plt
sns.barplot(x=total_posts.index, y=total_posts["posts"], width=0.8)
plt.title("Number of Posts from Each Personality Type")
plt.xlabel("Personality Type")
plt.ylabel("Number of posts")

df['posts'] = df['posts'].str.replace('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', ' ')
df["posts"] = df["posts"].str.replace(r"[\"\'\|\?\=\.\@\#\*\,____]", '')
df["posts"] = df["posts"].str.replace(r"[INFJ', 'ENTP', 'INTP', 'INTJ', 'ENTJ', 'ENFJ', 'INFP', 'ENFP','ISFP', 'ISTP', 'ISFJ', 'ISTJ', 'ESTP', 'ESFP', 'ESTJ', 'ESFJ]", ' ')

df["word_count"] = df["posts"].str.split().str.len()
df["character count"] = df["posts"].str.len()
df["characters_per_word"] = df["character count"]/df["word_count"]
df["num"] = df["posts"].apply(lambda x: len([x for x in x.split() if x.isdigit()]))


#Sentiment Analysis
from textblob import TextBlob
import re

def sentiment(text):
  analysis = TextBlob(text)
  if analysis.sentiment.polarity > 0:
    return "positive"
  elif analysis.sentiment.polarity < 0:
    return "negative"
  elif analysis.sentiment.polarity == 0:
    return "neutral"

for index, row in df.iterrows():
  df.loc[index,"sentiment_value"] = TextBlob(df.iloc[index]["posts"]).sentiment.polarity
  df.loc[index,"sentiment_emotion"] = sentiment(df.iloc[index]["posts"])
df.head()

#Sentiment Analysis Visualization
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(20, 10))

sns.swarmplot(data=df,
              x="type",
              y="sentiment_value",
              hue="sentiment_emotion")

plt.figure(figsize=(7, 7))
sns.boxplot(y="type", x="sentiment_value", data=df, showfliers=False)

# Machine Learning Methods
from sklearn import preprocessing

from sklearn.model_selection import train_test_split
label = preprocessing.LabelEncoder()
df["label"] = label.fit_transform(df["type"])
df["emotion_indicator"] = label.fit_transform(df["sentiment_emotion"])
features = ["word_count",	"character count",	"characters_per_word",	"num",	"sentiment_value",	"emotion_indicator"]
X = df[features]
y = df["label"]

#df["type"].unique()

#K Neigbhors Classifier -
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.80, test_size=0.20, random_state=490)
knn = KNeighborsClassifier(n_neighbors = 5)
fit_model = knn.fit(X_train, y_train)
pred_type = knn.predict(X_test)
print(fit_model)
pred_df = pd.DataFrame(pred_type)
pred_df.columns = ["labels predicted"]
yt_df = pd.DataFrame(y_test).head()
yt_df.columns = ["actual labels"]
yt_df.head()

from warnings import simplefilter
from sklearn.metrics import classification_report
simplefilter(action='ignore', category=FutureWarning)
train_score = knn.score(X_train, y_train)
test_score = knn.score(X_test, y_test)
score_dict = {"Accuracy for Training set":[train_score], "Accuracy for Testing Set":[test_score]}
score_pd = pd.DataFrame(score_dict)
score_pd.rename({0:"Scores"})
tar_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"," 10", "11", "12", "13", "14", "15"]
class_report = classification_report(y_test, pred_type, target_names=tar_names)
print(class_report)

#SVM
from sklearn.svm import SVC

SVC_model = SVC(kernel="linear", C=100)
fit_model = SVC_model.fit(X_train, y_train)

pred_type = SVC_model.predict(X_test)

#SVM

train_score = SVC_model.score(X_train, y_train)
test_score = SVC_model.score(X_test, y_test)

score_dict = {"Accuracy for Training set":[train_score], "Accuracy for Testing Set":[test_score]}
score_pd = pd.DataFrame(score_dict)
score_pd.rename({0:"Scores"})

#SVM

tar_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"," 10", "11", "12", "13", "14", "15"]
class_report = classification_report(y_test, pred_type, target_names=tar_names)
print(class_report)

#SVM
pred_df = pd.DataFrame(pred_type)
pred_df.columns = ["labels predicted"]
yt_df = pd.DataFrame(y_test).head()
yt_df.columns = ["labels"]

pred_df = pd.DataFrame(pred_type)
pred_df.columns = ["labels predicted"]
yt_df = pd.DataFrame(y_train).head()
yt_df.columns = ["labels"]

#Decision Tree
from sklearn.tree import DecisionTreeClassifier
tree_dt = DecisionTreeClassifier(max_depth=2, random_state=490, criterion="entropy")
tree_model = tree_dt.fit(X_train, y_train)

train_score = tree_dt.score(X_train, y_train)
test_score = tree_dt.score(X_test, y_test)
score_dict = {"Accuracy for Training set":[train_score], "Accuracy for Testing Set":[test_score]}
score_pd = pd.DataFrame(score_dict)
score_pd.rename({0:"Scores"})

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
predt = tree_dt.predict(X_test)

tar_names = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"," 10", "11", "12", "13", "14", "15"]
class_report = classification_report(y_test, predt, target_names=tar_names)
#print(class_report)
predt_df = pd.DataFrame(predt)
y_test

import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
from sklearn.inspection import DecisionBoundaryDisplay
import matplotlib.pyplot as plt
plt.figure(figsize=(20,8), tight_layout=True)
plot_tree(tree_model, feature_names=['word_count', 'character count','characters_per_word', 'num', 'emotion_indicator','sentiment_value'], class_names=df["type"], fontsize=8)
#plt.show()
plt.savefig("DT.png")

#df["label"].unique()
#df["type"].unique()
