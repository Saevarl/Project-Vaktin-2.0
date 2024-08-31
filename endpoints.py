from fastapi import APIRouter, Depends
from services.scraper import Scraper
from services.parser import Parser

router = APIRouter()

@router.get("/scrape")
async def scrape_url(url: str, scraper: Scraper = Depends(), parser: Parser = Depends()):
    # Use the Scraper to get the page source
    page_source = scraper.get_page_source(url)
    
    # Use the Parser to process the page source
    body_content = parser.extract_body_content(page_source)
    cleaned_content = parser.clean_body_content(body_content)
    
    # Optionally split the content
    split_content = parser.split_dom_content(cleaned_content)
    
    # Return the cleaned content
    return {"cleaned_content": cleaned_content}

@router.get("/gpus")
async def scrape_gpus(scraper: Scraper = Depends(), parser: Parser = Depends()):
    

