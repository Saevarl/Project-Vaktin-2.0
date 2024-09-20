from bs4 import BeautifulSoup
from backend.scraper.services.scraper import Scraper

def scrape_gpu_scores():
    scraper = Scraper(headless=True)
    url = 'https://www.videocardbenchmark.net/high_end_gpus.html'
    
    try:
        page_source = scraper.get_page_source(url)
        soup = BeautifulSoup(page_source, 'html.parser')
        
        chartlist = soup.find('ul', class_='chartlist')
        gpu_benchmarks = {}
        
        if chartlist:
            for li in chartlist.find_all('li'):
                a_tag = li.find('a')
                if a_tag:
                    name_span = a_tag.find('span', class_='prdname')
                    score_span = a_tag.find('span', class_='count')
                    if name_span and score_span:
                        gpu_name = name_span.text.strip()
                        benchmark_score = score_span.text.strip()
                        if gpu_name.startswith("GeForce") or gpu_name.startswith("Radeon"):
                            if gpu_name.startswith("GeForce"):
                                gpu_name = gpu_name.replace("GeForce", "", 1).strip()
                            elif gpu_name.startswith("Radeon"):
                                gpu_name = gpu_name.replace("Radeon", "", 1).strip()
                            gpu_benchmarks[gpu_name] = benchmark_score
        
        return gpu_benchmarks
    
    finally:
        scraper.close_driver()

if __name__ == "__main__":
    gpu_data = scrape_gpu_scores()
    
    # Print the results
    for gpu, score in gpu_data.items():
        print(f"{gpu}: {score}")