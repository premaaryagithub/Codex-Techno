# -*- coding: utf-8 -*-
"""wine_quality.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tvZ3v3j0NRiYaXW8qAho1yknr56LOtOP
"""

wine_qt  = '1HPwGGOTCyk8zdW2pt870VkKIQb-QyMmr'
download_url1 = f'https://drive.google.com/uc?id={wine_qt}&export=download'

import pandas as pd
wine_data = pd.read_csv(download_url1, encoding='latin-1')

display(wine_data.head())

display(wine_data.shape)

display(wine_data.info())

display(wine_data.describe())

wine_data.drop_duplicates(inplace=True)   # no duplicates

display(wine_data.shape)

display(wine_data.isnull().sum())

import matplotlib.pyplot as plt
import seaborn as sns
# Set style for visualizations
sns.set_style('whitegrid')

# Distribution of wine quality
plt.figure(figsize=(10, 6))
sns.countplot(x='quality', data=wine_data)
plt.title('Distribution of Wine Quality Ratings')
plt.show()

# Correlation matrix
plt.figure(figsize=(12, 8))
corr = wine_data.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Matrix of Wine Features')
plt.show()

# Pairplot of selected features
sns.pairplot(wine_data[['fixed acidity', 'volatile acidity', 'citric acid', 'alcohol', 'quality']],
             hue='quality', palette='viridis')
plt.suptitle('Pairplot of Key Chemical Properties vs Quality', y=1.02)
plt.show()

# Boxplots of key features against quality
plt.figure(figsize=(12, 8))
sns.boxplot(x='quality', y='alcohol', data=wine_data)
plt.title('Alcohol Content by Wine Quality')
plt.show()

plt.figure(figsize=(12, 8))
sns.boxplot(x='quality', y='volatile acidity', data=wine_data)
plt.title('Volatile Acidity by Wine Quality')
plt.show()

plt.figure(figsize=(12, 8))
sns.boxplot(x='quality', y='density', data=wine_data)
plt.title('Density by Wine Quality')
plt.show()

"""Data Preprocessing :

"""

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
# Create binary classification (good/bad wine)
wine_data['quality_class'] = wine_data['quality'].apply(lambda x: 1 if x >= 6 else 0)

# Separate features and target
X = wine_data.drop(['quality', 'quality_class', 'Id'], axis=1)
y = wine_data['quality_class']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train_scaled, y_train)
rf_pred = rf.predict(X_test_scaled)

print("Random Forest Classifier:")
print(classification_report(y_test, rf_pred))
print("Accuracy:", accuracy_score(y_test, rf_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, rf_pred))

# Feature importance
plt.figure(figsize=(12, 8))
feat_importances = pd.Series(rf.feature_importances_, index=X.columns)
feat_importances.nlargest(10).plot(kind='barh')
plt.title('Top 10 Important Features - Random Forest')
plt.show()

from sklearn.linear_model import SGDClassifier



sgd = SGDClassifier(max_iter=1000, random_state=42)
sgd.fit(X_train_scaled, y_train)
sgd_pred = sgd.predict(X_test_scaled)

print("\nStochastic Gradient Descent Classifier:")
print(classification_report(y_test, sgd_pred))
print("Accuracy:", accuracy_score(y_test, sgd_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, sgd_pred))

from sklearn.svm import SVC

svc = SVC(kernel='rbf', random_state=42)
svc.fit(X_train_scaled, y_train)
svc_pred = svc.predict(X_test_scaled)

print("\nSupport Vector Classifier:")
print(classification_report(y_test, svc_pred))
print("Accuracy:", accuracy_score(y_test, svc_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, svc_pred))

# Analyzing density and acidity as predictors
plt.figure(figsize=(12, 8))
sns.scatterplot(x='density', y='fixed acidity', hue='quality_class', data=wine_data, palette='viridis')
plt.title('Density vs Fixed Acidity Colored by Quality Class')
plt.show()

plt.figure(figsize=(12, 8))
sns.scatterplot(x='pH', y='volatile acidity', hue='quality_class', data=wine_data, palette='viridis')
plt.title('pH vs Volatile Acidity Colored by Quality Class')
plt.show()

# Statistical analysis of key chemical properties
print("\nMean values by quality class:")
print(wine_data.groupby('quality_class')[['fixed acidity', 'volatile acidity', 'citric acid', 'density', 'alcohol']].mean())

