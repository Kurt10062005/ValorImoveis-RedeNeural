'''
AUTORES:
    Felipe Kuznik Thome 
    Kurt Cobain  Rodrigues 
    Pedro Henrique Ghinzelli do Nascimento
'''

import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# carrega os dados
dados = pd.read_csv("../dados/kc_house_data.csv")

# colunas de entrada
colunas_entrada = [
    "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors",
    "waterfront", "view", "condition", "grade", "sqft_above",
    "sqft_basement", "yr_built", "yr_renovated", "zipcode",
    "lat", "long", "sqft_living15", "sqft_lot15"
]

X = dados[colunas_entrada]
y = dados["price"]

# separa dados treino e teste
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ajusta os dados
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# busca hiperparametros com Grid Search
# !!!demora!!!
param_grid = {
    "hidden_layer_sizes": [(100, 50, 25)],
    "activation": ["relu", "tanh"],
    "alpha": [0.0001, 0.001],
    "learning_rate": ["constant", "adaptive"]
}

grid_search = GridSearchCV(
    MLPRegressor(solver="adam", max_iter=1000, random_state=42),
    param_grid,
    n_jobs=-1,
    cv=5
)
grid_search.fit(X_train, y_train)

print("Melhores parametros encontrados:", grid_search.best_params_)
modelo = grid_search.best_estimator_

# avaliar o modelo no conjunto de teste
y_pred = modelo.predict(X_test)
print(f"MAE (erro medio absoluto): {mean_absolute_error(y_test, y_pred):.2f}")
print(f"R^2: {r2_score(y_test, y_pred):.4f}")

# salvar o modelo treinado e o scaler
joblib.dump(modelo, "modelo_precos.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(colunas_entrada, "colunas_entrada.pkl")

print("Modelo, scaler e lista de colunas salvos na pasta modelos/")