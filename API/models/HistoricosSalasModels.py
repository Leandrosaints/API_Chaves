from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from API.core.config import settings


# Primeiro define o HistoricoAcesso

class HistoricoAcesso(settings.DBBaseModel):
    __tablename__ = 'historico_acesso'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    sala_id: int = Column(Integer, ForeignKey('salas.id'), nullable=False)
    usuario_id: int = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    data_hora_retirada: DateTime = Column(DateTime, nullable=False)
    data_hora_devolucao: DateTime = Column(DateTime, nullable=True)

    # Relacionamentos
    sala = relationship("SalaModel", back_populates="historicos")
    usuario = relationship("UsuarioModel", back_populates="historicos")

    def __repr__(self):
        return (f"<HistoricoAcesso(id={self.id}, sala_id={self.sala_id}, "
                f"usuario_id={self.usuario_id}, data_hora_retirada={self.data_hora_retirada})>")

"""O método __repr__ fornece uma representação em string útil para depuração.
Ele é automaticamente chamado quando um objeto é passado para a função print.
Isso ajuda a visualizar rapidamente o estado do objeto de forma clara e concisa."""