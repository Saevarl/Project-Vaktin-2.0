import json
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

class GPULLMParser:
    def __init__(self, model_name="phi3:3.8b"):
        self.model = OllamaLLM(model=model_name)
        self.template = """
            Extract GPU details from the following text, including: name, price, series, brand, model, manufacturer, and vram. Exclude extra technical details (e.g., ports). Use the examples for guidance.

            name: Full model name, including branding or OC edition.
            price: Numeric value, no currency symbols or extra formatting.
            series: Identify series from model (e.g., RTX 3050 → 3000 series, RX 7900XT → 7000 series).
            brand: Nvidia or AMD based on model.
            manufacturer: Company making the GPU (e.g., ASUS, Gigabyte, etc.).
            vram: VRAM capacity (e.g., 6GB, 24GB).

            IMPORTANT:
            The output should be on a json format and parsable using json.loads() function.

            Example input:
            "ASRock Phantom Gaming Radeon RX 7900 XTX 24GB - OC Edition, 177,900 Kr."

            Example output:

          {{
            "name": "ASRock Phantom Gaming Radeon RX 7900 XTX 24GB - OC Edition",
            "price": "177900",
            "series": "7000 series",
            "brand": "AMD",
            "model": "RX 7900 XTX",
            "manufacturer": "ASRock",
            "vram": "24GB"
          }}

            Input: "{input}"
            """


    def parse(self, gpu_info):
        prompt = ChatPromptTemplate.from_template(self.template)
        chain = prompt | self.model

        response = chain.invoke({"input": gpu_info})
        try:
            parsed_response = json.loads(response)
        except json.JSONDecodeError:
            parsed_response = {}

        print(parsed_response)
        return parsed_response




        
        
