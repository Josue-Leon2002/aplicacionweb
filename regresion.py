# -*- coding: utf-8 -*-
"""Regresion.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1XXJkDCutZ0wHnrL9i9hr1ePSA8JMYkH_
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from xgboost import XGBRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from google.colab import files
import pandas as pd

uploaded = files.upload()

for file_name in uploaded.keys():
    df = pd.read_csv(file_name)
    print(f"Archivo cargado: {file_name}")
    print(df.head())

df = pd.read_csv("dataset_transacciones_sintetico.csv")

categorical_cols = ['device_type', 'merchant_category', 'customer_segment',
                    'email_domain_type', 'customer_tenure_level', 'txn_hour_category']

le = LabelEncoder()
for col in categorical_cols:
    df[col] = le.fit_transform(df[col])

X = df.drop(columns=['transaction_id', 'amount', 'is_fraud'])  # Predictoras
y = df['amount']

print(df.head())

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

def eval_regression(y_true, y_pred):
    return {
        'MAE': mean_absolute_error(y_true, y_pred),
        'RMSE': mean_squared_error(y_true, y_pred, squared=False),
        'R2': r2_score(y_true, y_pred)
    }

def eval_regression(y_true, y_pred):
    # Calculate MSE and then take the square root for RMSE if squared parameter is not available
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    return {
        'MAE': mean_absolute_error(y_true, y_pred),
        'RMSE': rmse,  # Use calculated RMSE
        'R2': r2_score(y_true, y_pred)
    }

import numpy as np

model_svr = SVR(kernel='rbf', C=100)
model_svr.fit(X_train, y_train)
pred_svr = model_svr.predict(X_test)
metrics_svr = eval_regression(y_test, pred_svr)

model_xgb = XGBRegressor(objective='reg:squarederror', n_estimators=100)
model_xgb.fit(X_train, y_train)
pred_xgb = model_xgb.predict(X_test)
metrics_xgb = eval_regression(y_test, pred_xgb)

model_nn = MLPRegressor(hidden_layer_sizes=(64, 32), max_iter=300)
model_nn.fit(X_train, y_train)
pred_nn = model_nn.predict(X_test)
metrics_nn = eval_regression(y_test, pred_nn)

model_lr = LinearRegression()
model_lr.fit(X_train, y_train)
pred_lr = model_lr.predict(X_test)
metrics_lr = eval_regression(y_test, pred_lr)

print("Regresión Lineal:", metrics_lr)
print("SVM Regressor:", metrics_svr)
print("XGBoost Regressor:", metrics_xgb)
print("Neural Network Regressor:", metrics_nn)

import matplotlib.pyplot as plt
import seaborn as sns

metrics_all = {
    'Regresión Lineal': metrics_lr,
    'SVM': metrics_svr,
    'XGBoost': metrics_xgb,
    'Red Neuronal': metrics_nn
}

metrics_df = pd.DataFrame(metrics_all).T  # Transpuesta para que los modelos sean las filas
metrics_df.reset_index(inplace=True)
metrics_df.rename(columns={'index': 'Modelo'}, inplace=True)

plt.figure(figsize=(12, 6))
metrics_melted = metrics_df.melt(id_vars='Modelo', var_name='Métrica', value_name='Valor')
sns.barplot(data=metrics_melted, x='Modelo', y='Valor', hue='Métrica')
plt.title('Comparación de Métricas de Regresión por Modelo')
plt.ylabel('Valor')
plt.xticks(rotation=15)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

model_preds = {
    'Regresión Lineal': pred_lr,
    'SVM': pred_svr,
    'XGBoost': pred_xgb,
    'Red Neuronal': pred_nn
}
plt.figure(figsize=(16, 10))
for i, (name, pred) in enumerate(model_preds.items(), 1):
    plt.subplot(2, 2, i)
    sns.scatterplot(x=y_test, y=pred, alpha=0.3)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')  # Línea ideal
    plt.title(f'{name} - Real vs Predicho')
    plt.xlabel('Real')
    plt.ylabel('Predicho')

plt.tight_layout()
plt.show()