# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# import pandas as pd


# rfc = RandomForestClassifier(n_estimators=100, random_state=42)
# data = pd.read_csv('Data/data1.csv')

# data=data.drop('Soil type',axis=1)
# data=data.drop('Fertilizer Name', axis=1)
# data['Crop'] = data['Crop'].fillna(data['Crop'].mode()[0])
# data['OC'] = data['OC'].fillna(data['OC'].mode()[0])
# X = data.drop('Crop', axis=1)
# y = data['Crop']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
# def crop_model(input_values):
#     proba = rfc.predict_proba(input_values[0])
#     # Get three fertilizer with highest probability
#     recommended_crop = []
#     for i in range(3):
#         max_proba = max(proba)
#         max_index = list(proba).index(max_proba)
#         recommended_crop.append(rfc.classes_[max_index])
#         proba[max_index] = -1
#     return recommended_crop