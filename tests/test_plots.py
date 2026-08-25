"""
Testes de geração de gráficos de telemetria.
"""

import numpy as np
import pandas as pd

from f1_analytics_kern.plots.speed_trace import (
    plot_speed_trace_comparison,
    plot_speed_trace_single,
)


def test_plot_speed_trace_single() -> None:
    """Gera speed trace single a partir de telemetria sintética."""
    distances = np.linspace(0, 5000, 500)
    speeds = 100 + 200 * np.sin(distances / 500) ** 2
    mock_tel = pd.DataFrame({"Distance": distances, "Speed": speeds})

    fig, ax = plot_speed_trace_single(
        telemetry=mock_tel,
        driver="RUS",
        year=2026,
        gp="Australia",
        session_type="Q",
        save=False,
    )
    assert fig is not None
    assert ax is not None


def test_plot_speed_trace_comparison() -> None:
    """Gera speed trace comparativo a partir de telemetrias sintéticas."""
    distances = np.linspace(0, 5000, 500)
    speeds_a = 100 + 200 * np.sin(distances / 500) ** 2
    speeds_b = 95 + 205 * np.sin(distances / 500) ** 2

    mock_tel_a = pd.DataFrame({"Distance": distances, "Speed": speeds_a})
    mock_tel_b = pd.DataFrame({"Distance": distances, "Speed": speeds_b})

    fig, ax = plot_speed_trace_comparison(
        tel_a=mock_tel_a,
        driver_a="RUS",
        year_a=2025,
        tel_b=mock_tel_b,
        driver_b="RUS",
        year_b=2026,
        gp="Australia",
        session_type="Q",
        save=False,
    )
    assert fig is not None
    assert ax is not None
