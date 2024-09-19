from typing import Optional, Any
from pydantic import BaseModel, Field
import re

class GPUParserModel(BaseModel):
    name: str
    link: Optional[str] = None  # Made link optional with a default of None
    price: str
    series: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    manufacturer: Optional[str] = None
    vram: Optional[str] = None

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.series = self.get_series()
        self.brand = self.get_brand()
        self.vram = self.get_vram()
        self.model = self.get_model()
        self.manufacturer = self.get_manufacturer()
        

    def __str__(self):
        return (f"Name: {self.name}, Link: {self.link}, Price: {self.price}, "
                f"Series: {self.series}, Brand: {self.brand}, Model: {self.model}, "
                f"Manufacturer: {self.manufacturer}, "
                f"VRAM: {self.vram}")
    
    def __repr__(self):
        return self.__str__()
    
    def normalize_name(self):
        '''Normalizes the name of the GPU, 4060Ti -> 4060 Ti or 4080S -> 4080 Super etc'''
        self.name = re.sub(r"(\d{4})(Ti)", r"\1 Ti", self.name)
        self.name = re.sub(r"(\d{4})(XT)", r"\1 XT", self.name)
        self.name = re.sub(r"(\d{4})(XTX)", r"\1 XT", self.name)
        self.name = re.sub(r"(\d{4})(S)", r"\1 Super", self.name)
        self.name = re.sub(r"(\d{4})(Super)", r"\1 Super", self.name)
        self.name = re.sub(r"(\d{4})(GRE)", r"\1 GRE", self.name)

    def remove_technical_information_from_name(self):
        '''Removes technical information from the name of the GPU, ASUS RTX 3050 6GB Dual OC, 1xDisplayPort, 1xHDMI, 1xDVI -> ASUS RTX 3050 6GB Dual OC'''
        self.name = self.name.split(",")[0]
      
    def get_series(self):
        '''Extracts the series of the GPU, e.g. 3000 series, 4000 series, 6000 series, 7000 series'''
        self.normalize_name()
        self.remove_technical_information_from_name()
        if "nvidia" in self.name.lower() or "geforce" in self.name.lower() or "rtx" in self.name.lower():
            for word in self.name.split(" "):
                if word.isdigit() and len(word) == 4:
                    if word[0] == "3":
                        return "3000 series"
                    elif word[0] == "4":
                        return "4000 series"
        elif "amd" in self.name.lower() or "radeon" in self.name.lower() or "rx" in self.name.lower():
            for word in self.name.split(" "):
                if word.isdigit() and len(word) == 4:
                    if word[0] == "6":
                        return "6000 series"
                    elif word[0] == "7":
                        return "7000 series"
        return "Unknown"
    
    def get_brand(self):
        '''Extracts the brand of the GPU, either Nvidia or AMD'''
        if self.series == "3000 series" or self.series == "4000 series":
            return "Nvidia"
        elif self.series == "6000 series" or self.series == "7000 series":
            return "AMD"
        return "Unknown"

    def get_model(self):
        '''Extracts the model of the GPU, e.g. RTX 3060, RX 6700 XT, from the name'''
        if self.brand == "Nvidia":
            for i, word in enumerate(self.name.split(" ")):
                if word.lower() == "rtx":
                    ret_str = "RTX " + self.name.split(" ")[i+1]
                    if i+2 < len(self.name.split(" ")):
                        if self.name.split(" ")[i+2].lower() == "ti":
                            ret_str += " Ti"
                            # if Ti is followed by "Super"
                            if self.name.split(" ")[i+3].lower() == "super":
                                ret_str += " Super"
                        elif self.name.split(" ")[i+2].lower() == "super":
                            ret_str += " Super"
                    return ret_str + " " + self.vram
        elif self.brand == "AMD":
            for i, word in enumerate(self.name.split(" ")):
                if word.lower() == "rx":
                    ret_str = "RX " + self.name.split(" ")[i+1]
                    if i+2 < len(self.name.split(" ")):
                        if self.name.split(" ")[i+2].lower() == "xt":
                            ret_str += " XT"
                        elif self.name.split(" ")[i+2].lower() == "xtx":
                            ret_str += " XTX"
                        elif self.name.split(" ")[i+2].lower() == "gre":
                            ret_str += " GRE"
                    return ret_str + " " + self.vram
        return "Unknown"

    def get_manufacturer(self):
        '''Returns the manufacturer of the GPU, e.g. ASUS, Gigabyte, MSI, etc, by extracting the first word of the name'''
        return self.name.split(" ")[0]
    
    def get_vram(self):
        '''Returns the VRAM of the GPU in GB'''
        match = re.search(r"(\d{1,2}) ?GB", self.name)
        if match:
            return match.group(1) + "GB"
        return "Unknown"
    
    class Config:
        from_attributes = True
