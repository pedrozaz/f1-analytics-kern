"""
Tema Matplotlib Broadcast Vektor — configuração global de rcParams.

Aplica fundo escuro, gridlines técnicas, tipografia consistente e paleta
de alto contraste para renderização em vídeo YouTube (1080p/4K).
"""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

from f1_analytics_kern.config import FONTS, PALETTE


def apply_vektor_theme() -> None:
    """Aplica o tema broadcast Vektor ao Matplotlib via rcParams."""

    bg = PALETTE["bg_dark"]
    text = PALETTE["text_primary"]
    secondary = PALETTE["text_secondary"]
    grid = PALETTE["grid_subtle"]

    mpl.rcParams.update(
        {
            # ─── Fundo ────────────────────────────────────
            "figure.facecolor": bg,
            "axes.facecolor": bg,
            "savefig.facecolor": bg,
            # ─── Texto ────────────────────────────────────
            "text.color": text,
            "axes.labelcolor": secondary,
            "xtick.color": secondary,
            "ytick.color": secondary,
            # ─── Tipografia ───────────────────────────────
            "font.family": "sans-serif",
            "font.sans-serif": [FONTS["family_sans"]],
            "font.size": FONTS["label_size"],
            "axes.titlesize": FONTS["title_size"],
            "axes.labelsize": FONTS["label_size"],
            "xtick.labelsize": FONTS["tick_size"],
            "ytick.labelsize": FONTS["tick_size"],
            "legend.fontsize": FONTS["tick_size"],
            # ─── Grid ────────────────────────────────────
            "axes.grid": True,
            "grid.color": grid,
            "grid.linewidth": 0.5,
            "grid.alpha": 0.6,
            # ─── Eixos ───────────────────────────────────
            "axes.edgecolor": grid,
            "axes.linewidth": 0.6,
            "axes.spines.top": False,
            "axes.spines.right": False,
            # ─── Linhas ──────────────────────────────────
            "lines.linewidth": 2.0,
            "lines.antialiased": True,
            # ─── Legenda ─────────────────────────────────
            "legend.facecolor": PALETTE["bg_card"],
            "legend.edgecolor": grid,
            "legend.framealpha": 0.9,
            # ─── Exportação ──────────────────────────────
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.3,
            "figure.dpi": 120,
        }
    )


def create_figure(
    figsize: tuple[float, float] | None = None,
    nrows: int = 1,
    ncols: int = 1,
) -> tuple[plt.Figure, plt.Axes]:
    """
    Cria uma figura com o tema Vektor já aplicado.

    Args:
        figsize: Tamanho (largura, altura) em polegadas. Default: 16x9.
        nrows: Número de linhas do grid de subplots.
        ncols: Número de colunas do grid de subplots.

    Returns:
        Tupla (fig, ax) pronta para uso.
    """
    from f1_analytics_kern.config import EXPORT_CONFIG

    apply_vektor_theme()

    if figsize is None:
        figsize = EXPORT_CONFIG["figsize_standard"]

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
    return fig, ax
