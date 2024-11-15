from pydantic import BaseModel
from typing import Optional

#Sala: Um modelo que inclui o campo id (gerado automaticamente pelo banco de dados) e permite a conversão de ORM (Object-Relational Mapping) para o modelo Pydantic.
class SalaBase(BaseModel):
    nome: Optional[str]
    numero_chave: Optional[int]
    is_ocupada: Optional[bool]


#SalaCreate: Um modelo para criar novas salas, que herda de SalaBase.
class SalaCreate(SalaBase):

    pass

class SalaOcupada(SalaBase):
    is_ocupada: bool

#SalaBase: Define os campos básicos da tabela Salas (neste caso, apenas nome).
class Sala(SalaBase):
    id: int

    class Config:
        orm_mode = True


