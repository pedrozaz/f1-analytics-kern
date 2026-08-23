"""
Entry point CLI — gera plots de telemetria F1 para o vídeo Vektor.

Uso:
    uv run f1-analytics-kern
"""

from __future__ import annotations

import logging

from f1_analytics_kern.data.loader import get_fastest_lap, get_telemetry, load_session
from f1_analytics_kern.plots.speed_trace import (
    plot_speed_trace_comparison,
    plot_speed_trace_single,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Gera os plots de telemetria do vídeo."""
    logger.info("=== F1 Analytics Kern ===")

    # ─── Demo: Speed Trace de um piloto em 2024 (dados públicos e disponíveis) ────
    # Usando 2024 como teste porque os dados estão completos e cacheáveis.
    # Para o vídeo final, trocar para 2025/2026 quando as sessões estiverem disponíveis.
    year = 2024
    gp = "Bahrain"
    driver = "VER"

    logger.info("Carregando sessão: %s %s Q", year, gp)
    session = load_session(year, gp, "Q")

    logger.info("Buscando volta mais rápida de %s", driver)
    fastest = get_fastest_lap(session, driver)
    telemetry = get_telemetry(fastest)

    logger.info("Gerando speed trace single...")
    plot_speed_trace_single(
        telemetry,
        driver=driver,
        year=year,
        gp=gp,
        session_type="Q",
    )
    logger.info("✅ Speed trace single salvo em output/")

    # ─── Demo: Comparação de dois pilotos ─────────────────────────────────────────
    driver_b = "LEC"

    logger.info("Buscando volta mais rápida de %s", driver_b)
    fastest_b = get_fastest_lap(session, driver_b)
    telemetry_b = get_telemetry(fastest_b)

    logger.info("Gerando speed trace comparativo...")
    plot_speed_trace_comparison(
        tel_a=telemetry,
        driver_a=driver,
        year_a=year,
        tel_b=telemetry_b,
        driver_b=driver_b,
        year_b=year,
        gp=gp,
        session_type="Q",
    )
    logger.info("✅ Speed trace comparativo salvo em output/")

    logger.info("Concluído.")


if __name__ == "__main__":
    main()
