"""
Carregador de sessões e telemetria FastF1 com cache local integrado.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import fastf1

from f1_analytics_kern.config import CACHE_DIR

if TYPE_CHECKING:
    from fastf1.core import Lap, Laps, Session, Telemetry

logger = logging.getLogger(__name__)


def enable_cache() -> None:
    """Habilita o cache em disco do FastF1 no diretório configurado."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    fastf1.Cache.enable_cache(str(CACHE_DIR))


def load_session(
    year: int,
    gp: str | int,
    session_type: str = "Q",
    *,
    laps: bool = True,
    telemetry: bool = True,
    weather: bool = False,
    messages: bool = False,
) -> Session:
    """
    Carrega uma sessão específica de Fórmula 1 da API / cache.

    Args:
        year: Ano da temporada (ex: 2025, 2026).
        gp: Nome do GP (ex: 'Bahrain', 'Australia') ou número do round.
        session_type: Tipo de sessão ('FP1', 'FP2', 'FP3', 'Q', 'S', 'SQ', 'R').
        laps: Se deve carregar dados de voltas.
        telemetry: Se deve carregar canais de telemetria.
        weather: Se deve carregar dados climáticos.
        messages: Se deve carregar mensagens de rádio/direção de prova.

    Returns:
        Sessão carregada e pronta para consulta.
    """
    enable_cache()
    logger.info("Carregando sessão: %s %s - %s", year, gp, session_type)

    try:
        session = fastf1.get_session(year, gp, session_type)
        session.load(
            laps=laps,
            telemetry=telemetry,
            weather=weather,
            messages=messages,
        )
        return session
    except Exception as exc:
        logger.error("Erro ao carregar sessão %s %s %s: %s", year, gp, session_type, exc)
        raise


def get_fastest_lap(
    session: Session,
    driver: str | None = None,
) -> Lap:
    """
    Retorna a volta mais rápida da sessão ou de um piloto específico.

    Args:
        session: Sessão do FastF1 previamente carregada.
        driver: Código do piloto com 3 letras (ex: 'RUS', 'VER'). Se None, pega a mais rápida geral.

    Returns:
        Lap da volta mais rápida.

    Raises:
        ValueError: Se nenhuma volta válida for encontrada.
    """
    if driver is not None:
        laps = session.laps.pick_drivers(driver).pick_quicklaps()
        if laps.empty:
            raise ValueError(f"Nenhuma volta válida encontrada para o piloto '{driver}'.")
        fastest = laps.pick_fastest()
    else:
        laps = session.laps.pick_quicklaps()
        if laps.empty:
            raise ValueError("Nenhuma volta válida encontrada na sessão.")
        fastest = laps.pick_fastest()

    if fastest is None:
        raise ValueError("pick_fastest() retornou None — sem dados de tempo válidos.")

    return fastest


def get_telemetry(lap: Lap) -> Telemetry:
    """
    Extrai a telemetria contínua de uma volta.

    Colunas principais retornadas:
        - Distance (m): Distância percorrida no circuito
        - Speed (km/h): Velocidade instantânea
        - Throttle (%): Posição do acelerador (0 a 100)
        - Brake (bool): Aplicação do freio
        - nGear (int): Marcha engatada (0=N, 1-8)
        - RPM (int): Rotação do motor
        - DRS (int): Status do DRS / Modo Ativo
        - X, Y, Z (float): Coordenadas espaciais do carro na pista

    Returns:
        Telemetry DataFrame com canais de física sincronizados.

    Raises:
        ValueError: Se a telemetria estiver indisponível.
    """
    telemetry = lap.get_telemetry()
    if telemetry.empty:
        raise ValueError(f"Telemetria indisponível para a volta de {lap['Driver']}.")

    # Garante que a coluna Distance comece em 0
    if "Distance" in telemetry.columns:
        telemetry["Distance"] = telemetry["Distance"] - telemetry["Distance"].iloc[0]

    return telemetry


def get_driver_laps(session: Session, driver: str) -> Laps:
    """Retorna todas as voltas limpas (quicklaps) de um piloto em uma sessão."""
    return session.laps.pick_drivers(driver).pick_quicklaps()
