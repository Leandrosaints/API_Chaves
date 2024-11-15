from datetime import datetime
from pydantic import BaseModel
from typing import Optional

#HistoricoAcessoBase: Define os campos básicos da tabela HistoricoAcesso.
class HistoricoAcessoBase(BaseModel):
    sala_id: int
    usuario_id: int
    data_hora_retirada: datetime
    data_hora_devolucao: Optional[datetime] = None


#HistoricoAcessoCreate: Um modelo para criar novos registros de histórico de acesso.
class HistoricoAcessoCreate(HistoricoAcessoBase):
    pass


#HistoricoAcesso: Um modelo que inclui o campo id e permite a conversão de ORM para o modelo Pydantic.
class HistoricoAcesso(HistoricoAcessoBase):
    id: int

    class Config:
        orm_mode = True
"""
HistoricoAcessoBase:

Esta classe é a base para HistoricoAcessoCreate e HistoricoAcesso.
Serve para definir os campos que ambos os modelos herdarão, simplificando a manutenção e evitando repetição de código.
Normalmente, você não a usaria diretamente, mas sim as subclasses que se baseiam nela.

#HistoricoAcessoCreate:
Usada para criar novos registros de HistoricoAcesso.
É útil quando você está lidando com dados de entrada, pois ela não inclui o campo id, que será gerado pelo banco de dados.
Pode ser aplicada em rotas POST para criar entradas novas sem sobrecarregar o cliente com o campo id.

#HistoricoAcesso:
Usada para definir o modelo completo de HistoricoAcesso, incluindo o campo id.
Essa classe inclui orm_mode = True, o que permite a conversão automática de objetos ORM (do SQLAlchemy, por exemplo) 
para o modelo Pydantic. Isso facilita o envio de dados do banco para o cliente.
Ideal para rotas GET ou como modelo de resposta (response_model) para retornar registros completos ao cliente, 
incluindo o id e quaisquer dados adicionais armazenados no banco.
Em resumo:

HistoricoAcessoCreate: para inserção de novos registros (POST).
HistoricoAcesso: para retornar registros completos (GET), especialmente ao cliente."""