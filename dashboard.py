import streamlit as st
from nba_api.stats.static import players
from nba_api.stats.endpoints import playercareerstats
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="NBA Dashboard",
    page_icon="🏀",
    layout="wide"
)

# ── Custom CSS ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@400;500;600&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
    background-color: #0a0e1a;
    color: #ffffff;
}

.stApp {
    background: linear-gradient(160deg, #0a0e1a 0%, #0d1b3e 50%, #0a0e1a 100%);
}

/* ── Header ── */
.nba-header {
    text-align: center;
    padding: 2.5rem 1rem 1.5rem;
}

.nba-header h1 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 3.5rem;
    font-weight: 800;
    letter-spacing: 4px;
    text-transform: uppercase;
    background: linear-gradient(90deg, #C9243F, #ffffff, #1D4FBA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.nba-header p {
    color: #8899bb;
    font-size: 1rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

.nba-divider {
    height: 3px;
    background: linear-gradient(90deg, transparent, #C9243F, #1D4FBA, transparent);
    margin: 1rem auto 2rem;
    border-radius: 2px;
}

/* ── Search box ── */
.stTextInput > div > div > input {
    background: #111827 !important;
    border: 2px solid #1D4FBA !important;
    border-radius: 12px !important;
    color: #ffffff !important;
    font-size: 1.1rem !important;
    padding: 0.75rem 1.2rem !important;
    font-family: 'Barlow', sans-serif !important;
    transition: border-color 0.3s;
}

.stTextInput > div > div > input:focus {
    border-color: #C9243F !important;
    box-shadow: 0 0 0 3px rgba(201,36,63,0.2) !important;
}

.stTextInput > div > div > input::placeholder {
    color: #4a5a7a !important;
}

/* ── Player name banner ── */
.player-banner {
    background: linear-gradient(135deg, #1D4FBA 0%, #0d1b3e 60%, #C9243F 100%);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    margin: 1.5rem 0;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 32px rgba(29,79,186,0.3);
}

.player-banner .player-name {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #ffffff;
}

.player-banner .player-sub {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.6);
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-top: 2px;
}

.player-ball {
    font-size: 3rem;
}

/* ── Section titles ── */
.section-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #8899bb;
    margin: 2rem 0 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1D4FBA, transparent);
}

/* ── Stat cards ── */
.stat-card {
    background: linear-gradient(145deg, #111827, #0d1b3e);
    border: 1px solid rgba(29,79,186,0.4);
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
    box-shadow: 0 4px 20px rgba(0,0,0,0.4);
}

.stat-card:hover {
    transform: translateY(-4px);
    border-color: #C9243F;
}

.stat-card .stat-label {
    font-size: 0.75rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #8899bb;
    margin-bottom: 0.5rem;
}

.stat-card .stat-value {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
}

.stat-card .stat-value.red { color: #C9243F; }
.stat-card .stat-value.blue { color: #4d7fff; }
.stat-card .stat-value.gold { color: #f0a500; }
.stat-card .stat-value.green { color: #2ecc71; }

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden;
    border: 1px solid rgba(29,79,186,0.3) !important;
}

/* ── Spinner / alerts ── */
.stAlert {
    border-radius: 12px !important;
    border: none !important;
}

/* ── Hide streamlit branding ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="nba-header">
    <h1>🏀 NBA Stats Dashboard</h1>
    <p>Career Statistics Explorer</p>
</div>
<div class="nba-divider"></div>
""", unsafe_allow_html=True)

# ── Search ───────────────────────────────────────────────────
col_search, col_empty = st.columns([2, 1])
with col_search:
    nom = st.text_input("", placeholder="🔍  Search player — Ex: LeBron James, Stephen Curry...")

if nom:
    with st.spinner("🔍 Searching..."):
        result = players.find_players_by_full_name(nom)

    if not result:
        st.error(f"❌ Player '{nom}' not found. Check the spelling!")
    else:
        player = result[0]

        # ── Player banner ─────────────────────────────────────
        st.markdown(f"""
        <div class="player-banner">
            <div class="player-ball">🏀</div>
            <div>
                <div class="player-name">{player['full_name']}</div>
                <div class="player-sub">NBA · Career Statistics · Per Game</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("⏳ Loading career stats..."):
            career = playercareerstats.PlayerCareerStats(
                player_id=player['id'],
                per_mode36='PerGame'
            )
            df = career.season_totals_regular_season.get_data_frame()

        last = df.iloc[-1]

        # ── Stat cards ────────────────────────────────────────
        st.markdown('<div class="section-title">📊 Last Season</div>', unsafe_allow_html=True)

        c1, c2, c3, c4, c5 = st.columns(5)
        cards = [
            (c1, "Points", f"{last['PTS']:.1f}", "red"),
            (c2, "Rebounds", f"{last['REB']:.1f}", "blue"),
            (c3, "Assists", f"{last['AST']:.1f}", "gold"),
            (c4, "FG%", f"{last['FG_PCT']*100:.1f}%", "green"),
            (c5, "Games", f"{int(last['GP'])}", ""),
        ]
        for col, label, value, color in cards:
            with col:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">{label}</div>
                    <div class="stat-value {color}">{value}</div>
                </div>
                """, unsafe_allow_html=True)

        # ── Chart ─────────────────────────────────────────────
        st.markdown('<div class="section-title">📈 Career Progression</div>', unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(14, 4))
        fig.patch.set_facecolor('#111827')
        ax.set_facecolor('#111827')

        seasons = range(len(df))
        ax.plot(seasons, df['PTS'], marker='o', color='#C9243F', linewidth=2.5, markersize=6, label='Points')
        ax.plot(seasons, df['REB'], marker='s', color='#4d7fff', linewidth=2.5, markersize=6, label='Rebounds')
        ax.plot(seasons, df['AST'], marker='^', color='#f0a500', linewidth=2.5, markersize=6, label='Assists')

        ax.set_xticks(list(seasons))
        ax.set_xticklabels(df['SEASON_ID'], rotation=45, ha='right', color='#8899bb', fontsize=9)
        ax.tick_params(colors='#8899bb')
        ax.yaxis.set_major_locator(ticker.MultipleLocator(5))
        ax.grid(color='#1e2d4a', linestyle='--', linewidth=0.7, alpha=0.7)

        for spine in ax.spines.values():
            spine.set_edgecolor('#1e2d4a')

        ax.legend(facecolor='#0d1b3e', edgecolor='#1D4FBA', labelcolor='white', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)

        # ── Full table ────────────────────────────────────────
        st.markdown('<div class="section-title">📋 All Seasons</div>', unsafe_allow_html=True)

        display_df = df[['SEASON_ID','TEAM_ABBREVIATION','GP','PTS','REB','AST','FG_PCT','FG3_PCT','FT_PCT']].copy()
        display_df['FG_PCT'] = (display_df['FG_PCT'] * 100).round(1).astype(str) + '%'
        display_df['FG3_PCT'] = (display_df['FG3_PCT'] * 100).round(1).astype(str) + '%'
        display_df['FT_PCT'] = (display_df['FT_PCT'] * 100).round(1).astype(str) + '%'
        display_df.columns = ['Season','Team','GP','PTS','REB','AST','FG%','3P%','FT%']

        st.dataframe(display_df, use_container_width=True, hide_index=True)