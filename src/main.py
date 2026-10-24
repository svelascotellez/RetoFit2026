"""
Punto de Entrada Principal de Reto Fit 2026 (FastAPI + Uvicorn)
Listo para ejecucion y despliegue en Railway.com.
"""
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from src.application.challenge_service import ChallengeService
from src.presentation.api import router, get_challenge_service
from src.presentation.web_views import render_dashboard_html

def get_service() -> ChallengeService:
    """Proveedor inyectable del servicio orquestador."""
    return get_challenge_service()

app = FastAPI(
    title="Reto Fit 2026 - DIDT",
    description="Sistema de gestión físico y financiero para el evento Reto Fit de la DIDT.",
    version="1.0.0",
)

# Montar endpoints REST
app.include_router(router)


@app.get("/", response_class=HTMLResponse, summary="Dashboard Web Reto Fit")
def root_view(service: ChallengeService = Depends(get_service)) -> HTMLResponse:
    """Sirve la aplicacion web interactiva en Dark Mode Energy Neon con tarjetas Bento Grid."""
    html_content = render_dashboard_html(service)
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
