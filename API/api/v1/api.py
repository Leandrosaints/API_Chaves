from fastapi import APIRouter
from API.api.v1.endpoints import user_router
from API.api.v1.endpoints import historicos_salas_router
from API.api.v1.endpoints import salas_router

api_router = APIRouter()

api_router.include_router(user_router.router, prefix='/usuarios',tags=['usuarios'])
api_router.include_router(historicos_salas_router.router, prefix='/historicos', tags=['historicos'])
api_router.include_router(salas_router.router, prefix='/salas', tags=['salas'])
#api_router.include_router(filmes_router.router, prefix='/filmes', tags=['filmes'])