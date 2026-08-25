"""
Testes de configuração e tema.
"""

from f1_analytics_kern.config import EXPORT_CONFIG, PALETTE, TEAM_COLORS
from f1_analytics_kern.plots.style import apply_vektor_theme, create_figure


def test_palette_and_config() -> None:
    """Verifica se a paleta contém as chaves essenciais."""
    assert "bg_dark" in PALETTE
    assert "era_2025" in PALETTE
    assert "era_2026" in PALETTE
    assert "text_primary" in PALETTE
    assert "Mercedes" in TEAM_COLORS
    assert EXPORT_CONFIG["dpi"] == 300


def test_create_figure() -> None:
    """Verifica se create_figure retorna uma tupla (fig, ax) válida."""
    apply_vektor_theme()
    fig, ax = create_figure()
    assert fig is not None
    assert ax is not None
