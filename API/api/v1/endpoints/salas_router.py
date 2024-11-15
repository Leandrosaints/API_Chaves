from typing import List, Optional, Any
from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from API.models.SalasModels import SalaModel
from API.schemas.schemas_salas import Sala, SalaBase, SalaCreate,SalaOcupada
from API.models.UserModels import UsuarioModel
from sqlalchemy.orm import selectinload
from API.core.deps import get_session
from API.core.security import gerar_hash_senha, verificar_senha
from API.core.auth import autenticar,criar_token_acesso
from fastapi.responses import JSONResponse



router = APIRouter()

@router.get('/salas', response_model=List[Sala], status_code=status.HTTP_200_OK)
async def get_usuarios(db :AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(SalaModel)
        result = await session.execute(query)
        salas: List[SalaModel] = result.scalars().unique().all()

        return salas

#router que envia se a sala esta ocupada

@router.patch('/{sala_id}', response_model=Sala, status_code=status.HTTP_200_OK)
async def update_sala_status(sala_id: int, sala_ocupada: SalaOcupada, db: AsyncSession = Depends(get_session)):
    # Consulta a sala com o ID fornecido
    async with db as session:
        query = select(SalaModel).filter(SalaModel.id == sala_id)
        result_sala = await session.execute(query)
        sala = result_sala.scalars().one_or_none()

    # Verifica se a sala existe
    if not sala:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sala não encontrada")

    # Atualiza o status de ocupação da sala
    sala.is_ocupada = sala_ocupada.is_ocupada
    session.add(sala)
    await session.commit()
    await session.refresh(sala)  # Atualiza o objeto sala com os dados salvos

    return Sala(
        id=sala.id,
        nome=sala.nome,
        numero_chave=sala.numero_chave,
        is_ocupada=sala.is_ocupada
    )
