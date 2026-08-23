"""
Testes de geração de gráficos e vídeos de telemetria.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from f1_analytics_kern.plots.animated_telemetry import render_animated_telemetry_video
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


def test_render_animated_telemetry_video(tmp_path: Path) -> None:
    """Gera um vídeo animado curto (1s, 10fps) a partir de telemetria sintética."""
    distances = np.linspace(0, 5000, 100)
    speeds_a = 100 + 200 * np.sin(distances / 500) ** 2
    speeds_b = 95 + 205 * np.sin(distances / 500) ** 2

    mock_tel_a = pd.DataFrame(
        {
            "Distance": distances,
            "Speed": speeds_a,
            "Throttle": np.full(100, 100.0),
            "Brake": np.zeros(100, dtype=bool),
            "nGear": np.full(100, 7),
            "X": distances * np.cos(distances / 1000),
            "Y": distances * np.sin(distances / 1000),
        }
    )
    mock_tel_b = pd.DataFrame(
        {
            "Distance": distances,
            "Speed": speeds_b,
            "Throttle": np.full(100, 90.0),
            "Brake": np.zeros(100, dtype=bool),
            "nGear": np.full(100, 7),
            "X": distances * np.cos(distances / 1000),
            "Y": distances * np.sin(distances / 1000),
        }
    )

    out_file = "test_anim.mp4"
    video_path = render_animated_telemetry_video(
        tel_a=mock_tel_a,
        driver_a="RUS",
        year_a=2025,
        gp="Australia",
        session_type="Q",
        tel_b=mock_tel_b,
        driver_b="RUS",
        year_b=2026,
        output_filename=out_file,
        fps=10,
        duration_sec=1.0,
        dpi=60,
    )
    assert video_path.exists()
    assert video_path.stat().st_size > 0
    # Limpa o arquivo de teste
    video_path.unlink(missing_ok=True)
