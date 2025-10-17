from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey, Date, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    usuario = "usuario"

class StatusEnum(str, enum.Enum):
    pendente = "pendente"
    confirmado = "confirmado"
    concluido = "concluido"
    cancelado = "cancelado"

class LocalizacaoEnum(str, enum.Enum):
    sala = "sala"
    guardiao = "guardiao"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    google_id = Column(String(255), unique=True, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.usuario)
    criado_em = Column(DateTime, default=datetime.utcnow)

    agendamentos = relationship("Agendamento", back_populates="usuario")


class TipoDispositivo(Base):
    __tablename__ = "tipos_dispositivo"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)

    dispositivos = relationship("Dispositivo", back_populates="tipo")


class Sala(Base):
    __tablename__ = "salas"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)


class Guardiao(Base):
    __tablename__ = "guardioes"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    contato = Column(String(255))


class Dispositivo(Base):
    __tablename__ = "dispositivos"

    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    tipo_id = Column(Integer, ForeignKey("tipos_dispositivo.id"))
    localizacao_tipo = Column(Enum(LocalizacaoEnum))
    localizacao_id = Column(Integer)
    total = Column(Integer, default=1)
    disponivel = Column(Integer, default=1)
    status = Column(String(50), default="ativo")

    tipo = relationship("TipoDispositivo", back_populates="dispositivos")
    agendamentos = relationship("Agendamento", back_populates="dispositivo")


class Agendamento(Base):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    dispositivo_id = Column(Integer, ForeignKey("dispositivos.id"))
    data = Column(Date, nullable=False)
    aulas = Column(JSON)  # lista de aulas [1,2,3,...]
    quantidade = Column(Integer, default=1)
    status = Column(Enum(StatusEnum), default=StatusEnum.pendente)
    criado_em = Column(DateTime, default=datetime.utcnow)

    usuario = relationship("Usuario", back_populates="agendamentos")
    dispositivo = relationship("Dispositivo", back_populates="agendamentos")
