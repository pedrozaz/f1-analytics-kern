"""
Configurações globais, paleta de cores Broadcast Vektor e constantes de telemetria
"""

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
CACHE_DIR = ROOT_DIR / "data_cache"
OUTPUT_DIR = ROOT_DIR / "output"

CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = {
    # Fundo e estrutura
    "bg_dark": "#0B0E14",  # Grafite profundo
    "bg_card": "#111722",  # Fundo dos cards e caixas de dados
    "grid_subtle": "#18202E",  # Gridlines discretas
    "datum_slate": "#64748B",  # Linha de datum e referências
    # Textos
    "text_primary": "#F8FAFC",  # Texto principal de alto contraste
    "text_secondary": "#94A3B8",  # Rótulos de eixos e subtítulos
    "text_muted": "#475569",  # Rodapés e dados secundários
    # Comparações de ano
    "era_2025": "#FF2A2A",  # Vermelho Rosso Corsa
    "era_2026": "#00F5D4",  # Ciano Elétrico Neon
    # Destaques e alertas
    "cut_gold": "#FFC72C",  # Destaque de deltas e callouts
    "brake_red": "#EF4444",  # Freio ativado
    "throttle_green": "#10B981",  # Acelerador 100%
}

TEAM_COLORS = {
    "Mercedes": "#27F4D2",
    "Ferrari": "#E8002D",
    "Red Bull Racing": "#3671C6",
    "McLaren": "#FF8000",
    "Aston Martin": "#229971",
    "Alpine": "#0093CC",
    "Williams": "#64C4FF",
    "Racing Bulls": "#6692FF",
    "Audi": "#A1A3A1",
    "Haas": "#B6BABD",
}

EXPORT_CONFIG = {
    "dpi": 300,
    "format": "png",
    "figsize_standard": (16, 9),  # 16:9
    "figsize_wide": (18, 8),  # Gráficos estendidos
    "figsize_square": (10, 10),  # Mapas de circuito
}

FONTS = {
    "family_sans": "DejaVu Sans",
    "family_mono": "DejaVu Sans Mono",
    "title_size": 18,
    "subtitle_size": 13,
    "label_size": 11,
    "tick_size": 9,
}

WATERMARK_TEXT = "Dados: FIA via FastF1 | Análise: Assetto Kern"
DISCLAIMER_QUALI = "Sessão de Classificação (Q3) - Combustível baixo, modo de ataque máximo"
DISCLAIMER_TESTS = (
    "Testes de Pré-Temporada ≠ Corrida Real - Cargas de combustível e programas distintos"
)
