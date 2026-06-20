from __future__ import annotations

import os
from datetime import datetime, timezone, timedelta

import streamlit as st
import streamlit.components.v1 as components
from dotenv import load_dotenv

load_dotenv()

# ─── Streamlit page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Copa do Mundo 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [data-testid="stApp"] {
    background: #070b16 !important;
    color: #dde4f0 !important;
    font-family: 'Inter', sans-serif !important;
}

#MainMenu, footer, header { visibility: hidden !important; }

[data-testid="stSidebar"] { background: #0d1529 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #070b16; }
::-webkit-scrollbar-thumb { background: rgba(255,215,0,.25); border-radius: 3px; }

/* ── Hero ── */
.hero { text-align: center; padding: 36px 0 8px; }
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(2rem, 5vw, 3.8rem);
    font-weight: 700;
    background: linear-gradient(120deg, #FFD700 0%, #FF9500 45%, #FFD700 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; line-height: 1.1; margin: 0;
}
.hero-sub {
    letter-spacing: 4px; text-transform: uppercase;
    color: #6a7a9a; font-size: .78rem; margin: 6px 0 4px;
}
.hero-hosts { color: #4a5a78; font-size: .82rem; }
.hero-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,215,0,.3), transparent);
    margin: 20px 0;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,.03);
    border: 1px solid rgba(255,255,255,.06);
    border-radius: 14px; padding: 4px; gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 10px; padding: 8px 22px;
    font-weight: 600; font-size: .88rem;
    color: #5a6a88; background: transparent; border: none;
    font-family: 'Inter', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,rgba(255,215,0,.18),rgba(255,150,0,.12)) !important;
    color: #FFD700 !important;
    border: 1px solid rgba(255,215,0,.25) !important;
}
.stTabs [data-baseweb="tab-panel"] { padding-top: 16px; }

/* ── Metric box ── */
.metric-box {
    background: rgba(255,215,0,.05);
    border: 1px solid rgba(255,215,0,.15);
    border-radius: 14px; padding: 18px 12px; text-align: center;
}
.metric-val {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2.4rem; font-weight: 700; color: #FFD700; line-height: 1;
}
.metric-lbl { font-size: .72rem; color: #5a6a88; margin-top: 4px;
    text-transform: uppercase; letter-spacing: .5px; }

/* ── Match card ── */
.match-card {
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.07);
    border-radius: 14px; padding: 14px 18px; margin: 6px 0;
    transition: all .2s ease;
}
.match-card:hover {
    border-color: rgba(255,215,0,.3);
    background: rgba(255,215,0,.03);
    box-shadow: 0 6px 24px rgba(255,215,0,.07);
}
.match-card.live {
    border-color: rgba(0,255,100,.35) !important;
    background: rgba(0,255,100,.03) !important;
    animation: pulse 2.4s infinite;
}
@keyframes pulse {
    0%,100%{box-shadow:0 0 0 0 rgba(0,255,100,.25)}
    50%{box-shadow:0 0 0 8px rgba(0,255,100,0)}
}
.match-score {
    font-family: 'Rajdhani', sans-serif;
    font-size: 2rem; font-weight: 700; color: #FFD700;
    text-align: center; line-height: 1;
}
.match-vs { font-size: 1rem; color: #3a4a68; text-align: center; }
.team-name { font-size: .88rem; font-weight: 600; color: #c8d4e8; }
.match-meta { font-size: .72rem; color: #4a5a78; }

/* ── Badge ── */
.badge {
    display: inline-block; padding: 2px 10px; border-radius: 20px;
    font-size: .68rem; font-weight: 700; letter-spacing: .5px;
    text-transform: uppercase;
}
.b-live   { background:rgba(0,255,100,.18);  color:#00ff64; border:1px solid rgba(0,255,100,.35); }
.b-fin    { background:rgba(100,100,120,.18); color:#88899a; border:1px solid rgba(100,100,120,.3); }
.b-soon   { background:rgba(80,140,255,.18);  color:#7099ff; border:1px solid rgba(80,140,255,.3); }
.b-group  { background:rgba(0,200,150,.18);   color:#00c896; border:1px solid rgba(0,200,150,.3); }
.b-knock  { background:rgba(255,165,0,.18);   color:#FFA500; border:1px solid rgba(255,165,0,.3); }
.b-final  { background:rgba(255,60,60,.18);   color:#ff6060; border:1px solid rgba(255,60,60,.3); }

/* ── Group card ── */
.group-card {
    background: rgba(255,255,255,.035);
    border: 1px solid rgba(255,215,0,.1);
    border-radius: 16px; padding: 18px; margin-bottom: 16px;
    height: 100%;
}
.group-title {
    font-family: 'Rajdhani', sans-serif; font-size: 1.35rem;
    font-weight: 700; color: #FFD700; margin-bottom: 12px;
}

/* ── Standings table ── */
.std-table { width:100%; border-collapse:collapse; font-size:.8rem; }
.std-table th {
    color: #4a5a78; font-size:.65rem; text-transform:uppercase;
    letter-spacing:.5px; padding:4px 6px;
    border-bottom:1px solid rgba(255,255,255,.05); font-weight:600;
}
.std-table td { padding:7px 6px; border-bottom:1px solid rgba(255,255,255,.04); }
.std-table tr:last-child td { border-bottom:none; }
.std-table tr.q1 td:first-child { border-left:2px solid #00c864; }
.std-table tr.q2 td:first-child { border-left:2px solid #FFA500; }
.std-table tr.q3 td:first-child { border-left:2px solid rgba(255,215,0,.3); }
.std-table tr.out td { opacity:.5; }
.std-flag { width:22px; height:15px; object-fit:cover; border-radius:2px;
    vertical-align:middle; margin-right:6px; }
.std-pts { font-family:'Rajdhani',sans-serif; font-weight:700;
    font-size:.95rem; color:#FFD700; }

/* ── Stats ── */
.stat-row { display:flex; align-items:center; gap:10px; margin:6px 0; }
.stat-lbl { font-size:.72rem; color:#6a7a9a; min-width:130px; text-align:right; }
.stat-bar { flex:1; height:5px; background:rgba(255,255,255,.08); border-radius:3px; overflow:hidden; }
.stat-fill-h { height:100%; background:linear-gradient(90deg,#FFD700,#FF9500); border-radius:3px; float:right; }
.stat-fill-a { height:100%; background:linear-gradient(90deg,#5a9aff,#8a6fff); border-radius:3px; }
.stat-num { font-family:'Rajdhani',sans-serif; font-size:.85rem; font-weight:600;
    color:#dde4f0; min-width:28px; text-align:center; }

/* ── Event timeline ── */
.ev-row { display:flex; align-items:flex-start; gap:10px;
    padding:7px 0; border-bottom:1px solid rgba(255,255,255,.04); }
.ev-row:last-child { border-bottom:none; }
.ev-min { font-family:'Rajdhani',sans-serif; font-weight:700;
    color:#FFD700; min-width:34px; font-size:.85rem; }
.ev-ico { min-width:18px; font-size:.9rem; }
.ev-txt { font-size:.82rem; color:#c8d4e8; }
.ev-sub { font-size:.72rem; color:#5a6a88; }

/* ── Bracket ── */
.bracket-round-title {
    font-family:'Rajdhani',sans-serif; font-size:1.1rem;
    font-weight:700; color:#FFD700; text-align:center;
    padding:8px 0; letter-spacing:1px;
    border-bottom:1px solid rgba(255,215,0,.2); margin-bottom:10px;
}
.bracket-match {
    background:rgba(255,255,255,.04);
    border:1px solid rgba(255,255,255,.08);
    border-radius:10px; padding:10px 12px; margin:6px 0;
}
.bracket-match.winner { border-color:rgba(255,215,0,.3); }
.bracket-match.live { border-color:rgba(0,255,100,.35); }
.bracket-team {
    display:flex; align-items:center; gap:8px;
    padding:3px 0; font-size:.82rem; color:#c8d4e8;
}
.bracket-team.winner { color:#FFD700; font-weight:700; }
.bracket-score {
    font-family:'Rajdhani',sans-serif; font-weight:700;
    font-size:1rem; color:#FFD700; margin-left:auto;
}
.bracket-tbd { color:#4a5a78; font-style:italic; }

/* ── Section header ── */
.sec-hdr {
    font-family:'Rajdhani',sans-serif; font-size:1.4rem;
    font-weight:700; color:#e0e8f8; margin:16px 0 10px;
    display:flex; align-items:center; gap:8px;
}

/* ── H2H ── */
.h2h-bar { display:flex; align-items:center; gap:8px; margin:10px 0; }
.h2h-lbl { font-size:.75rem; color:#6a7a9a; min-width:60px; }
.h2h-track { flex:1; height:8px; background:rgba(255,255,255,.08);
    border-radius:4px; overflow:hidden; }
.h2h-fill { height:100%; background:linear-gradient(90deg,#FFD700,#FF9500); border-radius:4px; }

/* ── Buttons ── */
.stButton > button {
    background:linear-gradient(135deg,#FFD700,#FFA500) !important;
    color:#070b16 !important; border:none !important;
    border-radius:8px !important; font-weight:700 !important;
    font-family:'Inter',sans-serif !important; transition:all .25s !important;
}
.stButton > button:hover {
    transform:translateY(-1px) !important;
    box-shadow:0 6px 22px rgba(255,215,0,.3) !important;
}
.stButton > button[kind="secondary"] {
    background:rgba(255,255,255,.07) !important;
    color:#c8d4e8 !important;
    border:1px solid rgba(255,255,255,.1) !important;
}

/* ── Expander ── */
[data-testid="stExpander"] {
    background:rgba(255,255,255,.03) !important;
    border:1px solid rgba(255,215,0,.12) !important;
    border-radius:12px !important;
}
[data-testid="stExpanderToggleIcon"] { color:#FFD700 !important; }

/* ── Selectbox / Input ── */
.stSelectbox label, .stTextInput label { color:#6a7a9a !important; font-size:.8rem !important; }
[data-testid="stSelectbox"] > div > div {
    background:rgba(255,255,255,.06) !important;
    border:1px solid rgba(255,255,255,.1) !important; border-radius:8px !important;
}

/* ── Info box ── */
.info-box {
    background:rgba(80,140,255,.08); border:1px solid rgba(80,140,255,.2);
    border-radius:12px; padding:16px; margin:12px 0;
}
.info-box code {
    background:rgba(255,215,0,.12); color:#FFD700;
    padding:2px 8px; border-radius:4px; font-size:.82rem;
}

/* ── Flag image ── */
.flag-sm { width:28px; height:19px; object-fit:cover;
    border-radius:3px; box-shadow:0 1px 4px rgba(0,0,0,.4); }
.flag-md { width:42px; height:28px; object-fit:cover;
    border-radius:4px; box-shadow:0 2px 8px rgba(0,0,0,.4); }
.flag-lg { width:64px; height:43px; object-fit:cover;
    border-radius:6px; box-shadow:0 3px 12px rgba(0,0,0,.5); }

.legend-dot { display:inline-block; width:10px; height:10px;
    border-radius:50%; margin-right:6px; vertical-align:middle; }

/* ── Spinner override ── */
.stSpinner > div { border-top-color:#FFD700 !important; }

/* No data */
.no-data { text-align:center; color:#3a4a68; padding:40px 0; font-size:.9rem; }
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# ─── Session state ─────────────────────────────────────────────────────────────
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None
if "detail_tab" not in st.session_state:
    st.session_state.detail_tab = "stats"
if "season" not in st.session_state:
    st.session_state.season = os.getenv("SEASON", "2022")

# ─── Imports (after CSS to avoid white flash) ─────────────────────────────────
from src.api_client import FootballAPI
from src.data_processor import (
    parse_fixtures, parse_standings, parse_statistics, parse_events,
    tournament_summary, fixtures_by_group, build_team_group_map,
    flag_url, flag_emoji, fixture_status, is_group_stage,
    round_label, fixture_datetime, score_str, knockout_round_order,
    KNOCKOUT_ROUNDS,
)

# ─── Helpers ──────────────────────────────────────────────────────────────────

def team_flag(team: dict, w: int = 32, h: int = 22) -> str:
    """Country flag via flagcdn.com — emoji visible behind as permanent fallback."""
    name = team.get("name", "") if isinstance(team, dict) else str(team)
    emoji = flag_emoji(name)
    url = flag_url(name, width=40)
    if url:
        return (
            f'<span style="display:inline-block;position:relative;'
            f'width:{w}px;height:{h}px;vertical-align:middle;'
            f'overflow:hidden;border-radius:3px;flex-shrink:0">'
            f'<span style="position:absolute;inset:0;display:flex;align-items:center;'
            f'justify-content:center;font-size:{h}px;line-height:1">{emoji}</span>'
            f'<img src="{url}" '
            f'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover" '
            f'onerror="this.remove()" loading="lazy" />'
            f'</span>'
        )
    return f'<span style="font-size:{h}px;vertical-align:middle;line-height:1;flex-shrink:0">{emoji}</span>'


def team_logo_img(logo_url: str, size: int = 28) -> str:
    if logo_url:
        return (
            f'<img src="{logo_url}" width="{size}" height="{size}" '
            f'style="object-fit:contain;border-radius:4px;vertical-align:middle;flex-shrink:0" '
            f'onerror="this.style.opacity=\'0\'" />'
        )
    return ""


def format_dt(dt: datetime | None, local_offset_h: int = -3) -> str:
    if not dt:
        return "—"
    local = dt + timedelta(hours=local_offset_h)
    return local.strftime("%d/%m • %H:%M")


def elapsed_label(fix: dict) -> str:
    el = fix.get("fixture", {}).get("status", {}).get("elapsed")
    short = fix.get("fixture", {}).get("status", {}).get("short", "")
    if short == "HT":
        return "INT"
    if el:
        return f"{el}'"
    return ""


def round_badge(rnd: str) -> str:
    rnd_l = rnd.lower()
    if "final" in rnd_l and "3rd" not in rnd_l and "third" not in rnd_l and "place" not in rnd_l:
        return f'<span class="badge b-final">Final</span>'
    if "semi" in rnd_l:
        return f'<span class="badge b-knock">Semifinal</span>'
    if "quarter" in rnd_l:
        return f'<span class="badge b-knock">Quartas</span>'
    if "round of 32" in rnd_l:
        return f'<span class="badge b-knock">Oitavas ½</span>'
    if "round of 16" in rnd_l:
        return f'<span class="badge b-knock">Oitavas</span>'
    if "group" in rnd_l:
        return f'<span class="badge b-group">Fase de Grupos</span>'
    return f'<span class="badge b-group">{rnd}</span>'


EVENT_ICONS = {
    "Goal": "⚽",
    "Penalty": "🎯",
    "Missed Penalty": "❌",
    "Own Goal": "🥅",
    "Yellow Card": "🟨",
    "Red Card": "🟥",
    "Yellow Red Card": "🟧",
    "subst": "🔄",
    "Var": "📺",
}


def event_icon(ev: dict) -> str:
    detail = ev.get("detail", "")
    typ = ev.get("type", "")
    if detail == "Penalty":
        return "🎯"
    if detail == "Missed Penalty":
        return "❌"
    if detail == "Own Goal":
        return "🥅"
    return EVENT_ICONS.get(detail, EVENT_ICONS.get(typ, "•"))


# ─── API ──────────────────────────────────────────────────────────────────────

@st.cache_resource
def get_api(key: str, season: str = "2022") -> FootballAPI:
    api = FootballAPI(key)
    api.season = int(season)
    return api


@st.cache_data(ttl=1800, show_spinner=False)
def load_fixtures(api_key: str, season: str) -> tuple[list, str | None]:
    """Returns (fixtures_list, error_message_or_None)."""
    api = get_api(api_key, season)
    data = api.get_fixtures()
    if not data:
        return [], "Sem resposta da API. Verifique sua conexão."
    errors = data.get("errors", {})
    if errors:
        msg = list(errors.values())[0] if isinstance(errors, dict) else str(errors)
        return [], msg
    return data.get("response", []), None


@st.cache_data(ttl=1800, show_spinner=False)
def load_standings(api_key: str, season: str) -> list:
    api = get_api(api_key, season)
    data = api.get_standings()
    if not data or data.get("errors"):
        return []
    return data.get("response", [])


@st.cache_data(ttl=86400, show_spinner=False)
def load_match_detail(api_key: str, fixture_id: int) -> dict:
    api = get_api(api_key)
    stats_raw = api.get_fixture_statistics(fixture_id)
    events_raw = api.get_fixture_events(fixture_id)
    lin_raw = api.get_fixture_lineups(fixture_id)
    return {
        "stats": stats_raw.get("response", []) if stats_raw else [],
        "events": events_raw.get("response", []) if events_raw else [],
        "lineups": lin_raw.get("response", []) if lin_raw else [],
    }


@st.cache_data(ttl=86400, show_spinner=False)
def load_h2h(api_key: str, t1: int, t2: int) -> list:
    api = get_api(api_key)
    data = api.get_head_to_head(t1, t2)
    return data.get("response", []) if data else []


# ─── UI Components ────────────────────────────────────────────────────────────

def render_hero():
    season = os.getenv("SEASON", "2026")
    if season == "2026":
        title = "⚽ Copa do Mundo 2026"
        hosts = "🇺🇸 Estados Unidos &nbsp;•&nbsp; 🇨🇦 Canadá &nbsp;•&nbsp; 🇲🇽 México"
    elif season == "2022":
        title = "⚽ Copa do Mundo 2022"
        hosts = "🇶🇦 Qatar"
    else:
        title = f"⚽ Copa do Mundo {season}"
        hosts = ""
    st.markdown(f"""
    <div class="hero">
      <div class="hero-sub">FIFA</div>
      <h1 class="hero-title">{title}</h1>
      <div class="hero-hosts">{hosts}</div>
      <div class="hero-divider"></div>
    </div>
    """, unsafe_allow_html=True)


def render_setup_guide():
    st.markdown("""
    <div style="max-width:660px;margin:0 auto;padding:40px 20px">
      <h2 style="font-family:'Rajdhani',sans-serif;color:#FFD700;font-size:1.8rem">
        🔑 Configure sua API Key
      </h2>
      <p style="color:#8a9ab8;line-height:1.7">
        Este app usa a <strong style="color:#dde4f0">API-Football</strong> para buscar dados em tempo real
        da Copa do Mundo 2026. O plano gratuito oferece <strong style="color:#FFD700">100 requests/dia</strong>
        — mais do que suficiente com o cache JSON ativado.
      </p>

      <div class="info-box">
        <p style="margin:0 0 8px;font-weight:600;color:#dde4f0">Passo a passo:</p>
        <ol style="color:#8a9ab8;padding-left:18px;line-height:2">
          <li>Acesse <a href="https://dashboard.api-football.com/register" target="_blank"
              style="color:#FFD700">dashboard.api-football.com/register</a> e crie sua conta gratuita</li>
          <li>Confirme o e-mail e faça login</li>
          <li>Copie sua <strong style="color:#dde4f0">API Key</strong> no dashboard</li>
          <li>Na pasta do projeto, execute:<br>
              <code>cp .env.example .env</code></li>
          <li>Abra o <code>.env</code> e substitua <code>SUA_CHAVE_AQUI</code> pela sua key</li>
          <li>Reinicie o app: <code>streamlit run app.py</code></li>
        </ol>
      </div>

      <p style="color:#4a5a78;font-size:.82rem;margin-top:16px">
        ⚡ Todos os dados ficam em cache local na pasta <code>cache/</code> —
        resultados e estatísticas de jogos finalizados são salvos por 24h,
        placares e classificação por 30 minutos.
      </p>
    </div>
    """, unsafe_allow_html=True)


def render_metric_row(summary: dict):
    cols = st.columns(6)
    items = [
        (summary["teams"],         "Seleções"),
        (summary["total_matches"], "Partidas"),
        (summary["matches_played"],"Realizadas"),
        (summary["live"],          "Ao Vivo"),
        (summary["total_goals"],   "Gols"),
        (f"{summary['avg_goals']:.1f}", "Média/Jogo"),
    ]
    for col, (val, lbl) in zip(cols, items):
        with col:
            st.markdown(f"""
            <div class="metric-box">
              <div class="metric-val">{val}</div>
              <div class="metric-lbl">{lbl}</div>
            </div>""", unsafe_allow_html=True)


def render_match_row(fix: dict, key_prefix: str = "m") -> bool:
    """Render a single match card. Returns True if user clicked for details."""
    status = fixture_status(fix)
    fid = fix.get("fixture", {}).get("id", 0)
    home = fix.get("teams", {}).get("home", {})
    away = fix.get("teams", {}).get("away", {})
    rnd = round_label(fix)
    dt = fixture_datetime(fix)
    venue = fix.get("fixture", {}).get("venue", {}).get("name", "")

    home_name = home.get("name", "—")
    away_name = away.get("name", "—")

    status_badge = {
        "live": f'<span class="badge b-live">● AO VIVO {elapsed_label(fix)}</span>',
        "finished": '<span class="badge b-fin">Encerrado</span>',
        "upcoming": '<span class="badge b-soon">Em breve</span>',
    }[status]

    score = score_str(fix)
    card_cls = "match-card live" if status == "live" else "match-card"

    home_w = home.get("winner", False)
    away_w = away.get("winner", False)
    home_style = "font-weight:700;color:#FFD700" if home_w else ""
    away_style = "font-weight:700;color:#FFD700" if away_w else ""

    date_str = format_dt(dt)
    home_flag = team_flag(home, w=38, h=26)
    away_flag = team_flag(away, w=38, h=26)

    col_main, col_btn = st.columns([11, 1])
    with col_main:
        st.markdown(f"""
        <div class="{card_cls}">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px">
            <div>{round_badge(rnd)}&nbsp;&nbsp;{status_badge}</div>
            <div class="match-meta">📅 {date_str}&nbsp;&nbsp;🏟️ {venue or '—'}</div>
          </div>
          <div style="display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:12px">
            <div style="display:flex;align-items:center;gap:10px;justify-content:flex-end">
              <div class="team-name" style="text-align:right;{home_style}">{home_name}</div>
              {home_flag}
            </div>
            <div class="match-score">{score}</div>
            <div style="display:flex;align-items:center;gap:10px">
              {away_flag}
              <div class="team-name" style="{away_style}">{away_name}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

    with col_btn:
        btn_label = "📊" if status == "finished" else ("🔴" if status == "live" else "🔍")
        btn_help = "Ver estatísticas" if status == "finished" else (
            "Ao vivo" if status == "live" else "Ver times prováveis")
        clicked = st.button(btn_label, key=f"{key_prefix}_{fid}", help=btn_help)
        if clicked:
            if st.session_state.selected_match == fid:
                st.session_state.selected_match = None
            else:
                st.session_state.selected_match = fid
            return True
    return False


def render_statistics_panel(fix: dict, detail: dict):
    status = fixture_status(fix)
    home = fix.get("teams", {}).get("home", {})
    away = fix.get("teams", {}).get("away", {})

    st.markdown("---")
    st.markdown(f"""
    <div class="sec-hdr">
      {team_flag(home, w=36, h=24)}
      {home.get('name','—')}
      <span style="color:#3a4a68;margin:0 8px">vs</span>
      {team_flag(away, w=36, h=24)}
      {away.get('name','—')}
      &nbsp;<span style="font-size:.9rem;color:#6a7a9a">• Detalhes</span>
    </div>
    """, unsafe_allow_html=True)

    col_close, _ = st.columns([1, 9])
    with col_close:
        if st.button("✕ Fechar", key=f"close_{fix['fixture']['id']}", help="Fechar detalhes"):
            st.session_state.selected_match = None
            st.rerun()

    if status == "finished" or status == "live":
        _render_finished_detail(fix, detail)
    else:
        _render_upcoming_detail(fix, detail)

    st.markdown("---")


def _render_finished_detail(fix: dict, detail: dict):
    stats_raw = detail.get("stats", [])
    events_raw = detail.get("events", [])
    lineups_raw = detail.get("lineups", [])

    stats = parse_statistics(stats_raw)
    events = parse_events(events_raw)

    t1, t2, t3 = st.tabs(["📊 Estatísticas", "⚽ Eventos", "📋 Escalações"])

    with t1:
        if not stats:
            st.markdown('<div class="no-data">Estatísticas não disponíveis ainda.</div>',
                        unsafe_allow_html=True)
        else:
            _render_stats_bars(stats, fix)

    with t2:
        if not events:
            st.markdown('<div class="no-data">Eventos não disponíveis.</div>',
                        unsafe_allow_html=True)
        else:
            _render_events_timeline(events, fix)

    with t3:
        if not lineups_raw:
            st.markdown('<div class="no-data">Escalações não disponíveis.</div>',
                        unsafe_allow_html=True)
        else:
            _render_lineups(lineups_raw)


def _render_stats_bars(stats: dict, fix: dict):
    home_s = stats.get("home", {})
    away_s = stats.get("away", {})
    home = fix.get("teams", {}).get("home", {})
    away = fix.get("teams", {}).get("away", {})

    STAT_KEYS = [
        ("Ball Possession",   "Posse de Bola"),
        ("Total Shots",       "Chutes Totais"),
        ("Shots on Goal",     "Chutes no Gol"),
        ("Shots off Goal",    "Chutes Fora"),
        ("Blocked Shots",     "Chutes Bloqueados"),
        ("Corner Kicks",      "Escanteios"),
        ("Fouls",             "Faltas"),
        ("Offsides",          "Impedimentos"),
        ("Yellow Cards",      "Cartões Amarelos"),
        ("Red Cards",         "Cartões Vermelhos"),
        ("Goalkeeper Saves",  "Defesas do Goleiro"),
        ("Total passes",      "Passes Totais"),
        ("Passes accurate",   "Passes Certos"),
        ("Passes %",          "Precisão de Passes"),
    ]

    # Header
    c1, c2, c3 = st.columns([3, 4, 3])
    c1.markdown(
        f'<div style="display:flex;align-items:center;gap:8px;justify-content:flex-end">'
        f'{team_flag(home, w=32, h=22)}'
        f'<strong style="color:#FFD700;font-size:.85rem">{home.get("name","")}</strong>'
        f'</div>',
        unsafe_allow_html=True)
    c2.markdown('<div style="text-align:center;color:#4a5a78;font-size:.72rem">ESTATÍSTICA</div>',
                unsafe_allow_html=True)
    c3.markdown(
        f'<div style="display:flex;align-items:center;gap:8px">'
        f'{team_flag(away, w=32, h=22)}'
        f'<strong style="color:#7099ff;font-size:.85rem">{away.get("name","")}</strong>'
        f'</div>',
        unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    for api_key, label in STAT_KEYS:
        h_val = home_s.get(api_key)
        a_val = away_s.get(api_key)
        if h_val is None and a_val is None:
            continue

        h_str = str(h_val) if h_val is not None else "0"
        a_str = str(a_val) if a_val is not None else "0"

        # compute percentage for bar
        try:
            if "%" in h_str:
                hp = int(h_str.replace("%", "").strip())
                ap = 100 - hp
            else:
                hn = float(h_str.replace("%", "") or 0)
                an = float(a_str.replace("%", "") or 0)
                total = hn + an
                hp = int(hn / total * 100) if total else 50
                ap = 100 - hp
        except Exception:
            hp, ap = 50, 50

        c1, c2, c3 = st.columns([3, 4, 3])
        c1.markdown(
            f'<div style="text-align:right;font-family:Rajdhani,sans-serif;'
            f'font-weight:700;font-size:1rem;color:#FFD700">{h_str}</div>',
            unsafe_allow_html=True)
        c2.markdown(f"""
        <div style="text-align:center;margin-bottom:2px">
          <span style="font-size:.7rem;color:#5a6a88">{label}</span>
        </div>
        <div style="display:flex;gap:3px;height:5px">
          <div style="flex:{hp};background:linear-gradient(90deg,#FFD700,#FF9500);border-radius:3px 0 0 3px"></div>
          <div style="flex:{ap};background:linear-gradient(90deg,#5a9aff,#8a6fff);border-radius:0 3px 3px 0"></div>
        </div>
        """, unsafe_allow_html=True)
        c3.markdown(
            f'<div style="font-family:Rajdhani,sans-serif;font-weight:700;'
            f'font-size:1rem;color:#7099ff">{a_str}</div>',
            unsafe_allow_html=True)


def _render_events_timeline(events: list, fix: dict):
    home = fix.get("teams", {}).get("home", {})
    away = fix.get("teams", {}).get("away", {})
    home_id = home.get("id")

    home_events = [e for e in events if e["team_id"] == home_id]
    away_events = [e for e in events if e["team_id"] != home_id]

    col_h, col_a = st.columns(2)

    def render_side(col, team_events, team):
        with col:
            name = team.get("name", "")
            flag = team_flag(team, w=24, h=17)
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:10px">'
                f'{flag}'
                f'<strong style="font-size:.85rem;color:#c8d4e8">{name}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )
            if not team_events:
                st.markdown('<div class="no-data" style="padding:16px 0">Sem eventos</div>',
                            unsafe_allow_html=True)
                return
            rows = ""
            for ev in team_events:
                ico = event_icon(ev)
                mn = f"{ev['time']}'" if isinstance(ev['time'], int) else str(ev['time'])
                detail = ev.get("detail", "")
                player = ev.get("player", "")
                assist = ev.get("assist", "")
                sub_txt = f'<div class="ev-sub">↳ {assist}</div>' if assist else ""
                # sem indentação: 4+ espaços viram code block no markdown do Streamlit
                rows += (
                    f'<div class="ev-row">'
                    f'<div class="ev-min">{mn}</div>'
                    f'<div class="ev-ico">{ico}</div>'
                    f'<div>'
                    f'<div class="ev-txt">{player}</div>'
                    f'{sub_txt}'
                    f'<div class="ev-sub">{detail}</div>'
                    f'</div>'
                    f'</div>'
                )
            st.markdown(rows, unsafe_allow_html=True)

    render_side(col_h, home_events, home)
    render_side(col_a, away_events, away)


def _render_lineups(lineups_raw: list):
    if len(lineups_raw) < 2:
        st.info("Escalações não disponíveis.")
        return

    def side_html(lineup_data: dict) -> str:
        team = lineup_data.get("team", {})
        formation = lineup_data.get("formation", "")
        coach = lineup_data.get("coach", {}).get("name", "—")
        starters = lineup_data.get("startXI", [])
        subs = lineup_data.get("substitutes", [])

        players_html = "".join(
            f'<div style="padding:3px 0;border-bottom:1px solid rgba(255,255,255,.04)">'
            f'<span style="color:#4a5a78;margin-right:8px;font-size:.75rem">'
            f'{p.get("player",{}).get("number","")}</span>'
            f'<span style="font-size:.82rem;color:#c8d4e8">{p.get("player",{}).get("name","—")}</span>'
            f'</div>'
            for p in starters
        )
        subs_html = "".join(
            f'<div style="padding:3px 0;opacity:.6">'
            f'<span style="color:#4a5a78;margin-right:8px;font-size:.75rem">'
            f'{p.get("player",{}).get("number","")}</span>'
            f'<span style="font-size:.78rem;color:#8a9ab8">{p.get("player",{}).get("name","—")}</span>'
            f'</div>'
            for p in subs[:6]
        )
        return f"""
        <div style="background:rgba(255,255,255,.03);border-radius:10px;padding:14px">
          <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px">
            {team_logo_img(team.get('logo',''), 26)}
            <strong style="color:#dde4f0">{team.get('name','')}</strong>
            <span style="color:#4a5a78;margin-left:auto;font-size:.78rem">
              {formation} &nbsp;•&nbsp; 🧑‍💼 {coach}
            </span>
          </div>
          <div style="font-size:.68rem;color:#4a5a78;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:6px">Titulares</div>
          {players_html}
          <div style="font-size:.68rem;color:#4a5a78;text-transform:uppercase;
              letter-spacing:.5px;margin:10px 0 6px">Banco</div>
          {subs_html}
        </div>"""

    col1, col2 = st.columns(2)
    col1.markdown(side_html(lineups_raw[0]), unsafe_allow_html=True)
    col2.markdown(side_html(lineups_raw[1]), unsafe_allow_html=True)


def _render_upcoming_detail(fix: dict, detail: dict):
    home = fix.get("teams", {}).get("home", {})
    away = fix.get("teams", {}).get("away", {})
    dt = fixture_datetime(fix)

    # Countdown
    if dt:
        now = datetime.now(tz=timezone.utc)
        diff = dt - now
        if diff.total_seconds() > 0:
            days = diff.days
            hours = diff.seconds // 3600
            mins = (diff.seconds % 3600) // 60
            countdown = f"{days}d {hours}h {mins}m"
        else:
            countdown = "Em breve"
        st.markdown(f"""
        <div style="text-align:center;padding:20px 0">
          <div style="font-size:.75rem;color:#6a7a9a;text-transform:uppercase;
              letter-spacing:2px;margin-bottom:8px">Começa em</div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:2.5rem;
              font-weight:700;color:#FFD700">{countdown}</div>
          <div style="color:#5a6a78;font-size:.82rem;margin-top:4px">{format_dt(dt)}</div>
        </div>""", unsafe_allow_html=True)

    # Teams (TBD handled)
    home_name = home.get("name")
    away_name = away.get("name")

    col1, col2, col3 = st.columns([5, 2, 5])
    with col1:
        if home_name:
            st.markdown(f"""
            <div style="text-align:center">
              {team_logo_img(home.get('logo',''), 64)}
              <div style="font-size:1rem;font-weight:700;color:#dde4f0;margin-top:8px">
                {home_name}
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;color:#4a5a78;font-size:1.5rem">❓ A definir</div>',
                        unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="text-align:center;font-size:1.5rem;color:#3a4a68;padding-top:20px">vs</div>',
                    unsafe_allow_html=True)
    with col3:
        if away_name:
            st.markdown(f"""
            <div style="text-align:center">
              {team_logo_img(away.get('logo',''), 64)}
              <div style="font-size:1rem;font-weight:700;color:#dde4f0;margin-top:8px">
                {away_name}
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center;color:#4a5a78;font-size:1.5rem">❓ A definir</div>',
                        unsafe_allow_html=True)

    # H2H if both teams known
    if home_name and away_name and home.get("id") and away.get("id"):
        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        with st.expander("📈 Histórico de confrontos (H2H)", expanded=False):
            h2h_fixtures = detail.get("h2h", [])
            if not h2h_fixtures:
                st.markdown('<div class="no-data">Sem histórico disponível.</div>',
                            unsafe_allow_html=True)
            else:
                home_wins = sum(1 for f in h2h_fixtures
                                if f.get("teams", {}).get("home", {}).get("id") == home["id"]
                                and f.get("teams", {}).get("home", {}).get("winner"))
                away_wins = sum(1 for f in h2h_fixtures
                                if f.get("teams", {}).get("away", {}).get("id") == away["id"]
                                and f.get("teams", {}).get("away", {}).get("winner"))
                draws = len(h2h_fixtures) - home_wins - away_wins
                total = len(h2h_fixtures)
                hp = int(home_wins / total * 100) if total else 33
                dp = int(draws / total * 100) if total else 34
                ap = 100 - hp - dp

                st.markdown(f"""
                <div style="display:flex;justify-content:space-around;margin:12px 0">
                  <div style="text-align:center">
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;
                        font-weight:700;color:#FFD700">{home_wins}</div>
                    <div style="font-size:.7rem;color:#5a6a88">{home_name[:12]}</div>
                  </div>
                  <div style="text-align:center">
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;
                        font-weight:700;color:#6a7a9a">{draws}</div>
                    <div style="font-size:.7rem;color:#5a6a88">Empates</div>
                  </div>
                  <div style="text-align:center">
                    <div style="font-family:'Rajdhani',sans-serif;font-size:1.8rem;
                        font-weight:700;color:#7099ff">{away_wins}</div>
                    <div style="font-size:.7rem;color:#5a6a88">{away_name[:12]}</div>
                  </div>
                </div>
                <div style="display:flex;gap:2px;height:6px;border-radius:4px;overflow:hidden">
                  <div style="flex:{hp};background:linear-gradient(90deg,#FFD700,#FF9500)"></div>
                  <div style="flex:{dp};background:rgba(255,255,255,.15)"></div>
                  <div style="flex:{ap};background:linear-gradient(90deg,#5a9aff,#8a6fff)"></div>
                </div>
                """, unsafe_allow_html=True)

                for hf in h2h_fixtures[:5]:
                    render_match_row(hf, key_prefix="h2h")


def render_standings_table(group_name: str, teams: list):
    rows_html = ""
    for i, t in enumerate(teams):
        rank = t.get("rank", i + 1)
        team_info = t.get("team", {})
        t_name = team_info.get("name", "—")
        t_logo = team_info.get("logo", "")
        stats = t.get("all", {})
        pts = t.get("points", 0)
        played = stats.get("played", 0)
        w = stats.get("win", 0)
        d = stats.get("draw", 0)
        l = stats.get("lose", 0)
        gf = stats.get("goals", {}).get("for", 0)
        ga = stats.get("goals", {}).get("against", 0)
        gd = t.get("goalsDiff", 0)
        gd_str = f"+{gd}" if gd > 0 else str(gd)

        # row class based on qualification
        desc = t.get("description", "") or ""
        if rank <= 2 or "Qualified" in desc or "Champions" in desc:
            tr_cls = "q1"
        elif rank == 3:
            tr_cls = "q2"
        else:
            tr_cls = "out"

        logo_html = team_flag(team_info, w=26, h=18)

        rows_html += f"""
        <tr class="{tr_cls}">
          <td style="color:#5a6a88;font-size:.75rem;padding-left:8px">{rank}</td>
          <td style="white-space:nowrap"><span style="margin-right:7px">{logo_html}</span><span style="font-size:.82rem;color:#c8d4e8">{t_name}</span></td>
          <td style="color:#7a8aaa">{played}</td>
          <td style="color:#7a8aaa">{w}</td>
          <td style="color:#7a8aaa">{d}</td>
          <td style="color:#7a8aaa">{l}</td>
          <td style="color:#7a8aaa">{gf}:{ga}</td>
          <td style="color:#6a8a6a">{gd_str}</td>
          <td><span class="std-pts">{pts}</span></td>
        </tr>"""

    st.markdown(f"""
    <table class="std-table">
      <thead>
        <tr>
          <th>#</th><th>Seleção</th><th>J</th><th>V</th>
          <th>E</th><th>D</th><th>GP:GC</th><th>SG</th><th>Pts</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    <div style="margin-top:8px;display:flex;gap:16px">
      <div><span class="legend-dot" style="background:#00c864"></span><span style="font-size:.68rem;color:#5a6a88">Classificados</span></div>
      <div><span class="legend-dot" style="background:#FFA500"></span><span style="font-size:.68rem;color:#5a6a88">Possível vaga</span></div>
    </div>
    """, unsafe_allow_html=True)


def render_bracket_round(round_name: str, fixtures: list, key_prefix: str):
    st.markdown(f'<div class="bracket-round-title">{round_name}</div>', unsafe_allow_html=True)
    for fix in fixtures:
        fid = fix.get("fixture", {}).get("id", 0)
        home = fix.get("teams", {}).get("home", {})
        away = fix.get("teams", {}).get("away", {})
        status = fixture_status(fix)
        g = fix.get("goals", {})
        hg = g.get("home")
        ag = g.get("away")

        h_win = home.get("winner", False)
        a_win = away.get("winner", False)

        cls = "bracket-match"
        if status == "live":
            cls += " live"
        elif h_win or a_win:
            cls += " winner"

        def team_row(team_info, goals, is_winner):
            flag = team_flag(team_info, w=22, h=15) if team_info.get("name") else ""
            name = team_info.get("name", "A definir")
            name_cls = "bracket-team winner" if is_winner else "bracket-team"
            if not team_info.get("name"):
                name_cls += " bracket-tbd"
            score = f'<span class="bracket-score">{goals if goals is not None else ""}</span>'
            return f'<div class="{name_cls}">{flag} {name}{score}</div>'

        st.markdown(f"""
        <div class="{cls}">
          {team_row(home, hg, h_win)}
          <div style="height:1px;background:rgba(255,255,255,.05);margin:4px 0"></div>
          {team_row(away, ag, a_win)}
        </div>""", unsafe_allow_html=True)

        col_btn, _ = st.columns([1, 8])
        with col_btn:
            btn = "📊" if status == "finished" else ("🔴" if status == "live" else "🔍")
            if st.button(btn, key=f"{key_prefix}_b_{fid}", help="Ver detalhes"):
                st.session_state.selected_match = fid if st.session_state.selected_match != fid else None
                st.rerun()


# ─── Tabs ─────────────────────────────────────────────────────────────────────

def tab_overview(parsed: dict, summary: dict):
    render_metric_row(summary)

    # Live matches
    if parsed["live"]:
        st.markdown('<div class="sec-hdr">🔴 Ao Vivo</div>', unsafe_allow_html=True)
        for fix in parsed["live"]:
            render_match_row(fix, "ov_live")

    # Today's matches
    now_utc = datetime.now(tz=timezone.utc)
    today_matches = [
        f for f in parsed["all"]
        if fixture_datetime(f) and
        fixture_datetime(f).date() == now_utc.date() and
        fixture_status(f) != "live"
    ]
    if today_matches:
        st.markdown('<div class="sec-hdr">📅 Hoje</div>', unsafe_allow_html=True)
        for fix in today_matches:
            render_match_row(fix, "ov_today")

    # Upcoming (next 5)
    upcoming = parsed["upcoming"][:5]
    if upcoming:
        st.markdown('<div class="sec-hdr">🗓️ Próximas Partidas</div>', unsafe_allow_html=True)
        for fix in upcoming:
            render_match_row(fix, "ov_next")

    # Recent results (last 5)
    recent = parsed["finished"][:5]
    if recent:
        st.markdown('<div class="sec-hdr">🏁 Resultados Recentes</div>', unsafe_allow_html=True)
        for fix in recent:
            render_match_row(fix, "ov_rec")

    if not parsed["all"]:
        st.markdown('<div class="no-data">Nenhuma partida encontrada. Verifique sua API key e o League ID.</div>',
                    unsafe_allow_html=True)


def tab_groups(parsed: dict, standings_by_group: dict, team_group_map: dict):
    by_grp = fixtures_by_group(parsed["all"], team_group_map)
    sorted_groups = sorted(standings_by_group.keys())

    if not sorted_groups:
        st.markdown('<div class="no-data">Classificação não disponível ainda.</div>',
                    unsafe_allow_html=True)
        return

    for i in range(0, len(sorted_groups), 3):
        row_groups = sorted_groups[i:i + 3]
        cols = st.columns(len(row_groups))
        for col, grp_name in zip(cols, row_groups):
            with col:
                st.markdown(f'<div class="group-card"><div class="group-title">{grp_name}</div>',
                            unsafe_allow_html=True)
                render_standings_table(grp_name, standings_by_group[grp_name])
                st.markdown("</div>", unsafe_allow_html=True)

                # Group matches
                grp_fixtures = by_grp.get(grp_name, [])
                if grp_fixtures:
                    with st.expander(f"Ver partidas ({len(grp_fixtures)})", expanded=False):
                        for fix in grp_fixtures:
                            render_match_row(fix, f"grp_{grp_name.replace(' ','')}")


def tab_knockout(parsed: dict):
    ko_rounds = parsed["by_round_knockout"]
    if not ko_rounds:
        st.markdown("""
        <div style="text-align:center;padding:60px 0">
          <div style="font-size:3rem;margin-bottom:12px">🏆</div>
          <div style="font-family:'Rajdhani',sans-serif;font-size:1.4rem;color:#5a6a88">
            Fase eliminatória ainda não iniciada
          </div>
          <div style="font-size:.85rem;color:#3a4a58;margin-top:8px">
            Os confrontos serão definidos ao final da fase de grupos
          </div>
        </div>""", unsafe_allow_html=True)
        return

    sorted_rounds = sorted(ko_rounds.keys(), key=knockout_round_order)

    for rnd in sorted_rounds:
        fixtures = ko_rounds[rnd]
        fixtures.sort(key=lambda x: x.get("fixture", {}).get("timestamp", 0))
        with st.expander(f"🏆 {rnd} ({len(fixtures)} jogos)", expanded=True):
            render_bracket_round(rnd, fixtures, f"ko_{rnd.replace(' ','_')}")


def tab_matches(parsed: dict, api_key: str):
    all_rounds = sorted(
        set(round_label(f) for f in parsed["all"]),
        key=lambda r: (0 if "Group" in r else 1, r)
    )

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        filter_status = st.selectbox(
            "Status",
            ["Todos", "Realizados", "Ao Vivo", "Próximos"],
            key="filter_status"
        )
    with col_f2:
        filter_round = st.selectbox(
            "Fase / Rodada",
            ["Todas"] + all_rounds,
            key="filter_round"
        )
    with col_f3:
        search_team = st.text_input("Buscar time", placeholder="Ex: Brasil", key="search_team")

    filtered = parsed["all"]
    if filter_status == "Realizados":
        filtered = [f for f in filtered if fixture_status(f) == "finished"]
    elif filter_status == "Ao Vivo":
        filtered = [f for f in filtered if fixture_status(f) == "live"]
    elif filter_status == "Próximos":
        filtered = [f for f in filtered if fixture_status(f) == "upcoming"]

    if filter_round != "Todas":
        filtered = [f for f in filtered if round_label(f) == filter_round]

    if search_team:
        q = search_team.lower()
        filtered = [
            f for f in filtered
            if q in f.get("teams", {}).get("home", {}).get("name", "").lower() or
               q in f.get("teams", {}).get("away", {}).get("name", "").lower()
        ]

    filtered.sort(key=lambda x: x.get("fixture", {}).get("timestamp", 0))

    st.markdown(f'<div style="color:#5a6a88;font-size:.8rem;margin-bottom:12px">'
                f'{len(filtered)} partida(s) encontradas</div>', unsafe_allow_html=True)

    for fix in filtered:
        render_match_row(fix, "all")


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    render_hero()

    api_key = os.getenv("API_FOOTBALL_KEY", "").strip()
    if not api_key or api_key == "SUA_CHAVE_AQUI":
        render_setup_guide()
        return

    season = st.session_state.season

    # Sidebar: temporada + cache + API info
    with st.sidebar:
        st.markdown("## ⚙️ Configurações")

        # ── Season switcher ──────────────────────────────────────────────────
        st.markdown(
            '<div style="font-size:.8rem;color:#6a7a9a;margin-bottom:6px">'
            '⚽ <strong style="color:#dde4f0">Temporada</strong></div>',
            unsafe_allow_html=True,
        )
        col_22, col_26 = st.columns(2)
        with col_22:
            active_22 = season == "2022"
            if st.button(
                "2022 🇶🇦",
                key="btn_season_2022",
                type="primary" if active_22 else "secondary",
                use_container_width=True,
            ):
                if not active_22:
                    st.session_state.season = "2022"
                    st.session_state.selected_match = None
                    st.cache_data.clear()
                    st.rerun()
        with col_26:
            active_26 = season == "2026"
            if st.button(
                "2026 🌎",
                key="btn_season_2026",
                type="primary" if active_26 else "secondary",
                use_container_width=True,
            ):
                if not active_26:
                    st.session_state.season = "2026"
                    st.session_state.selected_match = None
                    st.cache_data.clear()
                    st.rerun()

        if season == "2026":
            st.markdown(
                '<div style="font-size:.72rem;color:#cc6644;margin-top:4px">'
                '⚠️ Requer plano pago na API-Football</div>',
                unsafe_allow_html=True,
            )

        st.markdown("---")
        api = get_api(api_key, season)
        cache_info = api.cache.cache_info()
        st.markdown(f"""
        <div style="font-size:.8rem;color:#6a7a9a">
          Cache: <strong style="color:#dde4f0">{cache_info['valid']}</strong>
          arquivos válidos de {cache_info['total']} total
        </div>""", unsafe_allow_html=True)

        if st.button("🗑️ Limpar Cache", help="Force atualização dos dados da API"):
            api.cache.clear_all()
            st.cache_data.clear()
            st.success("Cache limpo!")
            st.rerun()

        st.markdown("---")
        status_data = api.get_status()
        if status_data and status_data.get("response"):
            acc = status_data["response"].get("account", {})
            req = status_data["response"].get("requests", {})
            limit_day = req.get("limit_day", 100)
            used = req.get("current", 0)
            st.markdown(f"""
            <div style="font-size:.8rem;color:#6a7a9a">
              <div style="margin-bottom:6px">
                <strong style="color:#dde4f0">{acc.get('firstname','')} {acc.get('lastname','')}</strong>
              </div>
              Plano: <strong style="color:#FFD700">{acc.get('plan','Free')}</strong><br>
              Requests hoje: <strong style="color:#dde4f0">{used}</strong> / {limit_day}
            </div>""", unsafe_allow_html=True)
            pct = int(used / limit_day * 100) if limit_day else 0
            st.progress(min(pct, 100) / 100)

        st.markdown("---")
        league_id = os.getenv("LEAGUE_ID", "1")
        st.markdown(f"""
        <div style="font-size:.75rem;color:#4a5a78">
          League ID: <code style="color:#FFD700">{league_id}</code><br>
          Temporada: <code style="color:#FFD700">{season}</code>
        </div>""", unsafe_allow_html=True)

    # Load data
    with st.spinner(f"Carregando dados da Copa {season}..."):
        raw_fixtures, api_error = load_fixtures(api_key, season)
        raw_standings = load_standings(api_key, season)

    # Surface plan/API errors prominently
    if api_error:
        is_plan_error = "plan" in api_error.lower() or "free" in api_error.lower()
        
        # Mover HTML complexo para fora da f-string
        plan_restriction_html = '<div style="margin-top:10px;font-size:.82rem;color:#8a7a7a">O plano gratuito da API-Football permite acesso às temporadas <strong style="color:#FFD700">2022-2024</strong> apenas.<br>Para acessar a Copa 2026, você precisa de um plano pago em <a href="https://dashboard.api-football.com" target="_blank" style="color:#FFD700">dashboard.api-football.com</a>.<br><br>Para demonstrar o app funcionando, altere <code style="background:rgba(255,215,0,.15);color:#FFD700;padding:1px 6px;border-radius:3px">SEASON=2022</code> no arquivo <code style="background:rgba(255,215,0,.15);color:#FFD700;padding:1px 6px;border-radius:3px">.env</code> para usar os dados da Copa do Qatar.</div>'
        
        st.markdown(f"""
        <div style="background:rgba(255,80,80,.08);border:1px solid rgba(255,80,80,.25);
            border-radius:12px;padding:18px 20px;margin:0 0 20px">
        <div style="font-weight:700;color:#ff8080;margin-bottom:6px">
            {'⚠️ Restrição de Plano' if is_plan_error else '❌ Erro na API'}
        </div>
        <div style="color:#cc6666;font-size:.88rem;line-height:1.6">{api_error}</div>
        {plan_restriction_html if is_plan_error else ''}
        </div>
        """, unsafe_allow_html=True)
        if not raw_fixtures:
            return

    parsed = parse_fixtures(raw_fixtures)
    standings_by_group = parse_standings(raw_standings)
    team_group_map = build_team_group_map(standings_by_group)
    summary = tournament_summary(raw_fixtures)

    # Main tabs
    season_label = f"Copa {season}"
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Início",
        "⚽ Grupos",
        "⚡ Eliminatórias",
        "📋 Todas as Partidas",
    ])

    with tab1:
        tab_overview(parsed, summary)

    with tab2:
        tab_groups(parsed, standings_by_group, team_group_map)

    with tab3:
        tab_knockout(parsed)

    with tab4:
        tab_matches(parsed, api_key)

    # ── Match detail panel (shown when any match is selected) ────────────────
    selected_id = st.session_state.selected_match
    if selected_id:
        fix_map = {f.get("fixture", {}).get("id"): f for f in raw_fixtures}
        selected_fix = fix_map.get(selected_id)
        if selected_fix:
            status = fixture_status(selected_fix)
            home_id = selected_fix.get("teams", {}).get("home", {}).get("id")
            away_id = selected_fix.get("teams", {}).get("away", {}).get("id")

            if status in ("finished", "live"):
                with st.spinner("Carregando estatísticas..."):
                    detail = load_match_detail(api_key, selected_id)
            else:
                h2h = []
                if home_id and away_id:
                    with st.spinner("Carregando histórico..."):
                        h2h = load_h2h(api_key, home_id, away_id)
                detail = {"stats": [], "events": [], "lineups": [], "h2h": h2h}

            # Anchor para scroll automático
            st.markdown('<div id="copa-stats-anchor"></div>', unsafe_allow_html=True)
            render_statistics_panel(selected_fix, detail)

            # Scroll até as estatísticas
            components.html(
                """<script>
                (function() {
                  var el = window.parent.document.getElementById('copa-stats-anchor');
                  if (el) el.scrollIntoView({behavior: 'smooth', block: 'start'});
                })();
                </script>""",
                height=0,
            )


if __name__ == "__main__":
    main()
