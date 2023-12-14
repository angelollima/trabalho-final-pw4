from fastapi import ( APIRouter, Depends, Form, HTTPException, Path, Request, status,)

from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models.Usuario import Usuario
from util.mensagem import redirecionar_com_mensagem
from repositories.UsuarioRepo import UsuarioRepo
from util.seguranca import (conferir_senha, obter_hash_senha, obter_usuario_logado,)

router = APIRouter(prefix="/usuario")
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request, usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    usuarios = UsuarioRepo.obter_todos()
    return templates.TemplateResponse("usuario/index.html", {"request": request, "usuario": usuario, "usuarios": usuarios},)

@router.get("/arearestrita/{id_usuario:int}", response_class=HTMLResponse)
async def get_index(request: Request, id_usuario: int = Path(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    
    usuario_alterar = UsuarioRepo.obter_por_id(id_usuario)
    return templates.TemplateResponse("usuario/arearestrita.html", {"request": request, "usuario": usuario, "usuario_alterar": usuario_alterar},)

@router.get("/excluir/{id_usuario:int}", response_class=HTMLResponse)
async def get_excluir(request: Request, id_usuario: int = Path(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    usuario_excluir = UsuarioRepo.obter_por_id(id_usuario)
    return templates.TemplateResponse("usuario/excluir.html", {"request": request, "usuario": usuario, "usuario_excluir": usuario_excluir},)

@router.post("/excluir/{id_usuario:int}", response_class=HTMLResponse)
async def post_excluir(usuario: Usuario = Depends(obter_usuario_logado), id_usuario: int = Path(),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if id_usuario == 1:
        response = redirecionar_com_mensagem("/usuario","Não é possível excluir o administrador padrão do sistema.",)
        return response
    if id_usuario == usuario.id:
        response = redirecionar_com_mensagem("/usuario", "Não é possível excluir o próprio usuário que está logado.",)
        return response

    UsuarioRepo.excluir(id_usuario)
    response = redirecionar_com_mensagem("/usuario", "Usuário excluído com sucesso.",)
    return response

@router.get("/alterar/{id_usuario:int}", response_class=HTMLResponse)
async def get_alterar(request: Request, id_usuario: int = Path(), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    usuario_alterar = UsuarioRepo.obter_por_id(id_usuario)
    return templates.TemplateResponse("usuario/alterar.html", {"request": request, "usuario": usuario, "usuario_alterar": usuario_alterar},)

@router.post("/alterar/{id_usuario:int}", response_class=HTMLResponse)
async def post_alterar(id_usuario: int = Path(), nome: str = Form(...), email: str = Form(...), administrador: bool = Form(False), usuario: Usuario = Depends(obter_usuario_logado),):
    if not usuario:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    if not usuario.admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    if id_usuario == 1:
        response = redirecionar_com_mensagem("/usuario", "Não é possível alterar dados do administrador padrão.",)
        return response

    UsuarioRepo.alterar(Usuario(id=id_usuario, nome=nome, email=email, admin=administrador))
    response = redirecionar_com_mensagem("/usuario", "Usuário alterado com sucesso.")
    return response

@router.get("/novo")
async def get_usuario_novo(request: Request,):
    return templates.TemplateResponse("/usuario/inserir.html", {"request": request},)

@router.post("/novo", response_class=HTMLResponse)
async def post_usuario_novo(senha: str = Form(...), confsenha: str = Form(...),
    nome: str = Form(...), 
    email: str = Form(...), 
    administrador: bool = Form(False), 
    usuario: Usuario = Depends(obter_usuario_logado)):

    hash_senha = obter_hash_senha(senha)

    usuario = Usuario(nome=nome, email=email, senha=hash_senha, admin=administrador)
    print(usuario)
    print(UsuarioRepo.inserir(usuario))

    response = redirecionar_com_mensagem("/login", "Usuario criado com sucesso! Entre com seu email e senha para acessar!")
    return response