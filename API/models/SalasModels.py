from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from API.core.config import settings
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BOOLEAN
from sqlalchemy.orm import relationship




class SalaModel(settings.DBBaseModel):
    __tablename__ = 'salas'
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    numero_chave: int = Column(Integer, nullable=False)  # Definido como chave primária
    nome: str = Column(String(80), nullable=False)
    is_ocupada: bool = Column(BOOLEAN, default=False)

    # Relacionamento com HistoricoAcesso
    historicos = relationship("HistoricoAcesso", back_populates="sala")

    def __repr__(self):
        return f"<SalaModel(numero_chave={self.numero_chave}, nome='{self.nome}')>"



