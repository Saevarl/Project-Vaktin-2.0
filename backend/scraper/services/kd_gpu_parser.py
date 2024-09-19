from bs4 import BeautifulSoup

from backend.scraper.models.gpu_parser_model import GPUParserModel

class KDGPUParser:
    @staticmethod
    def extract_gpus(text_content):
        # remove junk from the start and end of the text_content
        text_content = text_content.split("Current filter:")[1]
        text_content = text_content.split("Karfa")[0]

        gpus = []
        lines = text_content.split("\n")
        for i, line in enumerate(lines):
            if line == "Setja í körfu":
                gpu_name = lines[i-9]
                gpu_link = lines[i-10].split(" ")[1][1:-1]
                gpu_price = lines[i-1].split("k")[0]
                if gpu_name.startswith("["):
                    gpu_name = lines[i-7]
                if gpu_name[0].isdigit():
                    gpu_name = lines[i-8]
                gpu = GPUParserModel(name=gpu_name, link=gpu_link, price=gpu_price)
                print(gpu)
                gpus.append(gpu)
                gpu = {}
        return gpus
    

        

        
