from bs4 import BeautifulSoup
from backend.scraper.models.gpu_parser_model import GPUParserModel
from backend.scraper.services.gpu_llm_parser import GPULLMParser

class TTGPUParser:
    @staticmethod
    def extract_gpus(text_content):
        # remove junk from the start and end of the text_content
        text_content = text_content.split("Velja nánar")[1]
        text_content = text_content.split("Hafðu samband:")[0]

        
        gpus = []
        lines = text_content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("[Link:"):
                
                link = line.split(" ")[1][1:-1]
                name = lines[i+1]
                price = lines[i+3].split(" ")[0]
                gpu = GPUParserModel(name=name, link=link, price=price)
                print(gpu)
                gpus.append(gpu)
                
        """ llm_parser = GPULLMParser()

        lines = text_content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("[Link:"):
                link = line.split(" ")[1][1:-1]
                name = lines[i + 1]
                price = lines[i + 3].split(" ")[0]
                
                # Combine name and price into a single GPU text entry
                gpu_text = f"{name}, {price}"
                
                # Use the LLM parser to extract detailed GPU information
                parsed_gpu = llm_parser.parse(gpu_text)
                
                # Print parsed data for testing
                print(f"Parsed GPU info: {parsed_gpu}")

                print(f"GPU {i}: ", gpu_text)
                print() """

        
        return gpus

        
