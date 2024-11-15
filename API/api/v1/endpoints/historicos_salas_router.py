from datetime import datetime

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import selectinload
from API.schemas.schemas_historico_salas import HistoricoAcessoCreate, HistoricoAcesso
from API.models.HistoricosSalasModels import HistoricoAcesso
from API.models.SalasModels import SalaModel
from API.models.UserModels import UsuarioModel
from API.core.deps import get_session
router = APIRouter()

from fastapi.responses import JSONResponse

@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=HistoricoAcessoCreate)
async def post_historico(historico: HistoricoAcessoCreate, db: AsyncSession = Depends(get_session)):

    async with db as session:
        # Verificando se a sala existe
        query_sala = select(SalaModel).filter(SalaModel.numero_chave == historico.sala_id)
        result_sala = await session.execute(query_sala)
        sala = result_sala.scalars().one_or_none()

        # Verificando se o usuário existe
        query_usuario = select(UsuarioModel).filter(UsuarioModel.id == historico.usuario_id)
        result_usuario = await session.execute(query_usuario)
        usuario = result_usuario.scalars().one_or_none()

        # Se a sala e o usuário existirem, criamos o histórico de acesso
        if sala and usuario:
            # Criando o novo histórico de acesso
            db_historico = HistoricoAcesso(
                sala_id=historico.sala_id,
                usuario_id=historico.usuario_id,
                data_hora_retirada=historico.data_hora_retirada,

            )
            session.add(db_historico)
            await session.commit()
            await session.refresh(db_historico)  # Atualiza db_historico com os dados salvos

            # Retornando o histórico com os campos manualmente convertidos para dicionário
            historico_dict = {
                "id": db_historico.id,
                "sala_id": db_historico.sala_id,
                "usuario_id": db_historico.usuario_id,
                "data_hora_retirada": db_historico.data_hora_retirada.isoformat(),  # Converte para string ISO

            }
            return JSONResponse(content=historico_dict)
        else:
            # Se a sala ou o usuário não existirem, lançar erro
            raise HTTPException(
                detail='Sala ou usuário não encontrado',
                status_code=status.HTTP_404_NOT_FOUND
            )


@router.get('/historicos/{sala_id}', status_code=status.HTTP_200_OK)
async def get_historico(sala_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        # Consulta o histórico com os dados relacionados da sala e do usuário
        query = (
            select(HistoricoAcesso)
            .options(
                selectinload(HistoricoAcesso.sala),  # Carregar a relação com a sala
                selectinload(HistoricoAcesso.usuario)  # Carregar a relação com o usuário
            )
            .filter(HistoricoAcesso.sala_id == sala_id)  # Filtro baseado no ID da sala
        )

        result = await session.execute(query)
        historicos = result.scalars().all()

        if historicos:
            # Montando a resposta completa com dados adicionais dos históricos relacionados à sala
            resultado = []
            for historico in historicos:
                resultado.append({
                    "id": historico.id,
                    "sala_id": historico.sala_id,
                    "usuario_id": historico.usuario_id,
                    "data_hora_retirada": historico.data_hora_retirada,
                    "data_hora_devolucao": historico.data_hora_devolucao,
                    "sala_nome": historico.sala.nome,  # Nome da sala, usando o relacionamento
                    "sala_numero": historico.sala.numero_chave,  # Número da sala
                    "nome": historico.usuario.nome,  # Nome do usuário
                    "funcao":historico.usuario.funcao,
                    "email": historico.usuario.email,  # Email do usuário
                    "telefone": historico.usuario.telefone,  # Número do usuário (caso exista)
                })

            return resultado
        else:
            raise HTTPException(
                detail=f'Não foi encontrado histórico de acesso para a sala com o ID {sala_id}',
                status_code=status.HTTP_404_NOT_FOUND
            )


@router.patch('/historico/devolver/{sala_id}/{usuario_id}', status_code=status.HTTP_200_OK)
async def update_data_hora_devolucao(sala_id: int, usuario_id: int, db: AsyncSession = Depends(get_session)):
    """
    Atualiza o campo `data_hora_devolucao` do último histórico de acesso
    para uma combinação específica de sala e usuário.
    """
    async with db as session:
        # Busca o histórico mais recente para a combinação de `sala_id` e `usuario_id`
        query = (
            select(HistoricoAcesso)
            .filter(HistoricoAcesso.sala_id == sala_id, HistoricoAcesso.usuario_id == usuario_id)
            .order_by(HistoricoAcesso.data_hora_retirada.desc())  # Ordena pelo último acesso
            .limit(1)  # Seleciona apenas o mais recente
        )
        result = await session.execute(query)
        historico = result.scalars().one_or_none()

        # Verifica se o histórico foi encontrado
        if not historico:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Histórico de acesso para a sala e usuário especificados não encontrado."
            )

        # Atualiza apenas o campo `data_hora_devolucao`
        historico.data_hora_devolucao = datetime.now().isoformat()  # Define a data e hora atual para devolução
        await session.commit()  # Salva as alterações no banco de dados
        await session.refresh(historico)  # Atualiza o objeto `historico` com os dados salvos

        # Retorna a resposta com os dados atualizados
        return {
            "id": historico.id,
            "sala_id": historico.sala_id,
            "usuario_id": historico.usuario_id,
            "data_hora_retirada": historico.data_hora_retirada.isoformat(),
            "data_hora_devolucao": historico.data_hora_devolucao.isoformat()
        }