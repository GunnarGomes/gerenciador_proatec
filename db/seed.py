from .database import SessionLocal, engine, Base
from .models import TipoDispositivo, Sala, Guardiao, Dispositivo

def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    if not db.query(TipoDispositivo).first():
        tipos = ["Notebook", "Tablet", "Computador de Sala"]
        for t in tipos:
            db.add(TipoDispositivo(nome=t))

    if not db.query(Sala).first():
        salas = ["Sala de Informática 1", "Sala de Informática 2", "Sala de Informática 3"]
        for s in salas:
            db.add(Sala(nome=s))

    if not db.query(Guardiao).first():
        guardioes = [
            Guardiao(nome="Guardião de Notebooks"),
            Guardiao(nome="Guardião de Tablets")
        ]
        db.add_all(guardioes)
        db.flush()  # gera IDs para relacionar

        # busca tipos
        tipo_notebook = db.query(TipoDispositivo).filter_by(nome="Notebook").first()
        tipo_tablet = db.query(TipoDispositivo).filter_by(nome="Tablet").first()
        tipo_sala = db.query(TipoDispositivo).filter_by(nome="Computador de Sala").first()

        # cria dispositivos
        db.add_all([
            Dispositivo(nome="Sala Informática 1", tipo_id=tipo_sala.id, localizacao_tipo="sala", localizacao_id=1, total=1, disponivel=1),
            Dispositivo(nome="Sala Informática 2", tipo_id=tipo_sala.id, localizacao_tipo="sala", localizacao_id=2, total=1, disponivel=1),
            Dispositivo(nome="Sala Informática 3", tipo_id=tipo_sala.id, localizacao_tipo="sala", localizacao_id=3, total=1, disponivel=1),
            Dispositivo(nome="Notebooks", tipo_id=tipo_notebook.id, localizacao_tipo="guardiao", localizacao_id=1, total=40, disponivel=40),
            Dispositivo(nome="Tablets", tipo_id=tipo_tablet.id, localizacao_tipo="guardiao", localizacao_id=2, total=40, disponivel=40)
        ])

    db.commit()
    db.close()
