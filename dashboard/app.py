"""
list Contributor Funnel Dashboard
"""

import streamlit as st
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

# ─── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("lauraarakakii/onboarding-flow/main/dashboard/cohort_retention.csv")
    with open("lauraarakakii/onboarding-flow/main/dashboard/funnel_summary.json") as f:
        funnel = json.load(f)
    return df, funnel

df, funnel = load_data()

list_name = funnel.get("list", "unknown-list")
short_list_name = list_name.split(".")[-1]

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=f"{short_list_name} · Contributor Funnel",
    page_icon="🐧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Sora:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* Dark sidebar */
section[data-testid="stSidebar"] {
    background: #0d1117 !important;
    border-right: 1px solid #21262d;
}
section[data-testid="stSidebar"] * {
    color: #e6edf3 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-size: 0.95rem;
    padding: 6px 0;
    letter-spacing: 0.01em;
}

/* Main background */
.main .block-container {
    background: #0d1117;
    padding-top: 2rem;
    padding-bottom: 4rem;
    max-width: 1280px;
}

/* Headers */
h1, h2, h3 {
    font-family: 'Sora', sans-serif !important;
    color: #e6edf3 !important;
}

/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #30363d;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    border-radius: 4px 0 0 4px;
}
.metric-card.teal::before { background: #2dd4bf; }
.metric-card.blue::before { background: #60a5fa; }
.metric-card.amber::before { background: #fbbf24; }
.metric-card.rose::before  { background: #f87171; }

.metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #8b949e !important;
    margin-bottom: 0.4rem;
}
.metric-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2.2rem;
    font-weight: 700;
    color: #e6edf3;
    line-height: 1;
}
.metric-sub {
    font-size: 0.78rem;
    color: #8b949e;
    margin-top: 0.4rem;
}

/* Section titles */
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #e6edf3;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    border-bottom: 1px solid #21262d;
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
    margin-top: 1.8rem;
}

/* Insight boxes */
.insight-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-left: 4px solid #2dd4bf;
    border-radius: 0 10px 10px 0;
    padding: 1rem 1.2rem;
    margin: 0.6rem 0;
    font-size: 0.9rem;
    color: #c9d1d9;
    line-height: 1.6;
}
.insight-box strong { color: #2dd4bf; }

/* Glossary */
.gloss-term {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.8rem;
}
.gloss-term h4 {
    font-family: 'JetBrains Mono', monospace;
    color: #60a5fa !important;
    margin: 0 0 0.4rem 0;
    font-size: 1rem;
}
.gloss-term p {
    color: #8b949e;
    font-size: 0.88rem;
    margin: 0;
    line-height: 1.6;
}

/* Page header */
.page-header {
    background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
    border: 1px solid #21262d;
    border-radius: 16px;
    padding: 2rem 2.4rem;
    margin-bottom: 2rem;
}
.page-header h1 {
    font-size: 1.8rem;
    font-weight: 800;
    margin: 0 0 0.3rem 0;
    background: linear-gradient(90deg, #2dd4bf, #60a5fa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.page-header p {
    color: #8b949e;
    font-size: 0.9rem;
    margin: 0;
}

/* Chart container */
.chart-wrap {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 14px;
    padding: 0.5rem;
    margin-bottom: 1.2rem;
}

/* Override streamlit defaults */
div[data-testid="stMarkdownContainer"] p { color: #c9d1d9; }
div[data-testid="stMarkdownContainer"] li { color: #c9d1d9; }
.stSelectbox label, .stMultiSelect label { color: #8b949e !important; font-size: 0.82rem !important; }
</style>
""", unsafe_allow_html=True)



# Plotly dark template
TEAL    = "#2dd4bf"
BLUE    = "#60a5fa"
AMBER   = "#fbbf24"
ROSE    = "#f87171"
VIOLET  = "#a78bfa"
GREEN   = "#4ade80"
PALETTE = [TEAL, BLUE, AMBER, ROSE, VIOLET, GREEN]

CHART_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Sora, sans-serif", color="#c9d1d9"),
    margin=dict(l=10, r=10, t=40, b=10),
    xaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickcolor="#30363d"),
    yaxis=dict(gridcolor="#21262d", linecolor="#30363d", tickcolor="#30363d"),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor="#30363d"),
)

# ─── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"### 🐧 **{short_list_name} · LKML5Ws**")
    st.markdown("<hr style='border-color:#21262d;margin:0.6rem 0'>", unsafe_allow_html=True)

    page = st.radio(
        "Navegação",
        ["📊 Visão Geral", "🔬 Análise de Coorte", "🚰 Funil de Contribuição", "📖 Glossário"],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#21262d;margin:0.8rem 0'>", unsafe_allow_html=True)
    st.markdown("**Filtrar por Ano**")

    years = sorted(df["entry_year"].unique())
    year_range = st.select_slider(
        "Período de análise",
        options=years,
        value=(years[0], years[-1]),
        label_visibility="collapsed",
    )

    df_filt = df[(df["entry_year"] >= year_range[0]) & (df["entry_year"] <= year_range[1])].copy()

    st.markdown("<hr style='border-color:#21262d;margin:0.8rem 0'>", unsafe_allow_html=True)
    st.caption(f"**{len(df_filt)} coortes** · {year_range[0]}–{year_range[1]}")
    st.caption(f"Lista `{list_name}` · Linux Kernel")
    st.caption("Dados extraídos via `lore.kernel.org`")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — VISÃO GERAL
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Visão Geral":

    st.markdown(f"""
    <div class="page-header">
      <h1>Visão Geral do Funil de Contribuição</h1>
      <p>Lista <strong>{list_name}</strong> do Linux Kernel · 2004–2024 </p>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI Cards ──────────────────────────────────────────────────────────────
    total_contributors = df_filt["cohort_size"].sum()
    total_patchers     = df_filt["n_patched"].sum()
    total_reviewed     = df_filt["n_reviewed"].sum()
    total_ret6         = df_filt["n_retained_6m"].sum()
    total_ret12        = df_filt["n_retained_12m"].sum()

    pct_patch   = total_patchers  / total_contributors * 100
    pct_rev     = total_reviewed  / total_contributors * 100
    pct_r6      = total_ret6      / total_contributors * 100
    pct_r12     = total_ret12     / total_contributors * 100
    mttfp       = funnel["mttfp_days"]
    rev_conv    = funnel["review_conversion_pct"]

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="metric-card teal">
          <div class="metric-label">Novos Contribuidores</div>
          <div class="metric-value">{total_contributors:,}</div>
          <div class="metric-sub">no período {year_range[0]}–{year_range[1]}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="metric-card blue">
          <div class="metric-label">Enviaram ao Menos 1 Patch</div>
          <div class="metric-value">{total_patchers:,}</div>
          <div class="metric-sub">{pct_patch:.1f}% dos novos contribuidores</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
        <div class="metric-card amber">
          <div class="metric-label">Tempo Médio até 1º Patch</div>
          <div class="metric-value">{mttfp:.0f}d</div>
          <div class="metric-sub">após o primeiro contato com a lista</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    c4, c5, c6 = st.columns(3)
    with c4:
        st.markdown(f"""
        <div class="metric-card blue">
          <div class="metric-label">Receberam Revisão</div>
          <div class="metric-value">{total_reviewed:,}</div>
          <div class="metric-sub">{pct_rev:.1f}% do total · {rev_conv:.1f}% dos que patcharam</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown(f"""
        <div class="metric-card rose">
          <div class="metric-label">Retidos após 6 Meses</div>
          <div class="metric-value">{total_ret6:,}</div>
          <div class="metric-sub">{pct_r6:.1f}% do total de novos</div>
        </div>
        """, unsafe_allow_html=True)
    with c6:
        st.markdown(f"""
        <div class="metric-card rose">
          <div class="metric-label">Retidos após 12 Meses</div>
          <div class="metric-value">{total_ret12:,}</div>
          <div class="metric-sub">{pct_r12:.1f}% do total de novos</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Funnel Overview ────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Funil Consolidado (período selecionado)</div>', unsafe_allow_html=True)

    stages  = ["Novos\nContribuidores", "Enviaram\nPatch", "Receberam\nRevisão", "Retidos\n6 meses", "Retidos\n12 meses"]
    values  = [total_contributors, total_patchers, total_reviewed, total_ret6, total_ret12]
    colors  = [TEAL, BLUE, VIOLET, AMBER, ROSE]

    fig_funnel = go.Figure(go.Funnel(
        y=stages,
        x=values,
        textposition="inside",
        textinfo="value+percent initial",
        marker=dict(color=colors, line=dict(width=1, color="#0d1117")),
        connector=dict(line=dict(color="#30363d", width=1)),
    ))
    fig_funnel.update_layout(**CHART_LAYOUT, height=360,
                             title=dict(text="", x=0.5))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_funnel, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Trend Overview ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Evolução Anual das Taxas de Conversão</div>', unsafe_allow_html=True)

    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=df_filt["entry_year"], y=df_filt["pct_patch"],
        name="% enviou patch", line=dict(color=TEAL, width=2.5), mode="lines+markers",
        marker=dict(size=6)))
    fig_trend.add_trace(go.Scatter(x=df_filt["entry_year"], y=df_filt["pct_review"],
        name="% recebeu revisão", line=dict(color=BLUE, width=2.5, dash="dot"), mode="lines+markers",
        marker=dict(size=6)))
    fig_trend.add_trace(go.Scatter(x=df_filt["entry_year"], y=df_filt["pct_ret_6m"],
        name="% retido 6m", line=dict(color=AMBER, width=2.5), mode="lines+markers",
        marker=dict(size=6)))
    fig_trend.add_trace(go.Scatter(x=df_filt["entry_year"], y=df_filt["pct_ret_12m"],
        name="% retido 12m", line=dict(color=ROSE, width=2.5, dash="dot"), mode="lines+markers",
        marker=dict(size=6)))
    fig_trend.update_layout(**CHART_LAYOUT, height=340,
                            yaxis_title="% do cohort", xaxis_title="Ano de Entrada",
                            hovermode="x unified")
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Key Insights ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Principais Achados</div>', unsafe_allow_html=True)

    best_patch_yr = df_filt.loc[df_filt["pct_patch"].idxmax(), "entry_year"]
    best_patch_pct = df_filt["pct_patch"].max()
    best_rev_yr   = df_filt.loc[df_filt["pct_review"].idxmax(), "entry_year"]
    best_rev_pct  = df_filt["pct_review"].max()

    insights = [
        f"De cada <strong>100 novos contribuidores</strong>, apenas <strong>~{pct_patch:.0f}</strong> chegam a enviar um patch — evidenciando uma barreira de entrada significativa.",
        f"A taxa de revisão ({pct_rev:.1f}%) é muito menor que a taxa de patch ({pct_patch:.0f}%), sugerindo que <strong>a maioria dos patches não recebe feedback</strong> formal na lista.",
        f"O <strong>Tempo Médio até o Primeiro Patch</strong> é de <strong>{mttfp:.0f} dias</strong>, indicando que há um período de observação/aprendizagem antes da primeira contribuição.",
        f"A retenção de 12 meses (<strong>{pct_r12:.1f}%</strong>) é praticamente metade da retenção de 6 meses ({pct_r6:.1f}%), apontando perda significativa no segundo semestre.",
        f"O ano <strong>{best_rev_yr}</strong> registrou a maior taxa de revisão ({best_rev_pct:.1f}%), possivelmente relacionado a mudanças no processo de revisão da lista.",
    ]
    for ins in insights:
        st.markdown(f'<div class="insight-box">{ins}</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ANÁLISE DE COORTE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔬 Análise de Coorte":

    st.markdown("""
    <div class="page-header">
      <h1>Análise de Coorte por Ano de Entrada</h1>
      <p>Acompanhamento da evolução de cada coorte ao longo do funil de contribuição</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Cohort size bar ────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Tamanho das Coortes por Ano</div>', unsafe_allow_html=True)

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df_filt["entry_year"], y=df_filt["cohort_size"],
        name="Novos Contribuidores",
        marker=dict(color=TEAL, opacity=0.85, line=dict(color="#0d1117", width=0.5))))
    fig_bar.add_trace(go.Bar(x=df_filt["entry_year"], y=df_filt["n_patched"],
        name="Enviaram Patch", marker=dict(color=BLUE, opacity=0.85)))
    fig_bar.add_trace(go.Bar(x=df_filt["entry_year"], y=df_filt["n_reviewed"],
        name="Receberam Revisão", marker=dict(color=VIOLET, opacity=0.85)))
    fig_bar.update_layout(**CHART_LAYOUT, barmode="group", height=320,
                          yaxis_title="Nº de Contribuidores", xaxis_title="Ano",
                          hovermode="x unified")
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Retention Heatmap ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Heatmap de Retenção por Coorte</div>', unsafe_allow_html=True)
    st.caption("Percentual de novos contribuidores de cada coorte que atingiu cada etapa do funil")

    heat_data = df_filt[["entry_year","pct_patch","pct_review","pct_ret_6m","pct_ret_12m"]].set_index("entry_year")
    heat_data.columns = ["% Patch", "% Revisão", "% Retido 6m", "% Retido 12m"]

    fig_heat = go.Figure(go.Heatmap(
        z=heat_data.values.T,
        x=[str(y) for y in heat_data.index],
        y=heat_data.columns.tolist(),
        colorscale=[[0, "#0d1117"], [0.3, "#1c3a4a"], [0.6, "#0e7490"], [1.0, "#2dd4bf"]],
        text=np.round(heat_data.values.T, 1),
        texttemplate="%{text}%",
        textfont=dict(size=9, family="JetBrains Mono"),
        hoverongaps=False,
        showscale=True,
        colorbar=dict(tickcolor="#8b949e", outlinecolor="#21262d"),
    ))
    fig_heat.update_layout(**CHART_LAYOUT, height=280)
    fig_heat.update_xaxes(tickangle=-45, tickfont=dict(size=9))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_heat, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Dropout Waterfall ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Análise de Abandono por Etapa</div>', unsafe_allow_html=True)

    left_col, right_col = st.columns([1, 1])

    with left_col:
        year_sel = st.selectbox("Selecionar coorte para detalhar",
                                 df_filt["entry_year"].tolist(),
                                 index=len(df_filt)//2)
        row = df_filt[df_filt["entry_year"] == year_sel].iloc[0]

        labels  = ["Novos", "→ Patch", "→ Revisão", "→ Retido 6m", "→ Retido 12m"]
        vals_abs = [row.cohort_size, row.n_patched, row.n_reviewed, row.n_retained_6m, row.n_retained_12m]
        drops    = [0] + [vals_abs[i-1] - vals_abs[i] for i in range(1, len(vals_abs))]

        fig_wf = go.Figure()
        colors_wf = [TEAL] + [ROSE]*4
        fig_wf.add_trace(go.Bar(
            x=labels, y=vals_abs,
            marker_color=colors_wf,
            text=[f"{v:,}" for v in vals_abs],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=11),
        ))
        fig_wf.update_layout(**CHART_LAYOUT, height=320, showlegend=False,
                             title=dict(text=f"Coorte {year_sel}", font=dict(size=14, color="#e6edf3"), x=0.5),
                             yaxis_title="Contribuidores")
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_wf, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        # Step conversion rates for selected cohort
        conv_labels = ["Novo → Patch", "Patch → Revisão", "Revisão → Ret.6m", "Ret.6m → Ret.12m"]
        conv_values = [
            row.n_patched / row.cohort_size * 100,
            row.n_reviewed / row.n_patched * 100 if row.n_patched else 0,
            row.n_retained_6m / row.n_reviewed * 100 if row.n_reviewed else 0,
            row.n_retained_12m / row.n_retained_6m * 100 if row.n_retained_6m else 0,
        ]
        fig_conv = go.Figure(go.Bar(
            x=conv_values, y=conv_labels,
            orientation="h",
            marker=dict(
                color=conv_values,
                colorscale=[[0, "#f87171"], [0.5, "#fbbf24"], [1.0, "#2dd4bf"]],
                cmin=0, cmax=100,
                showscale=False,
            ),
            text=[f"{v:.1f}%" for v in conv_values],
            textposition="outside",
            textfont=dict(family="JetBrains Mono", size=12),
        ))
        fig_conv.update_layout(**CHART_LAYOUT, height=320, showlegend=False,
                               title=dict(text=f"Conversão entre etapas · {year_sel}",
                                          font=dict(size=14, color="#e6edf3"), x=0.5))
        fig_conv.update_xaxes(range=[0, 115], title_text="Taxa de conversão (%)")
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_conv, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Retention scatter ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Relação entre Tamanho de Coorte e Retenção</div>', unsafe_allow_html=True)

    fig_scat = go.Figure()
    fig_scat.add_trace(go.Scatter(
        x=df_filt["cohort_size"],
        y=df_filt["pct_ret_12m"],
        mode="markers+text",
        text=df_filt["entry_year"].astype(str),
        textposition="top center",
        textfont=dict(size=9, color="#8b949e"),
        marker=dict(
            size=df_filt["n_patched"] / df_filt["n_patched"].max() * 28 + 6,
            color=df_filt["entry_year"],
            colorscale="teal",
            showscale=True,
            colorbar=dict(title="Ano", tickcolor="#8b949e", outlinecolor="#21262d"),
            line=dict(color="#21262d", width=1),
        ),
        hovertemplate="<b>%{text}</b><br>Cohort: %{x}<br>Ret.12m: %{y:.1f}%<extra></extra>",
    ))
    fig_scat.update_layout(**CHART_LAYOUT, height=360,
                           xaxis_title="Tamanho do Cohort (novos contribuidores)",
                           yaxis_title="Retenção 12 meses (%)")
    st.caption("Tamanho do círculo proporcional ao número de contribuidores que enviaram patch")
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_scat, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Data table ─────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Tabela de Dados Completa</div>', unsafe_allow_html=True)
    display_df = df_filt.rename(columns={
        "entry_year": "Ano", "cohort_size": "Novos", "n_patched": "Patcharam",
        "n_reviewed": "Revisados", "n_retained_6m": "Retidos 6m", "n_retained_12m": "Retidos 12m",
        "pct_patch": "% Patch", "pct_review": "% Revisão",
        "pct_ret_6m": "% Ret.6m", "pct_ret_12m": "% Ret.12m",
    })
    st.dataframe(
        display_df.set_index("Ano").style
        .background_gradient(subset=["% Patch","% Revisão","% Ret.6m","% Ret.12m"],
                             cmap="YlGn", vmin=0)
        .format({"% Patch": "{:.1f}%", "% Revisão": "{:.1f}%",
                 "% Ret.6m": "{:.1f}%", "% Ret.12m": "{:.1f}%"}),
        use_container_width=True, height=420,
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — FUNIL DE CONTRIBUIÇÃO
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🚰 Funil de Contribuição":

    st.markdown(f"""
    <div class="page-header">
    <h1>Funil de Contribuição — {short_list_name}</h1>
    <p>Análise detalhada do pipeline desde o primeiro contato até a retenção de longo prazo</p>
    </div>
    """, unsafe_allow_html=True)

    # ── Sankey diagram ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">Fluxo de Contribuidores pelo Funil (período selecionado)</div>', unsafe_allow_html=True)

    total = df_filt["cohort_size"].sum()
    patched = df_filt["n_patched"].sum()
    reviewed = df_filt["n_reviewed"].sum()
    ret6 = df_filt["n_retained_6m"].sum()
    ret12 = df_filt["n_retained_12m"].sum()

    not_patched  = total - patched
    patched_only = patched - reviewed
    reviewed_only = reviewed - ret6
    ret6_only    = ret6 - ret12

    node_labels = [
        "Novos Contribuidores",
        "Enviaram Patch",
        "Receberam Revisão",
        "Retidos 6m",
        "Retidos 12m",
        "Sem Patch",
        "Sem Revisão",
        "Abandono 6m",
        "Abandono 12m",
    ]

    fig_sankey = go.Figure(go.Sankey(
        node=dict(
            pad=20, thickness=22,
            line=dict(color="#0d1117", width=0.5),
            label=node_labels,
            color=[TEAL, BLUE, VIOLET, AMBER, GREEN, "#374151", "#374151", "#374151", "#374151"],
        ),
        link=dict(
            source=[0, 0, 1, 1, 2, 2, 3, 3],
            target=[1, 5, 2, 6, 3, 7, 4, 8],
            value=[patched, not_patched, reviewed, patched_only, ret6, reviewed_only, ret12, ret6_only],
            color=["rgba(45,212,191,0.25)", "rgba(248,113,113,0.15)",
                   "rgba(96,165,250,0.25)", "rgba(248,113,113,0.15)",
                   "rgba(167,139,250,0.25)", "rgba(248,113,113,0.15)",
                   "rgba(74,222,128,0.25)", "rgba(248,113,113,0.15)"],
        ),
    ))
    fig_sankey.update_layout(**CHART_LAYOUT, height=480)
    fig_sankey.update_layout(font=dict(size=11, family="Sora, sans-serif"))
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_sankey, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

    # ── Funnel global (JSON) ───────────────────────────────────────────────────
    st.markdown(f"""<div class="section-title">Funil Global da Lista {list_name} (todos os anos)</div>""", unsafe_allow_html=True)
    stages_json = funnel["stages"]

    col_f1, col_f2 = st.columns([3, 2])

    with col_f1:
        fig_glob = go.Figure(go.Funnel(
            y=[s["label"] for s in stages_json],
            x=[s["n"] for s in stages_json],
            textinfo="value+percent initial",
            marker=dict(
                color=[TEAL, BLUE, VIOLET, AMBER, ROSE],
                line=dict(width=1, color="#0d1117"),
            ),
            connector=dict(line=dict(color="#30363d", width=1)),
        ))
        fig_glob.update_layout(**CHART_LAYOUT, height=360)
        st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
        st.plotly_chart(fig_glob, use_container_width=True, config={"displayModeBar": False})
        st.markdown('</div>', unsafe_allow_html=True)

    with col_f2:
        st.markdown('<div class="section-title" style="margin-top:0">Taxas Acumuladas</div>', unsafe_allow_html=True)
        for s in stages_json:
            bar_w = s["pct"]
            color = TEAL if s["pct"] > 20 else (AMBER if s["pct"] > 5 else ROSE)
            st.markdown(f"""
            <div style="margin-bottom:1rem">
              <div style="display:flex;justify-content:space-between;margin-bottom:4px">
                <span style="font-size:0.82rem;color:#c9d1d9">{s['label']}</span>
                <span style="font-family:'JetBrains Mono',monospace;font-size:0.85rem;color:{color}">{s['pct']}%</span>
              </div>
              <div style="background:#21262d;border-radius:4px;height:8px">
                <div style="background:{color};width:{bar_w}%;height:8px;border-radius:4px;transition:width 0.5s"></div>
              </div>
              <div style="font-size:0.75rem;color:#8b949e;margin-top:2px">{s['n']:,} contribuidores</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card amber" style="margin-top:1.2rem">
          <div class="metric-label">MTTFP (Tempo médio ao 1º Patch)</div>
          <div class="metric-value" style="font-size:1.6rem">{funnel['mttfp_days']:.1f} dias</div>
        </div>
        <br>
        <div class="metric-card blue">
          <div class="metric-label">Conversão Patch → Revisão</div>
          <div class="metric-value" style="font-size:1.6rem">{funnel['review_conversion_pct']:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Stacked area — volume over time ────────────────────────────────────────
    st.markdown('<div class="section-title">Volume de Contribuidores por Etapa ao Longo do Tempo</div>', unsafe_allow_html=True)

    fig_area = go.Figure()
    fig_area.add_trace(go.Scatter(
        x=df_filt["entry_year"], y=df_filt["cohort_size"],
        name="Novos", fill="tozeroy",
        line=dict(color=TEAL, width=0), fillcolor="rgba(45,212,191,0.15)"))
    fig_area.add_trace(go.Scatter(
        x=df_filt["entry_year"], y=df_filt["n_patched"],
        name="Enviaram Patch", fill="tozeroy",
        line=dict(color=BLUE, width=0), fillcolor="rgba(96,165,250,0.2)"))
    fig_area.add_trace(go.Scatter(
        x=df_filt["entry_year"], y=df_filt["n_reviewed"],
        name="Revisados", fill="tozeroy",
        line=dict(color=VIOLET, width=0), fillcolor="rgba(167,139,250,0.25)"))
    fig_area.add_trace(go.Scatter(
        x=df_filt["entry_year"], y=df_filt["n_retained_12m"],
        name="Retidos 12m", fill="tozeroy",
        line=dict(color=ROSE, width=0), fillcolor="rgba(248,113,113,0.35)"))
    fig_area.update_layout(**CHART_LAYOUT, height=300, hovermode="x unified",
                           yaxis_title="Contribuidores", xaxis_title="Ano de Entrada")
    st.markdown('<div class="chart-wrap">', unsafe_allow_html=True)
    st.plotly_chart(fig_area, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — GLOSSÁRIO
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📖 Glossário":

    st.markdown("""
    <div class="page-header">
      <h1>Glossário de Termos</h1>
      <p>Definições dos conceitos utilizados neste dashboard</p>
    </div>
    """, unsafe_allow_html=True)

    glossary = [
        ("Coorte (Cohort)", "Grupo de contribuidores que fizeram seu primeiro contato com a lista de e-mails no mesmo ano. A análise de coorte permite acompanhar a jornada de cada grupo de forma isolada, evitando misturar comportamentos de pessoas em momentos diferentes da comunidade."),
        (f"Novo Contribuidor", f"Qualquer pessoa que enviou pelo menos uma mensagem para a lista {short_list_name} pela primeira vez em um dado ano, independentemente do tipo de mensagem (patch, pergunta, revisão etc.)."),
        ("Patch", "Conjunto de modificações de código-fonte submetido à lista de e-mails para revisão e possível inclusão no kernel Linux. No contexto desta pesquisa, contabilizamos contribuidores que enviaram ao menos um patch."),
        ("Revisão (Code Review)", f"Feedback técnico formal recebido por um patch submetido. Na lista {short_list_name}, revisões chegam como respostas de e-mail ao patch original. Um contribuidor é marcado como 'revisado' se ao menos um de seus patches recebeu ao menos uma revisão."),
        ("MTTFP — Mean Time to First Patch", f"Tempo médio (em dias) entre o primeiro contato de um contribuidor com a lista {short_list_name} e o envio do seu primeiro patch. Mede o tempo de 'incubação' ou fase de lurking. Na {list_name}, esse valor é de ~58 dias."),
        ("Taxa de Conversão Patch→Revisão", f"Percentual de contribuidores que enviaram pelo menos um patch E tiveram ao menos um de seus patches revisado. Mede a eficiência do processo de feedback da comunidade. Na {list_name}, apenas ~20,6% dos patchers recebem revisão."),
        ("Retenção 6 meses", f"Percentual de novos contribuidores de um coorte que continuaram ativos na lista {short_list_name} pelos 6 meses seguintes ao seu primeiro contato. 'Ativo' é definido como pelo menos uma mensagem enviada no período."),
        ("Retenção 12 meses", f"Análogo à retenção de 6 meses, mas para o período de 12 meses após o primeiro contato. Indica a capacidade da comunidade de manter novos membros por um ano completo."),
        ("Funil de Contribuição", "Representação visual das etapas que um novo contribuidor percorre, desde o primeiro contato até a retenção de longo prazo. Cada etapa do funil representa uma barreira ou filtro que reduz o número de contribuidores ativos."),
        ("Sankey Diagram", "Tipo de visualização de fluxo onde a largura das setas é proporcional ao volume de dados que flui entre nós. Aqui usado para mostrar quantos contribuidores progridem em cada etapa do funil vs. quantos abandonam."),
        ("lore.kernel.org", "Arquivo público de todas as listas de e-mails do kernel Linux. Fonte dos dados utilizados nesta pesquisa para mineração de patches e revisões."),
        ("Lurking", "Comportamento de observação passiva em uma comunidade online — quando um usuário lê mensagens mas não participa ativamente. O período de lurking antes do primeiro patch é capturado pela métrica MTTFP."),
        ("Drop-off", "Taxa de abandono entre duas etapas consecutivas do funil. Um alto drop-off entre 'Novo Contribuidor' e 'Enviou Patch' indica barreiras de entrada significativas."),
    ]

    col1, col2 = st.columns(2)
    for i, (term, defn) in enumerate(glossary):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="gloss-term">
              <h4>📌 {term}</h4>
              <p>{defn}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Referências Metodológicas</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="insight-box">
      Os dados foram extraídos da lista <strong>{list_name}</strong> via <strong>lore.kernel.org</strong>.
      A identificação de contribuidores é feita por endereço de e-mail. Patches são identificados por
      prefixos <code>[PATCH]</code> nas mensagens. Revisões são respostas em-thread com comentários técnicos.
      A retenção é calculada com janela deslizante de 6 e 12 meses a partir do primeiro contato.
    </div>
    """, unsafe_allow_html=True)
