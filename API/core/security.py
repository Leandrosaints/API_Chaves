from passlib.context import CryptContext

# instanciando a class CryptContext
CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')


# schemas e parametro do metedo constructor -->


def verificar_senha(senha: str, hash_senha: str) -> bool:
    return CRIPTO.verify(senha, hash_senha)


def gerar_hash_senha(senha: str) -> str:
    return CRIPTO.hash(senha)

