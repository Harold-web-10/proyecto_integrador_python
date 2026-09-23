from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, catalog, reviews, favorites

app = FastAPI(
    title=settings.APP_NAME,
    description="API de Red Social para Reseñas de Libros y Películas.",
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(catalog.router)
app.include_router(reviews.router)
app.include_router(favorites.router)


@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}
