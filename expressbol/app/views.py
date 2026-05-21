from flask import jsonify, render_template, request
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func
from sqlalchemy import extract
from wtforms import SelectField
from flask_appbuilder.fieldwidgets import Select2Widget
from wtforms.validators import ValidationError
from .servicios.servicio_ia import analizar_ingresos

from .extensions import appbuilder, db

from .models import (
    Cliente,
    Vehiculo,
    RutaViaje,
    Envio
)


class WelcomeView(BaseView):
    route_base = "/inicio"
    default_view = "index"

    @expose('/')
    def index(self):
        return self.render_template("welcome.html")


appbuilder.add_view(
    WelcomeView,
    "Inicio",
    icon="fa-home",
    category=""
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

    add_form_extra_fields = {
    "tipo": SelectField(
            "Tipo",
            choices=[
                ("Camión", "Camión"),
                ("Camioneta", "Camioneta"),
                ("Furgón", "Furgón"),
                ("Semi Trailer", "Semi Trailer"),
                ("Trailer", "Trailer")
            ],
            widget=Select2Widget()
        )
    }

    edit_form_extra_fields = {
        "tipo": SelectField(
            "Tipo",
            choices=[
                ("Camión", "Camión"),
                ("Camioneta", "Camioneta"),
                ("Furgón", "Furgón"),
                ("Semi Trailer", "Semi Trailer"),
                ("Trailer", "Trailer")
            ],
            widget=Select2Widget()
        )
    }


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

    CIUDADES = [
        ("La Paz", "La Paz"),
        ("Santa Cruz", "Santa Cruz"),
        ("Cochabamba", "Cochabamba"),
        ("Sucre", "Sucre"),
        ("Tarija", "Tarija"),
        ("Potosí", "Potosí"),
        ("Oruro", "Oruro"),
        ("Beni", "Beni"),
        ("Pando", "Pando"),
        ("Chuquisaca", "Chuquisaca")
    ]

    add_form_extra_fields = {
        "estado": SelectField(
            "Estado",
            choices=[
                ("Registrado", "Registrado"),
                ("En tránsito", "En tránsito"),
                ("Entregado", "Entregado"),
                ("Cancelado", "Cancelado")
            ],
            widget=Select2Widget()
        ),
        "origen": SelectField(
            "Origen",
            choices=CIUDADES,
            widget=Select2Widget()
        ),

        "destino": SelectField(
            "Destino",
            choices=CIUDADES,
            widget=Select2Widget()
        )
    }

    edit_form_extra_fields = {
        "estado": SelectField(
            "Estado",
            choices=[
                ("Registrado", "Registrado"),
                ("En tránsito", "En tránsito"),
                ("Entregado", "Entregado"),
                ("Cancelado", "Cancelado")
            ],
            widget=Select2Widget()
        ),
        "origen": SelectField(
            "Origen",
            choices=CIUDADES,
            widget=Select2Widget()
        ),

        "destino": SelectField(
            "Destino",
            choices=CIUDADES,
            widget=Select2Widget()
        )
    }

    def pre_add(self, item):
        if item.origen == item.destino:
            raise ValidationError("Origen y destino no pueden ser iguales")

    def pre_update(self, item):
        if item.origen == item.destino:
            raise ValidationError("Origen y destino no pueden ser iguales")


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
        ).order_by(func.sum(Envio.precio).desc()).all()

        labels = [str(r[0]) for r in resultados]
        values = [float(r[1]) if r[1] else 0 for r in resultados]

        detalles = [
            {"fecha": str(r[0]), "total": float(r[1]) if r[1] else 0}
            for r in resultados
        ]

        analisis = analizar_ingresos(detalles)

        return jsonify({
            "labels": labels,
            "values": values,
            "detalles": detalles,
            "analisis": analisis
        })

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


class GraficosView(BaseView):
    route_base = "/graficos"
    default_view = "index"

    @expose('/')
    def index(self):
        return self.render_template("graficos/index.html")

    @expose('/heatmap_rutas')
    def heatmap_rutas(self):
        from_date = request.args.get('from_date', None)
        to_date = request.args.get('to_date', None)
        estado = request.args.get('estado', None)

        query = db.session.query(Envio)
        if from_date:
            query = query.filter(Envio.fecha_registro >= from_date)
        if to_date:
            query = query.filter(Envio.fecha_registro <= to_date)
        if estado and estado != 'todos':
            query = query.filter(Envio.estado == estado)

        envios = query.all()

        dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
        rutas_set = set()
        for e in envios:
            rutas_set.add(f"{e.origen} -> {e.destino}")
        rutas = sorted(list(rutas_set))

        heatmap_data = []
        for dia_idx, dia in enumerate(dias):
            row = []
            for ruta in rutas:
                count = sum(1 for e in envios if 
                    f"{e.origen} -> {e.destino}" == ruta and 
                    e.fecha_registro and e.fecha_registro.weekday() == dia_idx)
                row.append(count)
            heatmap_data.append(row)

        return jsonify({"dias": dias, "rutas": rutas, "data": heatmap_data})

    @expose('/estado_mes')
    def estado_mes(self):
        year = request.args.get('year', None)

        query = db.session.query(Envio)
        if year:
            query = query.filter(extract('year', Envio.fecha_registro) == int(year))

        envios = query.all()

        meses = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        estados = ['Registrado', 'En transito', 'Entregado', 'Cancelado']

        mes_data = {m: {e: 0 for e in estados} for m in meses}
        for e in envios:
            if e.fecha_registro and e.estado:
                mes_idx = e.fecha_registro.month - 1
                mes_name = meses[mes_idx]
                est = e.estado if e.estado in estados else 'Registrado'
                mes_data[mes_name][est] = mes_data.get(mes_name, {}).get(est, 0) + 1

        return jsonify({
            "meses": meses,
            "estados": estados,
            "data": mes_data,
            "labels": meses,
            "datasets": [
                {"label": "Registrado", "data": [mes_data[m].get("Registrado", 0) for m in meses], "backgroundColor": "#3366cc"},
                {"label": "En transito", "data": [mes_data[m].get("En transito", 0) for m in meses], "backgroundColor": "#ff9900"},
                {"label": "Entregado", "data": [mes_data[m].get("Entregado", 0) for m in meses], "backgroundColor": "#109618"},
                {"label": "Cancelado", "data": [mes_data[m].get("Cancelado", 0) for m in meses], "backgroundColor": "#dc3912"}
            ]
        })

    @expose('/estados')
    def estados(self):
        estados = db.session.query(Envio.estado).distinct().all()
        return jsonify([e[0] for e in estados])

    @expose('/years')
    def years(self):
        results = db.session.query(
            extract('year', Envio.fecha_registro).label('year')
        ).distinct().order_by(extract('year', Envio.fecha_registro).desc()).all()
        return jsonify([int(y[0]) for y in results if y[0]])


appbuilder.add_view(
    ReportesView,
    "Reportes",
    icon="fa-chart-bar",
    category="Gestion"
)

appbuilder.add_view(
    GraficosView,
    "Graficos",
    icon="fa-chart-line",
    category="Gestion"
)