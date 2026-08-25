"""
Speed Trace — Velocidade por Distância (overlay comparativo).

Gera o gráfico principal de telemetria: curva de velocidade ao longo do
circuito para um ou dois pilotos/anos, com anotações de broadcast.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib.pyplot as plt

from f1_analytics_kern.config import (
    EXPORT_CONFIG,
    OUTPUT_DIR,
    PALETTE,
    WATERMARK_TEXT,
)
from f1_analytics_kern.plots.style import create_figure

if TYPE_CHECKING:
    from fastf1.core import Telemetry


def plot_speed_trace_single(
    telemetry: Telemetry,
    driver: str,
    year: int,
    gp: str,
    session_type: str = "Q",
    *,
    color: str | None = None,
    save: bool = True,
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plota o speed trace de um único piloto.

    Args:
        telemetry: DataFrame de telemetria com colunas Distance e Speed.
        driver: Código do piloto (ex: 'RUS').
        year: Ano da temporada.
        gp: Nome do GP (ex: 'Australia').
        session_type: Tipo da sessão (ex: 'Q').
        color: Cor da linha. Default: era_2026 ciano.
        save: Se deve salvar o PNG em output/.

    Returns:
        Tupla (fig, ax).
    """
    if color is None:
        color = PALETTE["era_2026"]

    fig, ax = create_figure()

    ax.plot(
        telemetry["Distance"],
        telemetry["Speed"],
        color=color,
        linewidth=2.0,
        label=f"{driver} — {year}",
    )

    ax.set_xlabel("Distância (m)")
    ax.set_ylabel("Velocidade (km/h)")
    ax.set_title(
        f"Speed Trace — {driver} | {gp} {year} ({session_type})",
        fontweight="bold",
        pad=16,
    )
    ax.legend(loc="upper right")

    # Watermark
    fig.text(
        0.5,
        0.01,
        WATERMARK_TEXT,
        ha="center",
        fontsize=7,
        color=PALETTE["text_muted"],
        style="italic",
    )

    if save:
        out = OUTPUT_DIR / f"speed_trace_{driver}_{gp}_{year}.png"
        fig.savefig(out, dpi=EXPORT_CONFIG["dpi"], format=EXPORT_CONFIG["format"])

    return fig, ax


def plot_speed_trace_comparison(
    tel_a: Telemetry,
    driver_a: str,
    year_a: int,
    tel_b: Telemetry,
    driver_b: str,
    year_b: int,
    gp: str,
    session_type: str = "Q",
    *,
    color_a: str | None = None,
    color_b: str | None = None,
    save: bool = True,
) -> tuple[plt.Figure, plt.Axes]:
    """
    Plota o speed trace comparativo de dois pilotos ou dois anos sobrepostos.

    Args:
        tel_a: Telemetria do primeiro piloto/ano.
        driver_a: Código do primeiro piloto.
        year_a: Ano do primeiro dataset.
        tel_b: Telemetria do segundo piloto/ano.
        driver_b: Código do segundo piloto.
        year_b: Ano do segundo dataset.
        gp: Nome do GP.
        session_type: Tipo da sessão.
        color_a: Cor da primeira linha. Default: era_2025 vermelho.
        color_b: Cor da segunda linha. Default: era_2026 ciano.
        save: Se deve salvar o PNG.

    Returns:
        Tupla (fig, ax).
    """
    if color_a is None:
        color_a = PALETTE["era_2025"]
    if color_b is None:
        color_b = PALETTE["era_2026"]

    fig, ax = create_figure()

    ax.plot(
        tel_a["Distance"],
        tel_a["Speed"],
        color=color_a,
        linewidth=2.0,
        alpha=0.85,
        label=f"{driver_a} — {year_a}",
    )
    ax.plot(
        tel_b["Distance"],
        tel_b["Speed"],
        color=color_b,
        linewidth=2.0,
        alpha=0.85,
        label=f"{driver_b} — {year_b}",
    )

    ax.set_xlabel("Distância (m)")
    ax.set_ylabel("Velocidade (km/h)")

    if year_a == year_b:
        title = f"Speed Trace — {driver_a} vs {driver_b} | {gp} {year_a} ({session_type})"
    else:
        title = f"Speed Trace — {gp} {year_a} vs {year_b} ({session_type})"

    ax.set_title(title, fontweight="bold", pad=16)
    ax.legend(loc="upper right")

    # Watermark
    fig.text(
        0.5,
        0.01,
        WATERMARK_TEXT,
        ha="center",
        fontsize=7,
        color=PALETTE["text_muted"],
        style="italic",
    )

    if save:
        out = OUTPUT_DIR / f"speed_compare_{driver_a}v{driver_b}_{gp}_{year_a}v{year_b}.png"
        fig.savefig(out, dpi=EXPORT_CONFIG["dpi"], format=EXPORT_CONFIG["format"])

    return fig, ax
