'''
AUTORES:
    Felipe Kuznik Thome 
    Kurt Cobain Rodrigues 
    Pedro Henrique Ghinzelli do Nascimento
'''

# BIBLIOTECAS 
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib
import numpy as np
from sklearn.metrics import mean_squared_error

# CARREGA DADOS DO CSV
dados = pd.read_csv("../dados/kc_house_data2_moderadamente_modificado.csv")

# SEPARA COLUNAS DE ENTRADAS
colunas_entrada = [
    "bedrooms", "bathrooms", "sqft_living", "sqft_lot", "floors",
    "waterfront", "view", "condition", "grade", "sqft_above",
    "sqft_basement", "yr_built", "yr_renovated",
    "lat", "long", "sqft_living15", "sqft_lot15"
]

# CARREGA OS DADOS DO CSV PARA X E Y
X = dados[colunas_entrada]
y = dados["price"]

# SEPARADO DADOS EM TREINO, VALIDAÇÃO E TESTE (70/15/15)
X_train, X_temp, y_train, y_temp = train_test_split(
    X, y, test_size=0.3, random_state=42
)
X_val, X_test, y_val, y_test = train_test_split(
    X_temp, y_temp, test_size=0.5, random_state=42
)

# AJUSTA OS DADOS, NORMALIZA
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_val = scaler.transform(X_val)
X_test = scaler.transform(X_test)

# NORMALIZA O PREÇO TAMBÉM
scaler_y = StandardScaler()
y_train_norm = scaler_y.fit_transform(y_train.values.reshape(-1, 1)).ravel()

# ESCOLHA DAS COMBINAÇÕES DOS HIPERPARÂMETROS!
param_grid = {
    "hidden_layer_sizes": 
    [
        
        (8, 17)       # CAMADAS OCULTAS E SEUS NEURONIOS
        
     ],
    "activation": ["relu", "tanh"],                           # FUNÇÃO DE ATIVAÇÃO
    "alpha": [0.0001, 0.001],                                 # REGULARIZAÇÃO L2
    "learning_rate": ["constant", "adaptive"]                 # TAXA DE APRENDIZADO
}

# BUSCA DOS MELHORES HIPERPARÂMETROS COM GRID_SEARCH (!!! DEMORA !!!)
grid_search = GridSearchCV(
    MLPRegressor(solver="adam", max_iter=1000, random_state=42),
    param_grid,
    n_jobs=-1,
    cv=5
)
grid_search.fit(X_train, y_train_norm)

# SELEÇÃO DO MELHOR MODELO
print(f"Melhores parametros encontreados: {grid_search.best_params_}\n")
modelo = grid_search.best_estimator_

# AVALIA O MODELO NO CONJUNTO DE VALIDAÇÃO
y_pred_val_norm = modelo.predict(X_val)
y_pred_val = scaler_y.inverse_transform(y_pred_val_norm.reshape(-1, 1)).ravel() # desnormaliza valor
print(f"[Validacao] Erro medio da previsao (MAE): R$ {mean_absolute_error(y_val, y_pred_val):,.2f}")
print(f"[Validacao] Qualidade do ajuste do modelo (R^2): {r2_score(y_val, y_pred_val):.2%}\n")

# AVALIA O MODELO NO CONJUNTO DE TESTES
y_pred_norm = modelo.predict(X_test)
y_pred = scaler_y.inverse_transform(y_pred_norm.reshape(-1, 1)).ravel()
print(f"[Teste] Erro medio da previsao (MAE): R$ {mean_absolute_error(y_test, y_pred):,.2f}")
print(f"[Teste] Qualidade do ajuste do modelo (R^2): {r2_score(y_test, y_pred):.2%}")

######### RESULTADOS E ANALISES #############

# ERROS INDIVIDUAIS
erros_percentuais = np.abs(
    (y_test.values - y_pred) / y_test.values
) * 100

# MÉTRICAS
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mape = np.mean(erros_percentuais)
mediana = np.median(erros_percentuais)
p90 = np.percentile(erros_percentuais, 90)
p95 = np.percentile(erros_percentuais, 95)
pior = np.max(erros_percentuais)

# IMPRIMIR AS MÉTRICAS
print(f"RMSE: R$ {rmse:,.2f}")
print(f"MAPE: {mape:.2f}%")
print(f"Mediana do erro: {mediana:.2f}%")
print(f"90% dos erros: abaixo de {p90:.2f}%")
print(f"95% dos erros: abaixo de {p95:.2f}%")
print(f"Pior erro: {pior:.2f}%")

# TABELAS PARA IMPRIMIR E ANALISAR OS PIORES IMÓVEIS E SUAS CARACTERISTICAS
resultado = pd.DataFrame({
    'real': y_test,
    'previsto': y_pred,
    'erro': abs(y_test - y_pred),
    'erro_percentual': (abs(y_test - y_pred) / y_test) * 100
}, index=y_test.index) 

resultado["erro"] = resultado["previsto"] - resultado["real"]

resultado["erro_percentual"] = (
    np.abs(resultado["erro"] / resultado["real"]) * 100
)

print(
    resultado
    .sort_values("erro_percentual", ascending=False)
    .head(20)
)

piores = resultado.sort_values(
    "erro_percentual",
    ascending=False
).head(10)

print(dados.loc[piores.index])

# SALVAR O MODELO TREINADO E OS SCALERS
joblib.dump(modelo, "modelo_precos.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(scaler_y, "scaler_y.pkl")
joblib.dump(colunas_entrada, "colunas_entrada.pkl")

print("Modelo, scaler e lista de colunas salvos na pasta modelos/")