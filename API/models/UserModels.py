from sqlalchemy import Column, Integer, String, BOOLEAN
from sqlalchemy.orm import relationship

from API.core.config import settings


"""
nullable -> Se definido como o padrão True, indica que a coluna será renderizada como permitindo NULL, caso contrário, ela será renderizada como NOT NULL. Este parâmetro é usado apenas ao emitir instruções CREATE TABLE.
Unique -> definie uma coluna como de dados unicos, ou seja nao posso ter dois email com o mesmo dado
"""


class UsuarioModel(settings.DBBaseModel):
    __tablename__ = 'usuarios'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    nome: str = Column(String(80), nullable=False)
    sobrenome: str = Column(String(40), nullable=False)
    funcao: str = Column(String(80), nullable=False)
    email: str = Column(String(256), nullable=False, unique=True)
    senha: str = Column(String(256), nullable=False)
    endereco: str = Column(String(256), nullable=False)
    telefone: str = Column(String(80), nullable=False)
    admin: bool = Column(BOOLEAN, default=False)

    # Relacionamento com HistoricoAcesso
    historicos = relationship("HistoricoAcesso", back_populates="usuario")

    def __repr__(self):
        return f"<UsuarioModel(id={self.id}, nome='{self.nome}', sobrenome='{self.sobrenome}')>"
