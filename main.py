'''
AUTORES:
    Felipe Kuznik Thome 
    Kurt Cobain  Rodrigues 
    Pedro Ghinzelli
'''

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import joblib

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# carrega modelo treinado, scaler e lista de colunas (uma ves so) qd o server liga
modelo = joblib.load("modelos/modelo_precos.pkl")
scaler = joblib.load("modelos/scaler.pkl")
colunas_entrada = joblib.load("modelos/colunas_entrada.pkl")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


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
    condicao: int = Form(...),
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
        "condition": condicao,
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

