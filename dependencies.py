from injector import inject, Module, provider, singleton
from config.settings import Settings
from endpoints import router
from fastapi import APIRouter, FastAPI

from services.scraper import Scraper
from services.parser import Parser

class FastAPIModule(Module):
    @singleton
    @provider
    def provide_app(self, router: APIRouter) -> FastAPI:
        app = FastAPI()
        app.include_router(router)
        return app

class RouterModule(Module):
    @singleton
    @provider
    def provide_router(self) -> APIRouter:
        return router
    
class SettingsModule(Module):
    @singleton
    @provider
    def provide_settings(self) -> Settings:
        return Settings()
    
class ScraperModule(Module):
    @singleton
    @provider
    def provide_scraper(self) -> Scraper:
        return Scraper()

class ParserModule(Module):
    @singleton
    @provider
    def provide_parser(self) -> Parser:
        return Parser()
