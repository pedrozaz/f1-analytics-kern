"""
Módulo de visualização e geração de gráficos broadcast e animações de vídeo.
"""

from f1_analytics_kern.plots.animated_telemetry import render_animated_telemetry_video
from f1_analytics_kern.plots.speed_trace import (
    plot_speed_trace_comparison,
    plot_speed_trace_single,
)
from f1_analytics_kern.plots.style import apply_vektor_theme, create_figure

__all__ = [
    "apply_vektor_theme",
    "create_figure",
    "plot_speed_trace_single",
    "plot_speed_trace_comparison",
    "render_animated_telemetry_video",
]
