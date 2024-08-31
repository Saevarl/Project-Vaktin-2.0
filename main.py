from injector import Injector
from fastapi import FastAPI
import uvicorn

from dependencies import FastAPIModule, RouterModule, SettingsModule, ScraperModule, ParserModule

if __name__ == "__main__":
    # Initialize the injector with the necessary modules
    injector = Injector([FastAPIModule(), RouterModule(), SettingsModule(), ScraperModule(), ParserModule()])


    # Retrieve the FastAPI app instance from the injector
    app = injector.get(FastAPI)

    # Run the FastAPI app with Uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8090)
