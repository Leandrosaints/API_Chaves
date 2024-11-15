from typing import Optional, List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pytz import timezone#lib para pegar zona de horario

from API.models.UserModels import UsuarioModel
from API.core.config import settings
from API.core.security import verificar_senha
from pydantic import EmailStr

Oauth_2_schema = OAuth2PasswordBearer(
    tokenUrl=f'{settings.API_V1_STR}/usuarios/login'
)

"""
baixo criamos uam func na qual usar as credenciais (passada na hora do cadastro so dados)
assim a fuunc iria validar os dados
"""
async def autenticar(email:EmailStr, senha:str, db:AsyncSession) -> Optional[UsuarioModel]:
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.email == email)
        result = await session.execute(query)
        usuario:UsuarioModel = result.scalars().unique().one_or_none()

        if not usuario:
            return None
        if not verificar_senha(senha, usuario.senha):
            return None
        return usuario

"""
a func abaixo cria um token de acesso com a func interna do jwt.encode() que usa a carga util de dados para isso.
a func do jwt funciona com tres arg(), sao eles:payload, key_secret e algoritmo de hash.
o token retonado jwt e composto por um Header, payload a signature

obs:os dados passado no encode nao esta respctivamente nessa ordem!

"""
def criar_token(tipo_token:str, tempo_vida:timedelta, sub:str)->str:
    payload = {}
    sp = timezone('America/Sao_Paulo')
    expire = datetime.now(tz=sp) + tempo_vida

    payload["type"] = tipo_token
    payload["exp"] =  expire
    payload["iat"] = datetime.now(tz=sp)
    payload["sub"]= str(sub)

    return jwt.encode(payload, settings.JWT_SECRETS, algorithm=settings.ALGORITHM)

"""
a func recebe como argumento um sub que e uma (claim do payload) que no caso aqui, nessa funcao, e o usuario do id, que sera informado na hora que a mes for chamada.
dentro desta funcao retornamos a func acima, que recebe seus respectivos arg criando o token de acesso 
"""
def criar_token_acesso(sub:str) ->str:
    return criar_token(

        tipo_token='acess_token',
        tempo_vida=timedelta(minutes=settings.ACESSE_TOKEN_EXPIRE_MINUTES),
        sub=sub

    )





