"""
Animação de Telemetria F1 em Vídeo (MP4 Broadcast 60fps).

Renderiza vídeo com:
- Speed trace sendo desenhado dinamicamente curva a curva
- Cores dinâmicas inteligentes (Cores oficiais das equipes ou Eras 2025 vs 2026)
- HUD digital em tempo real (Speed km/h, Throttle %, Brake, Gear, Delta)
- Mini-mapa do circuito com dots dos carros sincronizados
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np

from f1_analytics_kern.config import (
    OUTPUT_DIR,
    PALETTE,
    WATERMARK_TEXT,
)
from f1_analytics_kern.plots.style import apply_vektor_theme

if TYPE_CHECKING:
    from fastf1.core import Session, Telemetry

logger = logging.getLogger(__name__)


def resolve_driver_color(
    driver: str,
    year: int,
    session: Session | None = None,
    default_color: str = "#00F5D4",
) -> str:
    """Resolve a cor oficial do piloto/equipe ou fallback de era."""
    if session is not None:
        try:
            import fastf1.plotting

            color = fastf1.plotting.get_driver_color(driver, session=session)
            if color:
                return color
        except Exception:
            pass

    return default_color


def render_animated_telemetry_video(
    tel_a: Telemetry,
    driver_a: str,
    year_a: int,
    gp: str,
    session_type: str = "Q",
    tel_b: Telemetry | None = None,
    driver_b: str | None = None,
    year_b: int | None = None,
    session: Session | None = None,
    output_filename: str | None = None,
    fps: int = 60,
    duration_sec: float = 12.0,
    figsize: tuple[float, float] = (16, 9),
    dpi: int = 120,
) -> Path:
    """Gera um arquivo de vídeo MP4 com a animação da telemetria e HUD dinâmico."""
    apply_vektor_theme()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    is_comparison = tel_b is not None and driver_b is not None
    if output_filename is None:
        if is_comparison:
            output_filename = f"anim_{driver_a}v{driver_b}_{gp}_{year_a}v{year_b}.mp4"
        else:
            output_filename = f"anim_{driver_a}_{gp}_{year_a}.mp4"

    output_path = OUTPUT_DIR / output_filename

    # ─── Resolução Inteligente de Cores ────────────────────────────────
    if is_comparison:
        if year_a != year_b:
            color_a = PALETTE["era_2025"]
            color_b = PALETTE["era_2026"]
        else:
            color_a = resolve_driver_color(
                driver_a, year_a, session=session, default_color=PALETTE["era_2025"]
            )
            color_b = resolve_driver_color(
                driver_b, year_b or year_a, session=session, default_color=PALETTE["era_2026"]
            )
    else:
        color_a = resolve_driver_color(
            driver_a, year_a, session=session, default_color=PALETTE["era_2026"]
        )
        color_b = PALETTE["era_2026"]

    # ─── Grid Comum de Distância para Sincronização ───────────────────
    total_frames = int(fps * duration_sec)
    max_dist_a = tel_a["Distance"].max()
    max_dist = max_dist_a if not is_comparison else max(max_dist_a, tel_b["Distance"].max())

    dist_grid = np.linspace(0, max_dist, total_frames)

    # Interpolação Piloto A
    speed_a = np.interp(dist_grid, tel_a["Distance"], tel_a["Speed"])
    throttle_a = np.interp(dist_grid, tel_a["Distance"], tel_a["Throttle"])
    brake_a = np.interp(dist_grid, tel_a["Distance"], tel_a["Brake"].astype(float))
    gear_a = np.interp(dist_grid, tel_a["Distance"], tel_a["nGear"]).round().astype(int)
    x_a = np.interp(dist_grid, tel_a["Distance"], tel_a["X"])
    y_a = np.interp(dist_grid, tel_a["Distance"], tel_a["Y"])

    # Interpolação Piloto B (se comparação)
    if is_comparison:
        assert tel_b is not None
        speed_b = np.interp(dist_grid, tel_b["Distance"], tel_b["Speed"])
        throttle_b = np.interp(dist_grid, tel_b["Distance"], tel_b["Throttle"])
        brake_b = np.interp(dist_grid, tel_b["Distance"], tel_b["Brake"].astype(float))
        x_b = np.interp(dist_grid, tel_b["Distance"], tel_b["X"])
        y_b = np.interp(dist_grid, tel_b["Distance"], tel_b["Y"])

    # ─── Configuração do Layout da Figura (GridSpec) ───────────────────
    fig = plt.figure(figsize=figsize, dpi=dpi)
    gs = gridspec.GridSpec(
        nrows=3,
        ncols=3,
        height_ratios=[1.2, 1.0, 0.9],
        width_ratios=[2.2, 1.0, 1.0],
        hspace=0.35,
        wspace=0.30,
        left=0.06,
        right=0.96,
        top=0.92,
        bottom=0.08,
    )

    # 1. Eixo Principal: Speed Trace
    ax_speed = fig.add_subplot(gs[0:2, 0])
    ax_speed.set_xlim(0, max_dist)
    max_speed_val = max(speed_a.max(), speed_b.max() if is_comparison else speed_a.max()) + 20
    min_speed_val = max(
        40, min(speed_a.min(), speed_b.min() if is_comparison else speed_a.min()) - 20
    )
    ax_speed.set_ylim(min_speed_val, max_speed_val)
    ax_speed.set_xlabel("Distância no Circuito (m)", fontsize=11, color=PALETTE["text_secondary"])
    ax_speed.set_ylabel("Velocidade (km/h)", fontsize=11, color=PALETTE["text_secondary"])

    ax_speed.plot(
        dist_grid, speed_a, color=PALETTE["datum_slate"], alpha=0.20, linewidth=1.5, linestyle="--"
    )
    if is_comparison:
        ax_speed.plot(
            dist_grid,
            speed_b,
            color=PALETTE["datum_slate"],
            alpha=0.20,
            linewidth=1.5,
            linestyle=":",
        )

    (line_a,) = ax_speed.plot([], [], color=color_a, linewidth=2.8, label=f"{driver_a} ({year_a})")
    (dot_a,) = ax_speed.plot([], [], marker="o", markersize=8, color=color_a)

    if is_comparison:
        (line_b,) = ax_speed.plot(
            [], [], color=color_b, linewidth=2.8, label=f"{driver_b} ({year_b})"
        )
        (dot_b,) = ax_speed.plot([], [], marker="o", markersize=8, color=color_b)

    ax_speed.legend(loc="upper left", framealpha=0.85)

    # 2. Eixo Inferior: Inputs (Throttle / Brake)
    ax_inputs = fig.add_subplot(gs[2, 0])
    ax_inputs.set_xlim(0, max_dist)
    ax_inputs.set_ylim(-10, 110)
    ax_inputs.set_xlabel("Distância (m)", fontsize=10, color=PALETTE["text_secondary"])
    ax_inputs.set_ylabel("Inputs (%)", fontsize=10, color=PALETTE["text_secondary"])
    (line_throttle_a,) = ax_inputs.plot(
        [], [], color=PALETTE["throttle_green"], linewidth=1.8, label=f"THR {driver_a}"
    )
    (line_brake_a,) = ax_inputs.plot(
        [], [], color=PALETTE["brake_red"], linewidth=1.8, label=f"BRK {driver_a}"
    )
    if is_comparison:
        (line_throttle_b,) = ax_inputs.plot(
            [],
            [],
            color=PALETTE["throttle_green"],
            linewidth=1.2,
            linestyle="--",
            alpha=0.7,
            label=f"THR {driver_b}",
        )
        (line_brake_b,) = ax_inputs.plot(
            [],
            [],
            color=PALETTE["brake_red"],
            linewidth=1.2,
            linestyle="--",
            alpha=0.7,
            label=f"BRK {driver_b}",
        )
    ax_inputs.legend(loc="upper left", fontsize=8, framealpha=0.85, ncol=2)

    # 3. Mini-Mapa do Circuito
    ax_map = fig.add_subplot(gs[0:2, 1:3])
    ax_map.set_facecolor(PALETTE["bg_card"])
    ax_map.plot(tel_a["X"], tel_a["Y"], color=PALETTE["datum_slate"], alpha=0.45, linewidth=2.5)
    (map_dot_a,) = ax_map.plot([], [], marker="o", markersize=10, color=color_a, label=driver_a)
    if is_comparison:
        (map_dot_b,) = ax_map.plot([], [], marker="o", markersize=10, color=color_b, label=driver_b)
    ax_map.set_xticks([])
    ax_map.set_yticks([])
    ax_map.set_title(
        "TRAÇADO DO CIRCUITO",
        fontsize=11,
        fontweight="bold",
        pad=8,
        color=PALETTE["text_primary"],
    )
    ax_map.axis("equal")

    # 4. HUD Digital
    ax_hud = fig.add_subplot(gs[2, 1:3])
    ax_hud.set_facecolor(PALETTE["bg_card"])
    ax_hud.set_xticks([])
    ax_hud.set_yticks([])
    ax_hud.set_xlim(0, 100)
    ax_hud.set_ylim(0, 100)

    hud_speed_text = ax_hud.text(
        15,
        65,
        "0",
        fontsize=28,
        fontweight="bold",
        color=color_a,
        ha="center",
        va="center",
        family="monospace",
    )
    ax_hud.text(
        15, 30, "KM/H", fontsize=10, color=PALETTE["text_secondary"], ha="center", va="center"
    )

    hud_gear_text = ax_hud.text(
        42,
        65,
        "N",
        fontsize=28,
        fontweight="bold",
        color=PALETTE["cut_gold"],
        ha="center",
        va="center",
        family="monospace",
    )
    ax_hud.text(
        42, 30, "MARCHA", fontsize=10, color=PALETTE["text_secondary"], ha="center", va="center"
    )

    hud_throttle_text = ax_hud.text(
        70,
        75,
        "THR: 0%",
        fontsize=11,
        fontweight="bold",
        color=PALETTE["throttle_green"],
        ha="left",
        va="center",
    )
    hud_brake_text = ax_hud.text(
        70,
        48,
        "BRK: OFF",
        fontsize=11,
        fontweight="bold",
        color=PALETTE["brake_red"],
        ha="left",
        va="center",
    )
    hud_delta_text = ax_hud.text(
        70,
        20,
        "DIST: 0m",
        fontsize=10,
        color=PALETTE["text_secondary"],
        ha="left",
        va="center",
    )

    if is_comparison:
        title_main = f"TELEMETRIA COMPARATIVA — {driver_a} vs {driver_b} | {gp} ({session_type})"
    else:
        title_main = f"TELEMETRIA ONBOARD — {driver_a} | {gp} {year_a} ({session_type})"
    fig.suptitle(title_main, fontsize=15, fontweight="bold", color=PALETTE["text_primary"])
    fig.text(
        0.5,
        0.02,
        WATERMARK_TEXT,
        ha="center",
        fontsize=8,
        color=PALETTE["text_muted"],
        style="italic",
    )

    def init():
        line_a.set_data([], [])
        dot_a.set_data([], [])
        line_throttle_a.set_data([], [])
        line_brake_a.set_data([], [])
        map_dot_a.set_data([], [])
        if is_comparison:
            line_b.set_data([], [])
            dot_b.set_data([], [])
            map_dot_b.set_data([], [])
            line_throttle_b.set_data([], [])
            line_brake_b.set_data([], [])
            return (
                line_a,
                dot_a,
                line_b,
                dot_b,
                line_throttle_a,
                line_brake_a,
                line_throttle_b,
                line_brake_b,
                map_dot_a,
                map_dot_b,
            )
        return (line_a, dot_a, line_throttle_a, line_brake_a, map_dot_a)

    def update(frame: int):
        idx = frame + 1
        curr_dist = dist_grid[:idx]

        line_a.set_data(curr_dist, speed_a[:idx])
        dot_a.set_data([curr_dist[-1]], [speed_a[idx - 1]])

        line_throttle_a.set_data(curr_dist, throttle_a[:idx])
        line_brake_a.set_data(curr_dist, brake_a[:idx] * 100)

        map_dot_a.set_data([x_a[idx - 1]], [y_a[idx - 1]])

        if is_comparison:
            line_b.set_data(curr_dist, speed_b[:idx])
            dot_b.set_data([curr_dist[-1]], [speed_b[idx - 1]])
            map_dot_b.set_data([x_b[idx - 1]], [y_b[idx - 1]])
            line_throttle_b.set_data(curr_dist, throttle_b[:idx])
            line_brake_b.set_data(curr_dist, brake_b[:idx] * 100)

        cur_spd = int(speed_a[idx - 1])
        cur_gear = gear_a[idx - 1]
        cur_thr = int(throttle_a[idx - 1])
        cur_brk = bool(brake_a[idx - 1] > 0.1)

        hud_speed_text.set_text(f"{cur_spd:03d}")
        hud_gear_text.set_text(f"{cur_gear}" if cur_gear > 0 else "N")
        hud_throttle_text.set_text(f"THR: {cur_thr:3d}%")
        hud_brake_text.set_text("BRK: ON" if cur_brk else "BRK: OFF")

        if is_comparison:
            delta_spd = cur_spd - int(speed_b[idx - 1])
            delta_sign = "+" if delta_spd >= 0 else ""
            hud_delta_text.set_text(f"Δ SPD: {delta_sign}{delta_spd} km/h")
        else:
            hud_delta_text.set_text(f"DIST: {int(curr_dist[-1])}m")

        if is_comparison:
            return (
                line_a,
                dot_a,
                line_b,
                dot_b,
                line_throttle_a,
                line_brake_a,
                line_throttle_b,
                line_brake_b,
                map_dot_a,
                map_dot_b,
            )
        return (line_a, dot_a, line_throttle_a, line_brake_a, map_dot_a)

    logger.info(
        "Renderizando animação (%d frames a %d fps, %dx%d)...",
        total_frames,
        fps,
        int(figsize[0] * dpi),
        int(figsize[1] * dpi),
    )
    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=total_frames,
        interval=1000 / fps,
        blit=False,
    )

    writer = animation.FFMpegWriter(
        fps=fps,
        codec="libx264",
        bitrate=8000,
        extra_args=["-pix_fmt", "yuv420p", "-preset", "fast"],
    )

    anim.save(output_path, writer=writer, dpi=dpi)
    plt.close(fig)

    logger.info("✅ Vídeo de telemetria renderizado com sucesso: %s", output_path)
    return output_path
