from flask import jsonify, render_template
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func

from .extensions import appbuilder, db

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


class ReportesView(BaseView):
    route_base = "/reportes"
    default_view = "index"

    @expose('/')
    def index(self):
        return self.render_template("reportes/index.html")

    @expose('/envios_estado')
    def envios_estado(self):
        resultados = db.session.query(
            Envio.estado,
            func.count(Envio.id).label('total')
        ).group_by(Envio.estado).all()

        labels = [r[0] for r in resultados]
        values = [r[1] for r in resultados]

        data = db.session.query(Envio).all()
        detalles = [
            {"codigo": e.codigo, "estado": e.estado, "origen": e.origen, "destino": e.destino, "precio": float(e.precio)}
            for e in data
        ]

        return jsonify({"labels": labels, "values": values, "detalles": detalles})

    @expose('/ingresos_periodo')
    def ingresos_periodo(self):
        resultados = db.session.query(
            func.date(Envio.fecha_registro).label('fecha'),
            func.sum(Envio.precio).label('total')
        ).filter(Envio.estado != 'Cancelado').group_by(
            func.date(Envio.fecha_registro)
        ).order_by(func.date(Envio.fecha_registro)).all()

        labels = [str(r[0]) for r in resultados]
        values = [float(r[1]) if r[1] else 0 for r in resultados]

        detalles = [
            {"fecha": str(r[0]), "total": float(r[1]) if r[1] else 0}
            for r in resultados
        ]

        return jsonify({"labels": labels, "values": values, "detalles": detalles})

    @expose('/envios_cliente')
    def envios_cliente(self):
        resultados = db.session.query(
            Cliente.nombre,
            func.count(Envio.id).label('total_envios'),
            func.sum(Envio.precio).label('total_ingresos')
        ).join(Envio).group_by(Cliente.id).order_by(
            func.count(Envio.id).desc()
        ).limit(10).all()

        labels = [r[0] for r in resultados]
        values = [r[1] for r in resultados]

        detalles = [
            {"cliente": r[0], "total_envios": r[1], "total_ingresos": float(r[2]) if r[2] else 0}
            for r in resultados
        ]

        return jsonify({"labels": labels, "values": values, "detalles": detalles})

    @expose('/envios_ruta')
    def envios_ruta(self):
        resultados = db.session.query(
            func.concat(Envio.origen, ' -> ', Envio.destino).label('ruta'),
            func.count(Envio.id).label('total')
        ).group_by(Envio.origen, Envio.destino).order_by(
            func.count(Envio.id).desc()
        ).all()

        labels = [r[0] for r in resultados]
        values = [r[1] for r in resultados]

        detalles = [
            {"ruta": r[0], "total": r[1]}
            for r in resultados
        ]

        return jsonify({"labels": labels, "values": values, "detalles": detalles})

    @expose('/utilizacion_vehiculos')
    def utilizacion_vehiculos(self):
        resultados = db.session.query(
            Vehiculo.placa,
            func.count(RutaViaje.id).label('total_viajes')
        ).outerjoin(RutaViaje).group_by(Vehiculo.id).order_by(
            func.count(RutaViaje.id).desc()
        ).all()

        labels = [r[0] for r in resultados]
        values = [r[1] for r in resultados]

        detalles = [
            {"placa": r[0], "total_viajes": r[1]}
            for r in resultados
        ]

        return jsonify({"labels": labels, "values": values, "detalles": detalles})


appbuilder.add_view(
    ReportesView,
    "Reportes",
    icon="fa-chart-bar",
    category="Gestion"
)