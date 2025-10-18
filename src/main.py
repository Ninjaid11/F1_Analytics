from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from src.f1_idea.f1_analytics import F1Analytics
from src.f1_idea.f1_compare import F1Compare
from src.scraper import F1Scraper
from src.config import Settings
from src.db import sessionmanager, get_db_session
from src.database.crud import create_report
from src.api.routes.testt_router import router as testt_router

class F1AnalyticsApp:
    def __init__(self, db_url: str):
        self.settings = Settings()
        self.db_url = db_url
        self.scraper = F1Scraper()
        self.app = FastAPI(title="F1 Analytics API", lifespan=self.lifespan)
        self.app.include_router(testt_router, prefix="/test")
        self._setup_frontend()
        self._setup_routes()
        self.analytics = F1Analytics()
        self.compare = F1Compare()

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        app.state.scraper = self.scraper
        sessionmanager.init(self.db_url)

        await sessionmanager.init_tables()

        yield

        if sessionmanager._engine is not None:
            await sessionmanager.close()

    def _setup_frontend(self):
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        self.templates = Jinja2Templates(directory="templates")

    def _setup_routes(self):
        @self.app.get("/compare_page", include_in_schema=False)
        async def compare_page(request: Request):
            return self.templates.TemplateResponse("compare.html", {"request": request})

        @self.app.get("/analytics_page", include_in_schema=False)
        async def analytics_page(request: Request):
            return self.templates.TemplateResponse("analytics.html", {"request": request})

        @self.app.get("/pilots")
        def get_pilots():
            scraper: F1Scraper = self.app.state.scraper
            pilots = scraper.get_pilots()
            return pilots # {"title": "Турнирная таблица", "pilots": pilots}

        @self.app.get("/results")
        def get_results():
            scraper: F1Scraper = self.app.state.scraper
            results = scraper.get_results()
            return {"title": "Last results", "results": results}

        @self.app.get("/analytics", response_model=None)
        async def get_analytics(db: AsyncSession = Depends(get_db_session)):
            scraper: F1Scraper = self.app.state.scraper
            pilots = scraper.get_pilots()
            results = scraper.get_results()

            report_text = self.analytics.analyze_f1_data(pilots, results)

            await create_report(
                db=db,
                prompt="данные о пилотах и гонках",
                response=report_text
            )

            return {"report": report_text}

        @self.app.get("/compare")
        async def compare_pilots(pilot1: str, pilot2: str, db: AsyncSession = Depends(get_db_session)):
            pilots = self.scraper.get_pilots()

            report_text = self.compare.compare_pilots(pilot1, pilot2, pilots)

            await create_report(
                db=db,
                prompt=f"Сравнение пилотов {pilot1} и {pilot2}",
                response=report_text
            )

            return  {"report": report_text}


f1_app = F1AnalyticsApp(db_url=Settings().DB_URL)
app = f1_app.app