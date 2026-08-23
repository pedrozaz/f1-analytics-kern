"""
Entry point CLI — gera gráficos e vídeos animados de telemetria F1 para o vídeo Vektor.

Uso:
    uv run f1-analytics-kern                 # Gera plots estáticos e vídeo MP4 de demo
    uv run f1-analytics-kern --video-only    # Gera apenas os vídeos animados
"""

from __future__ import annotations

import argparse
import logging

from f1_analytics_kern.data.loader import get_fastest_lap, get_telemetry, load_session
from f1_analytics_kern.plots.animated_telemetry import render_animated_telemetry_video
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
    """Gera os plots e vídeos de telemetria."""
    parser = argparse.ArgumentParser(
        description="F1 Analytics Broadcast Visualizations & Animations"
    )
    parser.add_argument("--year", type=int, default=2024, help="Ano da temporada (default: 2024)")
    parser.add_argument("--gp", type=str, default="Bahrain", help="Nome do GP (default: Bahrain)")
    parser.add_argument(
        "--driver-a", type=str, default="VER", help="Código do piloto A (default: VER)"
    )
    parser.add_argument(
        "--driver-b", type=str, default="LEC", help="Código do piloto B (default: LEC)"
    )
    parser.add_argument("--video-only", action="store_true", help="Gera apenas o vídeo animado")
    parser.add_argument(
        "--duration", type=float, default=12.0, help="Duração do vídeo em segundos (default: 12.0)"
    )
    parser.add_argument("--fps", type=int, default=60, help="FPS do vídeo (default: 60)")

    args = parser.parse_args()

    logger.info("=== F1 Analytics Kern — Broadcast Engine ===")
    logger.info("Carregando sessão: %s %s Q", args.year, args.gp)
    session = load_session(args.year, args.gp, "Q")

    logger.info("Extraindo telemetria de %s e %s...", args.driver_a, args.driver_b)
    lap_a = get_fastest_lap(session, args.driver_a)
    tel_a = get_telemetry(lap_a)

    lap_b = get_fastest_lap(session, args.driver_b)
    tel_b = get_telemetry(lap_b)

    if not args.video_only:
        logger.info("1. Gerando speed trace single (PNG 4K)...")
        plot_speed_trace_single(
            tel_a, driver=args.driver_a, year=args.year, gp=args.gp, session_type="Q"
        )

        logger.info("2. Gerando speed trace comparativo (PNG 4K)...")
        plot_speed_trace_comparison(
            tel_a=tel_a,
            driver_a=args.driver_a,
            year_a=args.year,
            tel_b=tel_b,
            driver_b=args.driver_b,
            year_b=args.year,
            gp=args.gp,
            session_type="Q",
        )

    logger.info("3. Renderizando animação de telemetria em vídeo MP4 (60 FPS)...")
    video_path = render_animated_telemetry_video(
        tel_a=tel_a,
        driver_a=args.driver_a,
        year_a=args.year,
        gp=args.gp,
        session_type="Q",
        tel_b=tel_b,
        driver_b=args.driver_b,
        year_b=args.year,
        session=session,
        fps=args.fps,
        duration_sec=args.duration,
    )

    logger.info("🏁 Render concluído com sucesso!")
    logger.info("Arquivo de vídeo pronto para edição: %s", video_path)


if __name__ == "__main__":
    main()
