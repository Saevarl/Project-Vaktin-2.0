import json
from datetime import datetime

from backend.scraper.services.tt_gpu_parser import TTGPUParser
from backend.scraper.services.scraper import Scraper
from backend.scraper.services.parser import Parser
from backend.scraper.services.kd_gpu_parser import KDGPUParser
from backend.scraper.models.db_models import GPU, Store, Price
from backend.scraper.populate import populate_stores
from backend.database.connection import SessionLocal
# Ensure stores are populated
populate_stores()

# Load GPU URLs and parse descriptions
with open("backend/scraper/gpu_urls.json", "r") as f:
    gpu_urls = json.load(f)

with open("backend/scraper/parse_descriptions.json", "r") as f:
    parse_descriptions = json.load(f)

# Initialize parsers and scrapers
scraper = Scraper()
parser = Parser()
kd_gpu_parser = KDGPUParser()
tt_gpu_parser = TTGPUParser()
gpu_parse_descriptions = parse_descriptions["gpu_parse_description"]

# Scrape GPUs
kisildalur_gpus = []
tolvutaekni_gpus = []

for store, store_urls in gpu_urls.items():
    print(f"Scraping GPUs from {store}")
    store_gpus = []
    
    for category, url in store_urls.items():
        page_source = scraper.get_page_source(url)
        cleaned_content = parser.clean_body_content(page_source)
        
        if store == "kisildalur":
            gpu_content = kd_gpu_parser.extract_gpus(cleaned_content)
        elif store == "tolvutaekni":
            gpu_content = tt_gpu_parser.extract_gpus(cleaned_content)
        
        store_gpus.extend(gpu_content)

    if store == "kisildalur":
        kisildalur_gpus = store_gpus
    elif store == "tolvutaekni":
        tolvutaekni_gpus = store_gpus

scraper.close_driver()

print(f"\nKÍSILDALUR: {kisildalur_gpus}")
print(f"TÖLVUTÆKNI: {tolvutaekni_gpus}")

session = SessionLocal()

# Get store objects
kisildalur_store = session.query(Store).filter(Store.name == "Kisildalur").first()
tolvutaekni_store = session.query(Store).filter(Store.name == "Tölvutækni").first()

if not kisildalur_store:
    print("Kisildalur store not found")
if not tolvutaekni_store:
    print("Tölvutækni store not found")

def add_or_update_gpus_and_prices(gpus, store):
    for gpu_obj in gpus:
        print(gpu_obj)
        if gpu_obj.model != "Unknown":
            # Check if GPU exists
            existing_gpu = session.query(GPU).filter(
                GPU.name == gpu_obj.name,
                GPU.link == gpu_obj.link
            ).first()

            if not existing_gpu:
                # Add new GPU
                gpu = GPU(name=gpu_obj.name, model=gpu_obj.model, manufacturer=gpu_obj.manufacturer, 
                          brand=gpu_obj.brand, series=gpu_obj.series, vram=gpu_obj.vram, link=gpu_obj.link)
                session.add(gpu)
                session.flush()  
                
                # Add price entry for new GPU
                new_price = Price(price=gpu_obj.price, store=store, gpu=gpu)
                session.add(new_price)
            else:
                # check if price has changed
                latest_price = session.query(Price).filter(
                    Price.gpu_id == existing_gpu.id,
                    Price.store_id == store.id
                ).order_by(Price.date.desc()).first()

                if not latest_price or latest_price.price != gpu_obj.price:
                    # Add new price entry if price has changed
                    new_price = Price(price=gpu_obj.price, date=datetime.now(), store=store, gpu=existing_gpu)
                    session.add(new_price)


add_or_update_gpus_and_prices(kisildalur_gpus, kisildalur_store)
add_or_update_gpus_and_prices(tolvutaekni_gpus, tolvutaekni_store)

session.commit()
session.close()