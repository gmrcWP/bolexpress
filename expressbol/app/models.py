from .extensions import db

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date
)

from sqlalchemy.orm import relationship


class Cliente(db.Model):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True)

    nombre = Column(String(100), nullable=False)

    telefono = Column(String(20))

    carnet = Column(String(20))

    envios = relationship(
        "Envio",
        back_populates="cliente"
    )

    def __repr__(self):
        return self.nombre


class Vehiculo(db.Model):
    __tablename__ = "vehiculo"

    id = Column(Integer, primary_key=True)

    placa = Column(String(20), unique=True)

    tipo = Column(String(50))

    capacidad_kg = Column(Float)

    viajes = relationship(
        "RutaViaje",
        back_populates="vehiculo"
    )

    def __repr__(self):
        return self.placa


class RutaViaje(db.Model):
    __tablename__ = "ruta_viaje"

    id = Column(Integer, primary_key=True)

    origen = Column(String(50))

    destino = Column(String(50))

    fecha_salida = Column(Date)

    fecha_llegada = Column(Date)

    vehiculo_id = Column(
        Integer,
        ForeignKey("vehiculo.id")
    )

    vehiculo = relationship(
        "Vehiculo",
        back_populates="viajes"
    )

    envios = relationship(
        "Envio",
        back_populates="viaje"
    )

    def __repr__(self):
        return f"{self.origen} -> {self.destino}"


class Envio(db.Model):
    __tablename__ = "envio"

    id = Column(Integer, primary_key=True)

    codigo = Column(String(20), unique=True)

    descripcion = Column(String(200))

    peso = Column(Float)

    precio = Column(Float)

    estado = Column(String(30))

    origen = Column(String(50))

    destino = Column(String(50))

    fecha_registro = Column(Date)

    cliente_id = Column(
        Integer,
        ForeignKey("cliente.id")
    )

    viaje_id = Column(
        Integer,
        ForeignKey("ruta_viaje.id")
    )

    cliente = relationship(
        "Cliente",
        back_populates="envios"
    )

    viaje = relationship(
        "RutaViaje",
        back_populates="envios"
    )

    def __repr__(self):
        return self.codigo