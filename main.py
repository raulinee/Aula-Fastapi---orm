#Fastapi
# pip install fastapi uvicorn jinja2 python-multipart
from fastapi import FastAPI, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
#Para salvar o ss em outra pasta
from fastapi.staticfiles import StaticFiles
from models import get_db, Curso, Aluno
from sqlalchemy.orm import Session


# Rodar o servidor: python -m uvicorn main:app --reload
app = FastAPI(title="Gestão escolar")

#Configar o diretório dos html
templates = Jinja2Templates(directory="templates")

#Mapeia a  pasta static para servir arquivos (CSS, IMG, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

#Abrir/retornar html:
# Rota - endpoint
# Método HTTP - GET, POST, PUT, DELETE
# GET = Pegar/Listar/Exibir
# POST = Criar/adicionar
# PUT = Atualizar
# DELETE = Deletar
@app.get("/")
def pagina_inical(request: Request):
    return templates.TemplateResponse(
        request,
        "pagina_inicial.html",
        {"request":request}
    )

@app.get("/alunos")
def listar_alunos(request: Request):
    alunos = [
        {"nome": "brandon", "nota": 5},
        {"nome": "Raul", "nota": 10},
        {"nome": "breno", "nota": 8},
        {"nome": "pedro", "nota": 2},
    ]
    return templates.TemplateResponse(
        request,
        "alunos.html",
        {"request": request, "alunos": alunos}
    )

#Exibir formulario de criar um curso
@app.get("/curso/cadastro")
def exibir_cadastro_curso(request: Request):
    return templates.TemplateResponse(
        request,
        "cadastro_curso.html",
        {"request": request}
    )

# Cadastrar curso
@app.post("/curso")
def criar_curso(
    nome: str = Form(...),
    duracao_dias: int = Form(...),
    descricao: str = Form(...),
    db: Session = Depends(get_db)
):

    novo_curo = Curso(nome=nome, duracao_dias= duracao_dias, descricao=descricao)
    db.add(novo_curo)
    db.commit()

    return RedirectResponse(url='/', status_code=303)