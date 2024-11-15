'''from fastapi import FastAPI
from core.config import settings
from api.v1.api import api_router

app = FastAPI(title="API GESTAO DE CHAVES")
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__=="__main__":
    import uvicorn

    uvicorn.run('main:app',
                host='127.0.0.1', port=8000,
                log_level='info',
                reload=True, debug=True)


'''
from fastapi import FastAPI
from API.core.config import settings
from API.api.v1.api import api_router
from pyngrok import ngrok
import uvicorn

app = FastAPI(title="API GESTÃO DE CHAVES")
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    # Configurar o token de autenticação do ngrok
    #ngrok.set_auth_token("2odGdyqXpSVZvAoF06rCtGQfPA1_5ar3CqfcDwBTCCLn81pNA")  # Adicione seu token aqui

    # Configurar o túnel ngrok
    #public_url = ngrok.connect(8000)
    #print(f"Túnel público disponível em: {public_url}")

    # Iniciar o servidor Uvicorn
    uvicorn.run('main:app',
                host='127.0.0.1', port=8000,
                log_level='info',
                reload=True, debug=True)

    # Desconectar o túnel quando o servidor parar (opcional)
    #ngrok.disconnect(public_url)


