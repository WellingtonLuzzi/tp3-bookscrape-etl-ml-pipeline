
from fastapi import FastAPI, Query
from typing import Optional
import pandas as pd

# 1. Inicialização da aplicação FastAPI com metadados para a documentação
app = FastAPI(
    title="Books Analytics & ML-Ready API",
    description="API REST para consulta de livros das categorias Horror, Science Fiction e Thriller.",
    version="1.0.0"
)

# 2. Função auxiliar para carregar o arquivo .CSV gerado
def carregar_dados():
    return pd.read_csv("dados_modelo_pronto.csv")

# 3. Endpoint raiz de verificação de saúde (Health Check)
@app.get("/")
def home():
    return {
        "mensagem": "API ML-Ready ativa! Acesse /dados para consumir o dataset ou /docs para testar."
    }

# 4. Endpoint principal: GET /dados
# Permite filtros opcionais via URL (ex: /dados?categoria=Horror&faixa_preco=Barato)
@app.get("/dados")
def listar_dados(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria (ex: Horror, Science Fiction, Thriller)"),
    faixa_preco: Optional[str] = Query(None, description="Filtrar por faixa (Barato, Médio, Caro)"),
    limite: int = Query(50, ge=1, le=100, description="Quantidade máxima de registros retornados")
):
    # Carrega o dataframe limpo
    df = carregar_dados()

    # Aplica filtros se o usuário/sistema tiver passado na URL
    if categoria:
        df = df[df["categoria"].str.lower() == categoria.lower()]
    if faixa_preco:
        df = df[df["faixa_preco"].str.lower() == faixa_preco.lower()]

    # Converte o resultado filtrado para lista de dicionários (formato JSON)
    registros = df.head(limite).to_dict(orient="records")

    return {
        "status": "sucesso",
        "total_retornado": len(registros),
        "filtros": {"categoria": categoria, "faixa_preco": faixa_preco},
        "dados": registros
    }
