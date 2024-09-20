import json
from datetime import datetime

from backend.scraper.services.gpu_score_scraper import scrape_gpu_scores
from backend.scraper.services.tt_gpu_parser import TTGPUParser
from backend.scraper.services.scraper import Scraper
from backend.scraper.services.parser import Parser
from backend.scraper.services.kd_gpu_parser import KDGPUParser
from backend.scraper.models.db_models import GPU, GPUModel, Store, Price
from backend.scraper.populate import populate_stores
from backend.database.connection import SessionLocal
# Ensure stores are populated
populate_stores()

# Load GPU URLs and parse descriptions
with open("backend/scraper/gpu_urls.json", "r") as f:
    gpu_urls = json.load(f)

""" with open("backend/scraper/parse_descriptions.json", "r") as f:
    parse_descriptions = json.load(f) """

# Initialize parsers and scrapers
scraper = Scraper()
parser = Parser()
kd_gpu_parser = KDGPUParser()
tt_gpu_parser = TTGPUParser()
#gpu_parse_descriptions = parse_descriptions["gpu_parse_description"]

# Scrape GPUs
kisildalur_gpus = []
tolvutaekni_gpus = []

for store, store_urls in gpu_urls.items():
    print(f"Scraping GPUs from {store}")
    
    for url in store_urls:
        page_source = scraper.get_page_source(url)
        cleaned_content = parser.clean_body_content(page_source)
        
        if store == "kisildalur":
            gpu_content = kd_gpu_parser.extract_gpus(cleaned_content)
            kisildalur_gpus.extend(gpu_content)
        elif store == "tolvutaekni":
            gpu_content = tt_gpu_parser.extract_gpus(cleaned_content)
            tolvutaekni_gpus.extend(gpu_content)
        
        print(f"Scraped {len(gpu_content)} GPUs from {url}")

scraper.close_driver()

print(f"\nKÍSILDALUR: {len(kisildalur_gpus)} GPUs")
print(f"TÖLVUTÆKNI: {len(tolvutaekni_gpus)} GPUs")

session = SessionLocal()

# Get store objects
kisildalur_store = session.query(Store).filter(Store.name == "Kisildalur").first()
tolvutaekni_store = session.query(Store).filter(Store.name == "Tölvutækni").first()

if not kisildalur_store:
    print("Kisildalur store not found")
if not tolvutaekni_store:
    print("Tölvutækni store not found")


# Scrape GPU benchmark scores
gpu_benchmark_scores = scrape_gpu_scores()

def get_or_create_gpu_model(gpu_obj):
    '''Takes a GPU object and returns the GPU model object from the database'''
    existing_model = session.query(GPUModel).filter(GPUModel.model == gpu_obj.model).first()
    if not existing_model:
        benchmark_score = get_benchmark_score(gpu_obj.model)
        gpu_model = GPUModel(
            model=gpu_obj.model,
            brand=gpu_obj.brand,
            series=gpu_obj.series,
            vram=gpu_obj.vram,
            benchmark_score=benchmark_score
        )
        session.add(gpu_model)
        session.flush()
        return gpu_model
    return existing_model

def get_benchmark_score(model):
    '''Takes a GPU model and returns the benchmark score from the gpu_benchmark_scores dictionary'''
    for key, value in gpu_benchmark_scores.items():
        if key in model:
            return int(str(value).replace(',', '')) if value else None
    return None

def get_or_create_gpu(gpu_obj, gpu_model):
    '''Takes a GPU object and a GPU model and returns the GPU object from the database'''
    existing_gpu = session.query(GPU).filter(
        GPU.name == gpu_obj.name,
        GPU.link == gpu_obj.link
    ).first()
    if not existing_gpu:
        gpu = GPU(name=gpu_obj.name, link=gpu_obj.link, model=gpu_model, manufacturer=gpu_obj.manufacturer)
        session.add(gpu)
        session.flush()
        return gpu
    return existing_gpu

def update_price(gpu, store, new_price):
    '''Takes a GPU object, a store object and a new price and updates the price in the database if the price is different from the latest price'''
    latest_price = session.query(Price).filter(
        Price.gpu_id == gpu.id,
        Price.store_id == store.id
    ).order_by(Price.date_checked.desc()).first()

    if not latest_price or latest_price.price != new_price:
        new_price_entry = Price(price=new_price, date_checked=datetime.now(), store=store, gpu=gpu)
        session.add(new_price_entry)

def add_or_update_gpus_and_prices(gpus, store):
    '''Takes a list of GPU objects and a store object and adds or updates the GPUs and prices in the database'''
    for gpu_obj in gpus:
        print(gpu_obj)
        if gpu_obj.model != "Unknown":
            gpu_model = get_or_create_gpu_model(gpu_obj)
            gpu = get_or_create_gpu(gpu_obj, gpu_model)
            update_price(gpu, store, gpu_obj.price)



add_or_update_gpus_and_prices(kisildalur_gpus, kisildalur_store)
add_or_update_gpus_and_prices(tolvutaekni_gpus, tolvutaekni_store)

session.commit()
session.close()