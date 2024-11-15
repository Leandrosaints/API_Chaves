from API.core.config import settings
from core.database import engine

async def create_tables()->None:
    import models.__all__models
    print('criando tabelas no banco de dados')
    async with engine.begin() as conn:
        await conn.run_sync(settings.DBBaseModel.metadata.drop_all)
        await conn.run_sync(settings.DBBaseModel.metadata.create_all)
    print('tabelas criadas com sucesso')
if __name__=='__main__':
    import asyncio
    asyncio.get_event_loop().run_until_complete(create_tables())
    






