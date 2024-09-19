from backend.scraper.models.db_models import Store, Base
from backend.database.connection import SessionLocal
from sqlalchemy import inspect

def populate_stores():
    session = SessionLocal()
    engine = session.get_bind()
    
    # Create tables if they don't exist
    Base.metadata.create_all(engine)
        
    # Check if stores already exist
    existing_stores = session.query(Store).all()
    if existing_stores:
        print("Stores already populated.")
        session.close()
        return

    # Populate stores
    store1 = Store(name="Tölvutækni", website_url="https://tolvutaekni.is", logo_url="https://vaktin.is/img/shopicons/tolvutaekni.png")
    store2 = Store(name="Kisildalur", website_url="https://kisildalur.is", logo_url="https://vaktin.is/img/shopicons/kisildalur.png")

    session.add_all([store1, store2])

    try:
        session.commit()
        print("Stores populated successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    populate_stores()