import sys
import os
from sqlalchemy import text

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import SessionLocal
from app.models import Usuario

def check_users():
    print("🔍 Verificando usuarios en la base de datos...")
    db = SessionLocal()
    try:
        users = db.query(Usuario).all()
        print(f"📊 Total usuarios encontrados: {len(users)}")
        
        for user in users:
            print(f"   👤 Usuario: {user.email}")
            print(f"      ID: {user.id}")
            print(f"      Activo: {user.activo}")
            print(f"      Superusuario: {user.es_superusuario}")
            print(f"      Hash inicio: {user.contrasena_hash[:10]}...")
            print("---")
            
    except Exception as e:
        print(f"❌ Error al leer base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_users()
