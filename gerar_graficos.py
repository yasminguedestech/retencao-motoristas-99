"""Gera os 3 gráficos do projeto 99 — design moderno, fundo branco."""
import matplotlib
matplotlib.use("Agg")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
import warnings
warnings.filterwarnings("ignore")

# ── Paleta 99 — amarelo + preto + branco ────────────────────
BG      = "#FFFFFF"
CARD    = "#FFFFFF"
SUBTLE  = "#FFFBE6"   # amarelo quase branco — fill de área
BORDER  = "#EDEDED"   # borda neutra
TEXT    = "#111111"   # preto 99
MUTED   = "#666666"   # cinza neutro

Y_BRIGHT = "#FFD600"  # amarelo 99 — Ativo / destaque principal
Y_MID    = "#F0C000"  # amarelo escurecido — linha / referência
Y_LIGHT  = "#FFF3B0"  # amarelo muito claro — fill de área
Y_DEEP   = "#1C1917"  # preto 99 — Churn / contraste forte
Y_WARM   = "#F5A800"  # âmbar — gradiente intermediário

CORES_STATUS = [Y_BRIGHT, Y_DEEP]   # Ativo (amarelo), Churn (preto)

plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    BG,
    "axes.edgecolor":    BORDER,
    "axes.labelcolor":   MUTED,
    "axes.titlecolor":   TEXT,
    "axes.titlesize":    12,
    "axes.labelsize":    9,
    "axes.titlepad":     12,
    "axes.spines.top":   False,
    "axes.spines.right": False,
    "axes.spines.left":  False,
    "axes.spines.bottom": True,
    "axes.grid":         True,
    "grid.color":        "#F5F5F0",
    "grid.linewidth":    0.7,
    "xtick.color":       MUTED,
    "ytick.color":       MUTED,
    "text.color":        TEXT,
    "font.family":       "DejaVu Sans",
    "legend.facecolor":  BG,
    "legend.edgecolor":  BORDER,
    "legend.labelcolor": TEXT,
    "legend.framealpha": 1,
})

np.random.seed(42)
N = 1200
cidades = ["São Paulo","Rio de Janeiro","Belo Horizonte","Curitiba","Fortaleza","Recife"]
pesos   = [0.40,0.25,0.15,0.10,0.06,0.04]
df = pd.DataFrame({
    "motorista_id": range(1, N+1),
    "cidade": np.random.choice(cidades, N, p=pesos),
    "tempo_plataforma_meses": np.random.randint(1, 37, N),
    "corridas_por_semana": np.random.choice(
        [0,1,2,3,4,5,6,7,8,9,10], N,
        p=[0.05,0.08,0.10,0.12,0.14,0.14,0.12,0.10,0.08,0.05,0.02]),
    "avaliacao_media": np.round(np.random.beta(8,2)*2+3,1).clip(1,5),
    "ganho_medio_semanal_r$": np.random.normal(700,200,N).clip(100,1800).round(2),
    "cancelamentos_mes": np.random.poisson(2,N),
    "suporte_acionado": np.random.choice([0,1],N,p=[0.65,0.35]),
    "bonus_recebido":   np.random.choice([0,1],N,p=[0.45,0.55]),
})
prob_churn = (
    0.05
    + (df["avaliacao_media"]<4.0).astype(int)*0.20
    + (df["ganho_medio_semanal_r$"]<500).astype(int)*0.25
    + (df["cancelamentos_mes"]>3).astype(int)*0.15
    + (df["corridas_por_semana"]<=2).astype(int)*0.18
    + (df["suporte_acionado"]==1).astype(int)*0.10
    - (df["bonus_recebido"]==1).astype(int)*0.12
    - (df["tempo_plataforma_meses"]>12).astype(int)*0.08
).clip(0,0.95)
df["churn"]  = (np.random.rand(N)<prob_churn).astype(int)
df["status"] = df["churn"].map({0:"Ativo",1:"Inativo (Churn)"})
motivos = ["Baixa remuneração","Migrou p/ concorrente","Problemas com suporte","Muitos cancelamentos","Outros"]
df.loc[df["churn"]==1,"motivo_saida"] = np.random.choice(
    motivos, df["churn"].sum(), p=[0.35,0.28,0.17,0.13,0.07])
df["motivo_saida"] = df["motivo_saida"].fillna("—")

# ── FIG 1: Visão Geral ──────────────────────────────────────
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.patch.set_facecolor(BG)
fig.suptitle("Análise de Retenção de Motoristas — 99",
             fontsize=17, fontweight="bold", color=TEXT, y=1.01)

# 1a. Rosca — status
ax = axes[0,0]; ax.set_facecolor(BG); ax.axis("off")
contagem = df["status"].value_counts()
wedges, _, autotexts = ax.pie(
    contagem, labels=None, autopct="%1.1f%%",
    colors=CORES_STATUS, startangle=90, pctdistance=0.78,
    wedgeprops=dict(edgecolor=BG, linewidth=4, width=0.5))
for at, color in zip(autotexts, [TEXT, "#FFFFFF"]):
    at.set_fontsize(12); at.set_fontweight("bold"); at.set_color(color)
churn_n = df["churn"].sum()
ativo_n = N - churn_n
ax.text(0, 0.12, f"{ativo_n}", ha="center", va="center",
        fontsize=22, color=Y_BRIGHT, fontweight="bold")
ax.text(0, -0.12, f"{churn_n}", ha="center", va="center",
        fontsize=16, color=Y_DEEP, fontweight="bold")
legend_els = [
    mpatches.Patch(facecolor=Y_BRIGHT, label=f"Ativo  ({ativo_n})"),
    mpatches.Patch(facecolor=Y_DEEP,   label=f"Churn  ({churn_n})"),
]
ax.legend(handles=legend_els, loc="lower center", bbox_to_anchor=(0.5,-0.08),
          ncol=2, fontsize=9, frameon=False)
ax.set_title("Distribuição de Status", color=TEXT, fontsize=12, pad=10)

# 1b. Boxplot — avaliação
ax = axes[0,1]; ax.set_facecolor(BG)
grupos = [df[df["churn"]==0]["avaliacao_media"], df[df["churn"]==1]["avaliacao_media"]]
bp = ax.boxplot(grupos, patch_artist=True, widths=0.38,
                medianprops=dict(color=TEXT, linewidth=2.2),
                whiskerprops=dict(color=MUTED, linewidth=1.3),
                capprops=dict(color=MUTED, linewidth=1.3),
                flierprops=dict(marker="o", markerfacecolor=BORDER,
                                markeredgecolor=MUTED, markersize=4, alpha=0.7))
bp["boxes"][0].set_facecolor(Y_LIGHT); bp["boxes"][0].set_edgecolor(Y_MID)
bp["boxes"][1].set_facecolor(Y_WARM+"44"); bp["boxes"][1].set_edgecolor(Y_DEEP)
ax.set_xticks([1,2]); ax.set_xticklabels(["Ativo","Inativo (Churn)"], color=TEXT, fontsize=10)
ax.set_ylabel("Avaliação Média"); ax.set_title("Avaliação Média × Status")
ax.axhline(4.0, color=Y_MID, linewidth=1.5, linestyle="--", alpha=0.9, label="Limite 4.0")
ax.legend(fontsize=9, frameon=False)
ax.spines["bottom"].set_color(BORDER)

# 1c. Barras horizontais — churn por cidade
ax = axes[1,0]; ax.set_facecolor(BG)
churn_cidade = df.groupby("cidade")["churn"].mean().sort_values()*100
media = churn_cidade.mean()
cores_c = [Y_BRIGHT if v == churn_cidade.max() else Y_LIGHT for v in churn_cidade.values]
bars = ax.barh(churn_cidade.index, churn_cidade.values,
               color=cores_c, edgecolor=BORDER, linewidth=0.8, height=0.55)
ax.axvline(media, color=Y_MID, linewidth=1.4, linestyle="--",
           alpha=0.9, label=f"Média  {media:.1f}%")
ax.set_xlabel("Taxa de Churn (%)"); ax.set_title("Taxa de Churn por Cidade")
ax.legend(fontsize=9, frameon=False)
ax.spines["bottom"].set_color(BORDER)
ax.grid(axis="x", color="#F5F5F0", linewidth=0.7)
ax.grid(axis="y", visible=False)
for bar, val in zip(bars, churn_cidade.values):
    ax.text(val+0.2, bar.get_y()+bar.get_height()/2,
            f"{val:.1f}%", va="center", fontsize=9,
            color=TEXT, fontweight="bold" if val==churn_cidade.max() else "normal")

# 1d. Scatter — corridas vs ganho (com jitter)
ax = axes[1,1]; ax.set_facecolor(BG)
mask = df["churn"]==0
jx_a = df[mask]["corridas_por_semana"]  + np.random.uniform(-0.35,0.35,mask.sum())
jx_c = df[~mask]["corridas_por_semana"] + np.random.uniform(-0.35,0.35,(~mask).sum())
ax.scatter(jx_a, df[mask]["ganho_medio_semanal_r$"],
           c=Y_BRIGHT, alpha=0.35, s=16, label="Ativo", linewidths=0)
ax.scatter(jx_c, df[~mask]["ganho_medio_semanal_r$"],
           c=Y_DEEP, alpha=0.45, s=16, label="Churn", linewidths=0)
ax.axhline(500, color=Y_MID, linewidth=1.5, linestyle="--", alpha=0.9, label="R$ 500/sem")
ax.set_xlabel("Corridas por Semana"); ax.set_ylabel("Ganho Médio Semanal (R$)")
ax.set_title("Corridas × Ganho por Status")
ax.legend(fontsize=9, frameon=False)
ax.spines["bottom"].set_color(BORDER)

plt.tight_layout(pad=2.5)
plt.savefig("fig1 visao geral.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("fig1 salva")

# ── FIG 2: Fatores ──────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(17, 5.5))
fig.patch.set_facecolor(BG)
fig.suptitle("Fatores que Influenciam o Churn de Motoristas",
             fontsize=15, fontweight="bold", color=TEXT)

# 2a. Motivos de saída
ax = axes[0]; ax.set_facecolor(BG)
motivos_count = df[df["churn"]==1]["motivo_saida"].value_counts()
pal = [Y_BRIGHT, Y_MID, Y_WARM, Y_LIGHT, BORDER]
bars = ax.bar(range(len(motivos_count)), motivos_count.values,
              color=pal[:len(motivos_count)], edgecolor=BG, linewidth=1.5, width=0.58)
ax.set_xticks(range(len(motivos_count)))
ax.set_xticklabels(motivos_count.index, rotation=28, ha="right", fontsize=8.5)
ax.set_ylabel("Motoristas"); ax.set_title("Motivos de Saída")
ax.spines["bottom"].set_color(BORDER)
for bar, val in zip(bars, motivos_count.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
            str(val), ha="center", fontsize=10, fontweight="bold", color=MUTED)

# 2b. Churn por faixa de ganho
ax = axes[1]; ax.set_facecolor(BG)
bins = [0,400,600,800,1000,1800]; labels_ganho=["<400","400–600","600–800","800–1k",">1k"]
df["faixa_ganho"] = pd.cut(df["ganho_medio_semanal_r$"], bins=bins, labels=labels_ganho)
churn_ganho = df.groupby("faixa_ganho", observed=True)["churn"].mean()*100
cores_g = [Y_BRIGHT if v == churn_ganho.max()
           else Y_MID if v >= churn_ganho.quantile(0.6)
           else Y_LIGHT for v in churn_ganho.values]
bars = ax.bar(churn_ganho.index, churn_ganho.values,
              color=cores_g, edgecolor=BG, linewidth=1.5, width=0.58)
ax.set_xlabel("Ganho Médio Semanal (R$)"); ax.set_ylabel("Taxa de Churn (%)")
ax.set_title("Churn por Faixa de Ganho")
ax.spines["bottom"].set_color(BORDER)
for bar, val in zip(bars, churn_ganho.values):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.3,
            f"{val:.1f}%", ha="center", fontsize=10, fontweight="bold", color=MUTED)

# 2c. Churn por tempo na plataforma
ax = axes[2]; ax.set_facecolor(BG)
bins_t=[0,3,6,12,24,36]; labels_t=["0–3m","3–6m","6–12m","12–24m","24–36m"]
df["faixa_tempo"] = pd.cut(df["tempo_plataforma_meses"], bins=bins_t, labels=labels_t)
churn_tempo = df.groupby("faixa_tempo", observed=True)["churn"].mean()*100
xs = list(range(len(churn_tempo)))
ax.fill_between(xs, churn_tempo.values, alpha=0.15, color=Y_BRIGHT)
ax.plot(xs, churn_tempo.values, color=Y_MID, linewidth=2.5,
        marker="o", markersize=9, markerfacecolor=Y_BRIGHT,
        markeredgecolor=Y_MID, markeredgewidth=2)
ax.set_xticks(xs); ax.set_xticklabels(churn_tempo.index)
ax.set_ylabel("Taxa de Churn (%)"); ax.set_title("Churn por Tempo na Plataforma")
ax.spines["bottom"].set_color(BORDER)
for i, val in enumerate(churn_tempo.values):
    ax.text(i, val+0.9, f"{val:.1f}%", ha="center", fontsize=9,
            fontweight="bold", color=MUTED)

plt.tight_layout(pad=2.5)
plt.savefig("fig2 fatores churn.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("fig2 salva")

# ── FIG 3: Correlação ───────────────────────────────────────
fig, ax = plt.subplots(figsize=(10,7))
fig.patch.set_facecolor(BG); ax.set_facecolor(BG)

cols_num = ["churn","avaliacao_media","ganho_medio_semanal_r$","corridas_por_semana",
            "cancelamentos_mes","tempo_plataforma_meses","suporte_acionado","bonus_recebido"]
corr = df[cols_num].corr()
labels_pt = ["Churn","Avaliação","Ganho Sem.","Corridas/Sem.",
             "Cancelamentos","Tempo Plataf.","Suporte","Bônus"]

mask = np.triu(np.ones_like(corr, dtype=bool))
cmap_99 = LinearSegmentedColormap.from_list("99brand", ["#FFFBE6", Y_LIGHT, Y_BRIGHT, Y_DEEP])

sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap=cmap_99,
            vmin=-0.2, vmax=0.2,
            ax=ax, xticklabels=labels_pt, yticklabels=labels_pt,
            linewidths=2, linecolor=BG,
            annot_kws={"size":10, "color":TEXT},
            cbar_kws={"shrink":0.7})
ax.set_xticklabels(ax.get_xticklabels(), color=MUTED, fontsize=9, rotation=35, ha="right")
ax.set_yticklabels(ax.get_yticklabels(), color=MUTED, fontsize=9, rotation=0)
ax.set_title("Correlação entre Variáveis e Churn",
             fontsize=14, fontweight="bold", color=TEXT, pad=16)
ax.collections[0].colorbar.ax.yaxis.set_tick_params(color=MUTED)
plt.setp(ax.collections[0].colorbar.ax.yaxis.get_ticklabels(), color=MUTED)

plt.tight_layout()
plt.savefig("fig3 correlacao.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.close()
print("fig3 salva")
print("todos os graficos gerados!")
