from datetime import datetime, timedelta
import random
from faker import Faker

fake = Faker(['es_ES', 'es_MX'])

from app import create_app
from app.extensions import db
from app.models import Cliente, Vehiculo, RutaViaje, Envio

def seed():
    app = create_app()
    with app.app_context():
        db.create_all()

        Cliente.query.delete()
        Vehiculo.query.delete()
        RutaViaje.query.delete()
        Envio.query.delete()
        db.session.commit()

        print("Creando clientes...")
        clientes = []
        for i in range(30):
            cliente = Cliente(
                nombre=fake.name(),
                telefono=f"+591 " + str(random.randint(60000000, 79999999)),
                carnet=str(random.randint(1000000, 9999999))
            )
            db.session.add(cliente)
            clientes.append(cliente)
        db.session.commit()

        print("Creando vehículos...")
        vehiculos = []
        tipos = ["Camión", "Camioneta", "Furgón", "Semi Trailer", "Trailer"]
        for i in range(10):
            vehiculo = Vehiculo(
                placa=f"{fake.license_plate()}-{random.randint(1,9)}",
                tipo=random.choice(tipos),
                capacidad_kg=random.uniform(500, 5000)
            )
            db.session.add(vehiculo)
            vehiculos.append(vehiculo)
        db.session.commit()

        print("Creando rutas...")
        rutas = []
        ciudades = ["La Paz", "Santa Cruz", "Cochabamba", "Sucre", "Tarija", "Potosí", "Oruro", "Beni", "Pando", "Chuquisaca"]
        for i in range(20):
            origen = random.choice(ciudades)
            destino = random.choice([c for c in ciudades if c != origen])
            fecha_salida = fake.date_between(start_date='-60d', end_date='+30d')
            fecha_llegada = fecha_salida + timedelta(days=random.randint(1, 5))
            
            ruta = RutaViaje(
                origen=origen,
                destino=destino,
                fecha_salida=fecha_salida,
                fecha_llegada=fecha_llegada,
                vehiculo=random.choice(vehiculos)
            )
            db.session.add(ruta)
            rutas.append(ruta)
        db.session.commit()

        print("Creando envíos...")
        estados = ["Registrado", "En tránsito", "Entregado", "Cancelado"]
        for i in range(50):
            fecha_registro = fake.date_between(start_date='-90d', end_date='today')
            
            origen = random.choice(ciudades)
            destino = random.choice([c for c in ciudades if c != origen])
            
            envio = Envio(
                codigo=f"ENV-{random.randint(10000, 99999)}",
                descripcion=fake.sentence(nb_words=6),
                peso=random.uniform(0.5, 100),
                precio=random.uniform(10, 500),
                estado=random.choice(estados),
                origen=origen,
                destino=destino,
                fecha_registro=fecha_registro,
                cliente=random.choice(clientes),
                viaje=random.choice(rutas)
            )
            db.session.add(envio)
        db.session.commit()

        print("")
        print("30 clientes creados")
        print("10 vehiculos creados")
        print("20 rutas creadas")
        print("50 envios creados")
        print("")
        print("Datos semilla generados exitosamente!")

if __name__ == "__main__":
    seed()