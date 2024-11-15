from datetime import datetime
from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from API.core.config import settings
from API.schemas.schemas_usuario import UsuarioSchemaBase, UsuarioSchemaUp, UsuarioSchemaCreate
from API.models.SalasModels import SalaModel
from API.models.HistoricosSalasModels import HistoricoAcesso
from API.models.UserModels import UsuarioModel
from sqlalchemy.orm import selectinload
from API.core.deps import get_session
from API.core.security import gerar_hash_senha, verificar_senha
from API.core.auth import autenticar,criar_token_acesso
from fastapi.responses import JSONResponse
from API.core.auth import Oauth_2_schema

router = APIRouter()

'''@router.get('/', response_model=List[UsuarioSchemaBase], status_code=status.HTTP_200_OK)
async def get_alls_actor(db:AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        actors:List[UsuarioModel] = result.scalars().unique().all()
        return actors'''
    
@router.get('/{user_id}', response_model=UsuarioSchemaBase, status_code=status.HTTP_200_OK)
async def get_actor(user_id: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == user_id)
        result = await session.execute(query)
        user: List[UsuarioModel] = result.scalars().unique().one_or_none()

        if user:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="os dados nao foram encontrados!")



@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UsuarioSchemaUp)
async def post_hotel(user:UsuarioSchemaUp, db:AsyncSession=Depends(get_session)):

    novo_user = UsuarioModel(nome=user.nome, sobrenome=user.sobrenome, email=user.email, senha=gerar_hash_senha(user.senha),
    endereco=user.endereco, funcao=user.funcao, telefone=user.telefone, admin=user.admin)
    async with db as session:
        try:
            session.add(novo_user)
            await session.commit()
            return novo_user
        except:
            raise HTTPException(detail='nao foi possivel cadastrar o usuario',
                                status_code=status.HTTP_406_NOT_ACCEPTABLE)

# Rota para redefinir a senha
@router.patch('/reset-password', status_code=status.HTTP_200_OK)
async def reset_password(data: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    # Verifica se o e-mail existe no banco de dados
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == data.email)
        result = await session.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="E-mail não encontrado."
            )

        # Criptografa a nova senha fornecida pelo usuário
        senha_hash = gerar_hash_senha(data.senha)

        # Atualiza a senha do usuário no banco de dados
        user.senha = senha_hash
        await session.commit()

        # Opcional: Envie uma confirmação ao usuário
        return {"detail": "Senha redefinida com sucesso."}


@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(detail='dados incorretos', status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse(content={"acess_token": criar_token_acesso(sub=usuario.id),"user_id":usuario.id,"token_type": "bearer"},
                        status_code=status.HTTP_200_OK)

@router.get('/historicos/{usuario_historico_id}', status_code=status.HTTP_200_OK)
async def get_historico_por_usuario(usuario_historico_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        # Consulta o histórico com os dados relacionados da sala e do usuário
        query = (
            select(HistoricoAcesso)
            .options(
                selectinload(HistoricoAcesso.sala),  # Carregar a relação com sala
                selectinload(HistoricoAcesso.usuario)  # Carregar a relação com usuário
            )
            .filter(HistoricoAcesso.usuario_id == usuario_historico_id)  # Filtra pelo usuário_id
        )

        result = await session.execute(query)
        historico = result.scalars().all()  # Retorna todos os históricos para o usuário

        if historico:
            # Montando a resposta completa com dados adicionais do relacionamento
            return [
                {
                    "id": h.id,
                    "sala_id": h.sala_id,
                    "usuario_id": h.usuario_id,
                    "data_hora_retirada": h.data_hora_retirada,
                    "data_hora_devolucao": h.data_hora_devolucao,
                    "sala_nome": h.sala.nome,  # Nome da sala, usando o relacionamento
                    "usuario_nome": h.usuario.nome  # Nome do usuário, usando o relacionamento
                }
                for h in historico
            ]
        else:
            raise HTTPException(
                detail=f'Não foi encontrado um histórico com o usuário ID {usuario_historico_id}',
                status_code=status.HTTP_404_NOT_FOUND
            )


'''@router.put('/{usuario_id}', response_model=UsuarioSchemaUp, status_code=status.HTTP_202_ACCEPTED)
async def put_user_up(usuario_id: int, user: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        # Busca o usuário pelo ID
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        user_up: UsuarioModel = result.scalars().unique().one_or_none()

        if user_up:
            # Atualiza os campos do usuário com os novos valores recebidos
            user_up.nome = user.nome
            user_up.sobrenome = user.sobrenome
            user_up.funcao = user.funcao
            user_up.email = user.email
            user_up.senha = user.senha  # Certifique-se de criptografar se necessário
            user_up.telefone = user.telefone
            user_up.endereco = user.endereco

            # Confirma as alterações no banco de dados
            await session.commit()
            # Refresca o objeto para garantir que a resposta esteja sincronizada com o banco de dados
            await session.refresh(user_up)

            return user_up
        else:
            # Retorna um erro 404 caso o usuário não seja encontrado
            raise HTTPException(
                detail='Usuário não encontrado.',
                status_code=status.HTTP_404_NOT_FOUND
            )'''

@router.patch('/{usuario_id}', response_model=UsuarioSchemaUp, status_code=status.HTTP_202_ACCEPTED)
async def patch_user(usuario_id: int, user: UsuarioSchemaUp, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        user_up: UsuarioModel = result.scalars().unique().one_or_none()

        if user_up:
            # Atualize apenas os campos fornecidos
            for attr, value in user.dict(exclude_unset=True).items():
                setattr(user_up, attr, value)

            await session.commit()
            return user_up
        else:
            raise HTTPException(detail="Usuário não encontrado", status_code=status.HTTP_404_NOT_FOUND)
revoked_tokens = set()
@router.post('/logout')
async def logout(token: str = Depends(Oauth_2_schema)):
    # Decodificar o token para pegar o tempo de expiração
    try:
        payload = jwt.decode(token, settings.JWT_SECRETS, algorithms=[settings.ALGORITHM])
        exp = payload.get("exp")

        # Adiciona o token à lista de revogados
        revoked_tokens.add(token)

        # Opcional: Limpa tokens expirados da lista
        now = datetime.utcnow()
        revoked_tokens.discard(t for t in revoked_tokens if jwt.decode(t, settings.JWT_SECRETS, algorithms=[settings.ALGORITHM]).get("exp", 0) < now.timestamp())

        return {"msg": "Logout realizado com sucesso"}
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou já expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Função para verificar se o token está na lista de revogados
def is_token_revoked(token: str) -> bool:
    return token in revoked_tokens