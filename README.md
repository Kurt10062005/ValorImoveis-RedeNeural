<!--
AUTORES:
    Felipe Kuznik Thome 
    Kurt Cobain  Rodrigues 
    Pedro Ghinzelli
-->

# Avaliação de Imóveis com Rede Neural Artificial (RNA)

Este projeto é uma aplicação web interativa desenvolvida com FastAPI para previsão e avaliação de preços de imóveis utilizando modelos de redes neurais.

---

## Estrutura do Projeto

* __pycache__/: Arquivos temporários gerados pelo Python para otimização de execução.
* dados/: Armazena as bases de dados e conjuntos de informações (arquivos .csv, .json, etc.) utilizados para treinamento e testes.
* modelos/: Contém o script do algoritmo (nomeArquivoDoAlgoritmo.py) responsável pelo treinamento/arquitetura da Rede Neural, além do arquivo do modelo treinado exportado.
* static/: Arquivos estáticos da interface web.
  * css/: Estilos visuais da página (style.css).
  * imagens/: Elementos visuais e overlays do mapa (mapa.jpeg).
  * js/: Scripts de interatividade no frontend (mapa.js e integração Leaflet).
* templates/: Páginas HTML do projeto (index.html).
* main.py: Arquivo principal da aplicação FastAPI, responsável por criar as rotas da API, carregar o HTML e conectar o modelo da IA com o frontend.

---

## Requisitos Prévios
Certifique-se de ter o Python instalado na sua máquina (versão 3.8 ou superior).
Instale as dependências necessárias executando o comando no terminal:

pip install fastapi uvicorn

(Caso utilize bibliotecas de Machine Learning no algoritmo, adicione-as também, como pip install numpy pandas torch scikit-learn)

---

## Como Rodar a Aplicação

1. Abra o terminal na pasta raiz do projeto (onde está o arquivo main.py).

2. Execute o servidor de desenvolvimento do FastAPI usando o Uvicorn:

uvicorn main:app --reload

Explicação do comando:
* main: Nome do arquivo main.py.
* app: Instância do FastAPI criada dentro do arquivo (app = FastAPI()).
* --reload: Reinicia o servidor automaticamente sempre que você salvar alterações no código.

3. Abra o navegador e acesse o endereço local:
http://127.0.0.1:8000

---

## Documentação da API

O FastAPI gera a documentação interativa automaticamente. Para testar as rotas da sua aplicação diretamente no navegador, acesse:

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

## Passo passo para clonar o repositório
1. Abrir o Terminal
Abra o PowerShell, CMD ou o terminal dentro do VS Code na pasta onde deseja salvar o projeto.

2. Executar o Comando de Clone
Digite o comando git clone seguido do link do repositório:

[git clone https://github.com/Kurt10062005/ValorImoveis-RedeNeural.git]

3. Entrar na Pasta do Projeto
Após o download ser concluído, acesse a pasta criada:

[cd ValorImoveis-RedeNeural]

4. Abrir no VS Code
Para abrir a pasta diretamente no VS Code, rode:

[code .]

(Ou abra o VS Code manualmente e vá em File > Open Folder para selecionar a pasta do projeto).
 
## Passo a passo de como atualizar o repositório depois de fazer alterações no projeto:
Passo 1: Verificar os arquivos alterados:
Para ver quais arquivos você modificou, criou ou deletou, rode:

[git status]

Passo 2: Adicionar as alterações:
Para preparar todos os arquivos alterados para o salvamento, execute:

[git add .]

Passo 3: Salvar as alterações (Commit)
Crie uma mensagem explicando o que você mudou ou adicionou:

[git commit -m "Sua mensagem aqui (ex: Atualiza layout e estilos)"]

Passo 4: Enviar para o GitHub (Push)
Envie o seu código salvo para o repositório online:

[git push]

Dica importante para trabalho em equipe:
Antes de começar a mexer no código é sempre bom rodar o comando abaixo para baixar as alterações que os outros integrantes do projeto possam ter feito:

[git pull]