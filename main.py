'''
AUTORES:
    Felipe Kuznik Thome 
    Kurt Cobain  Rodrigues 
    Pedro Henrique Ghinzelli do Nascimento
'''

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# carrega modelo treinado, scaler e lista de colunas (uma ves so) qd o server liga
modelo = joblib.load("modelos/modelo_precos.pkl")
scaler = joblib.load("modelos/scaler.pkl")
colunas_entrada = joblib.load("modelos/colunas_entrada.pkl")

# Carrega a base de dados das casas para simulação
df_casas = pd.read_csv("dados/kc_house_data.csv")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )

#Função para a interface do lado direito
@app.get("/simular-aleatorio")
def simular_aleatorio():
    # Seleciona uma casa aleatória do dataset (com ID entre 1 milhão e 9.9 bilhões)
    casa_amostra = df_casas.sample(n=1).iloc[0].to_dict()

    # Mapeamento do CSV para os nomes dos campos do formulário de simulação
    dados_simulacao = {
        "id": int(casa_amostra["id"]),
        "quartos": float(casa_amostra["bedrooms"]),
        "banheiros": float(casa_amostra["bathrooms"]),
        "area_living": float(casa_amostra["sqft_living"]),
        "area_lote": float(casa_amostra["sqft_lot"]),
        "andares": float(casa_amostra["floors"]),
        "waterfront": int(casa_amostra["waterfront"]),
        "view": int(casa_amostra["view"]),
        "conservacao": int(casa_amostra["condition"]),
        "grade": int(casa_amostra["grade"]),
        "area_shove": float(casa_amostra["sqft_above"]),
        "area_basement": float(casa_amostra["sqft_basement"]),
        "ano_construcao": int(casa_amostra["yr_built"]),
        "ano_reforma": int(casa_amostra["yr_renovated"]),
        "cep": int(casa_amostra["zipcode"]),
        "lat": float(casa_amostra["lat"]),
        "long": float(casa_amostra["long"]),
        "area_living15": float(casa_amostra["sqft_living15"]),
        "area_lote15": float(casa_amostra["sqft_lot15"]),
        "preco_real": float(casa_amostra["price"]),
    }
    return dados_simulacao

# recebe os dados que o usuer preencheu no form do site e devolve o preco da RNA
@app.post("/enviar")
def prever_preco(
    quartos: float = Form(...),
    banheiros: float = Form(...),
    area_living: float = Form(...),
    area_lote: float = Form(...),
    andares: float = Form(...),
    waterfront: int = Form(...),
    view: int = Form(...),
    conservacao: int = Form(...),
    grade: int = Form(...),
    area_shove: float = Form(...),
    area_basement: float = Form(...),
    ano_construcao: int = Form(...),
    ano_reforma: int = Form(...),
    cep: int = Form(...),
    lat: float = Form(...),
    long: float = Form(...),
    area_living15: float = Form(...),
    area_lote15: float = Form(...),
):
    # coloca dados recebidos num dicionario (usa nomes das colunas iguasi oas do treino (dados/kc_house_data.csv)
    dados_recebidos = {
        "bedrooms": quartos,
        "bathrooms": banheiros,
        "sqft_living": area_living,
        "sqft_lot": area_lote,
        "floors": andares,
        "waterfront": waterfront,
        "view": view,
        "condition": conservacao,
        "grade": grade,
        "sqft_above": area_shove,
        "sqft_basement": area_basement,
        "yr_built": ano_construcao,
        "yr_renovated": ano_reforma,
        "zipcode": cep,
        "lat": lat,
        "long": long,
        "sqft_living15": area_living15,
        "sqft_lot15": area_lote15,
    }

    # monta a lista de valores (ordem igual o treino (colunas_entrada.pkl))
    entrada = [dados_recebidos[coluna] for coluna in colunas_entrada]

    # aplica o mesmo padrao (StandardScaler) do treino
    entrada_padronizada = scaler.transform([entrada])

    # pede a previsao do modelo
    preco_previsto = modelo.predict(entrada_padronizada)[0]

    # devolve o resultado
    return {"preco_previsto": round(float(preco_previsto), 2)}

# Função para a interface do mapa
@app.get("/simular-aleatorio-mapa")
def simular_aleatorio_mapa():

    # Seleciona uma casa aleatória do dataset
    casa_amostra = df_casas.sample(n=1).iloc[0].to_dict()

    # Dados da casa para mostrar no mapa
    dados_imovel = {
        "id": int(casa_amostra["id"]),
        "quartos": float(casa_amostra["bedrooms"]),
        "banheiros": float(casa_amostra["bathrooms"]),
        "area_living": float(casa_amostra["sqft_living"]),
        "area_lote": float(casa_amostra["sqft_lot"]),
        "andares": float(casa_amostra["floors"]),
        "waterfront": int(casa_amostra["waterfront"]),
        "view": int(casa_amostra["view"]),
        "conservacao": int(casa_amostra["condition"]),
        "grade": int(casa_amostra["grade"]),
        "area_shove": float(casa_amostra["sqft_above"]),
        "area_basement": float(casa_amostra["sqft_basement"]),
        "ano_construcao": int(casa_amostra["yr_built"]),
        "ano_reforma": int(casa_amostra["yr_renovated"]),
        "cep": int(casa_amostra["zipcode"]),
        "lat": float(casa_amostra["lat"]),
        "long": float(casa_amostra["long"]),
        "area_living15": float(casa_amostra["sqft_living15"]),
        "area_lote15": float(casa_amostra["sqft_lot15"]),

        # Preço REAL do CSV
        "casa_preco_real": float(casa_amostra["price"])
    }

    # Dados que serão enviados para a RNA
    # O "price" NÃO entra aqui
    dados_rna = {
        "bedrooms": dados_imovel["quartos"],
        "bathrooms": dados_imovel["banheiros"],
        "sqft_living": dados_imovel["area_living"],
        "sqft_lot": dados_imovel["area_lote"],
        "floors": dados_imovel["andares"],
        "waterfront": dados_imovel["waterfront"],
        "view": dados_imovel["view"],
        "condition": dados_imovel["conservacao"],
        "grade": dados_imovel["grade"],
        "sqft_above": dados_imovel["area_shove"],
        "sqft_basement": dados_imovel["area_basement"],
        "yr_built": dados_imovel["ano_construcao"],
        "yr_renovated": dados_imovel["ano_reforma"],
        "zipcode": dados_imovel["cep"],
        "lat": dados_imovel["lat"],
        "long": dados_imovel["long"],
        "sqft_living15": dados_imovel["area_living15"],
        "sqft_lot15": dados_imovel["area_lote15"]
    }

    # Monta a entrada na mesma ordem utilizada no treinamento
    entrada = [dados_rna[coluna] for coluna in colunas_entrada]

    # Aplica o mesmo scaler utilizado no treinamento
    entrada_padronizada = scaler.transform([entrada])

    # Faz a previsão utilizando a RNA
    preco_previsto = modelo.predict(entrada_padronizada)[0]

    # Adiciona a previsão aos dados do imóvel
    dados_imovel["resultado_preco_mapa"] = round(float(preco_previsto), 2)

    # Retorna todos os dados para o mapa
    return dados_imovel