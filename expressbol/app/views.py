from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

from .extensions import appbuilder

from .models import (
    Cliente,
    Vehiculo,
    RutaViaje,
    Envio
)


class ClienteView(ModelView):
    datamodel = SQLAInterface(Cliente)

    list_columns = [
        "nombre",
        "telefono",
        "carnet"
    ]

    add_columns = [
        "nombre",
        "telefono",
        "carnet"
    ]

    edit_columns = [
        "nombre",
        "telefono",
        "carnet"
    ]


class VehiculoView(ModelView):
    datamodel = SQLAInterface(Vehiculo)

    list_columns = [
        "placa",
        "tipo",
        "capacidad_kg"
    ]

    add_columns = [
        "placa",
        "tipo",
        "capacidad_kg"
    ]

    edit_columns = [
        "placa",
        "tipo",
        "capacidad_kg"
    ]


class RutaViajeView(ModelView):
    datamodel = SQLAInterface(RutaViaje)

    list_columns = [
        "origen",
        "destino",
        "fecha_salida",
        "fecha_llegada",
        "vehiculo"
    ]

    add_columns = [
        "origen",
        "destino",
        "fecha_salida",
        "fecha_llegada",
        "vehiculo"
    ]

    edit_columns = [
        "origen",
        "destino",
        "fecha_salida",
        "fecha_llegada",
        "vehiculo"
    ]


class EnvioView(ModelView):
    datamodel = SQLAInterface(Envio)

    list_columns = [
        "codigo",
        "cliente",
        "origen",
        "destino",
        "peso",
        "precio",
        "estado",
        "viaje"
    ]

    add_columns = [
        "codigo",
        "descripcion",
        "peso",
        "precio",
        "estado",
        "origen",
        "destino",
        "fecha_registro",
        "cliente",
        "viaje"
    ]

    edit_columns = [
        "codigo",
        "descripcion",
        "peso",
        "precio",
        "estado",
        "origen",
        "destino",
        "fecha_registro",
        "cliente",
        "viaje"
    ]


appbuilder.add_view(
    ClienteView,
    "Clientes",
    icon="fa-users",
    category="Gestion"
)

appbuilder.add_view(
    VehiculoView,
    "Vehiculos",
    icon="fa-truck",
    category="Gestion"
)

appbuilder.add_view(
    RutaViajeView,
    "Rutas",
    icon="fa-road",
    category="Gestion"
)

appbuilder.add_view(
    EnvioView,
    "Envios",
    icon="fa-box",
    category="Gestion"
)