"""Gera os 3 gráficos do projeto 99 e salva como PNG."""
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

BG="#0D0D0D"; CARD="#1A1A1A"; BORDER="#2E2E2E"
AMARELO="#FFD600"; AMBER="#FFA000"; GOLD="#F59E0B"; CREAM="#FFF8DC"
MUTED="#A0A0A0"; TEXT="#F5F5F5"; VERMELHO="#EF4444"; VERDE="#22C55E"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": CARD, "axes.edgecolor": BORDER,
    "axes.labelcolor": MUTED, "axes.titlecolor": TEXT, "axes.titlesize": 13,
    "axes.labelsize": 10, "axes.titlepad": 14, "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.color": BORDER,
    "grid.linewidth": 0.6, "xtick.color": MUTED, "ytick.color": MUTED,
    "text.color": TEXT, "font.family": "DejaVu Sans",
    "legend.facecolor": CARD, "legend.edgecolor": BORDER, "legend.labelcolor": TEXT,
})

np.random.seed(42)
N = 1200
cidades = ["São Paulo","Rio de Janeiro","Belo Horizonte","Curitiba","Fortaleza","Recife"]
pesos   = [0.40,0.25,0.15,0.10,0.06,0.04]
df = pd.DataFrame({
    "motorista_id": range(1, N+1),
    "cidade": np.random.choice(cidades, N, p=pesos),
    "tempo_plataforma_meses": np.random.randint(1, 37, N),
    "corridas_por_semana": np.random.choice([0,1,2,3,4,5,6,7,8,9,10],N,
        p=[0.05,0.08,0.10,0.12,0.14,0.14,0.12,0.10,0.08,0.05,0.02]),
    "avaliacao_media": np.round(np.random.beta(8,2)*2+3,1).clip(1,5),
    "ganho_medio_semanal_r$": np.random.normal(700,200,N).clip(100,1800).round(2),
    "cancelamentos_mes": np.random.poisson(2,N),
    "suporte_acionado": np.random.choice([0,1],N,p=[0.65,0.35]),
    "bonus_recebido": np.random.choice([0,1],N,p=[0.45,0.55]),
})
prob_churn = (0.05
    +(df["avaliacao_media"]<4.0).astype(int)*0.20
    +(df["ganho_medio_semanal_r$"]<500).astype(int)*0.25
    +(df["cancelamentos_mes"]>3).astype(int)*0.15
    +(df["corridas_por_semana"]<=2).astype(int)*0.18
    +(df["suporte_acionado"]==1).astype(int)*0.10
    -(df["bonus_recebido"]==1).astype(int)*0.12
    -(df["tempo_plataforma_meses"]>12).astype(int)*0.08).clip(0,0.95)
df["churn"]=(np.random.rand(N)<prob_churn).astype(int)
df["status"]=df["churn"].map({0:"Ativo",1:"Inativo (Churn)"})
motivos=["Baixa remuneração","Migrou p/ concorrente","Problemas com suporte","Muitos cancelamentos","Outros"]
df.loc[df["churn"]==1,"motivo_saida"]=np.random.choice(motivos,df["churn"].sum(),p=[0.35,0.28,0.17,0.13,0.07])
df["motivo_saida"]=df["motivo_saida"].fillna("—")

# ── FIG 1: Visão Geral ──────────────────────────────────────
fig,axes=plt.subplots(2,2,figsize=(15,10)); fig.patch.set_facecolor(BG)
fig.suptitle("Análise de Retenção de Motoristas — 99",fontsize=18,fontweight="bold",color=AMARELO,y=1.01)

ax=axes[0,0]; ax.set_facecolor(CARD)
contagem=df["status"].value_counts()
wedges,texts,autotexts=ax.pie(contagem,labels=None,autopct="%1.1f%%",
    colors=[VERDE,VERMELHO],startangle=90,pctdistance=0.75,
    wedgeprops=dict(edgecolor=BG,linewidth=3,width=0.55))
for at in autotexts: at.set_fontsize(13); at.set_fontweight("bold"); at.set_color(TEXT)
ax.legend(["Ativo","Inativo (Churn)"],loc="center",fontsize=10,facecolor=CARD,edgecolor=BORDER,labelcolor=TEXT)
ax.text(0,0,f"{df['churn'].sum()}\nchurn",ha="center",va="center",fontsize=12,color=VERMELHO,fontweight="bold")
ax.set_title("Distribuição de Status",color=TEXT)

ax=axes[0,1]; ax.set_facecolor(CARD)
grupos=[df[df["churn"]==0]["avaliacao_media"],df[df["churn"]==1]["avaliacao_media"]]
bp=ax.boxplot(grupos,patch_artist=True,widths=0.45,
    medianprops=dict(color=AMARELO,linewidth=2.5),
    whiskerprops=dict(color=MUTED,linewidth=1.5),capprops=dict(color=MUTED,linewidth=1.5),
    flierprops=dict(marker="o",markerfacecolor=MUTED,markersize=4,alpha=0.5))
bp["boxes"][0].set_facecolor(VERDE+"55"); bp["boxes"][0].set_edgecolor(VERDE)
bp["boxes"][1].set_facecolor(VERMELHO+"55"); bp["boxes"][1].set_edgecolor(VERMELHO)
ax.set_xticks([1,2]); ax.set_xticklabels(["Ativo","Inativo (Churn)"],color=TEXT)
ax.set_ylabel("Avaliação Média",color=MUTED); ax.set_title("Avaliação Média × Status",color=TEXT)
ax.axhline(4.0,color=AMARELO,linewidth=1.8,linestyle="--",alpha=0.8,label="Limite 4.0")
ax.legend(fontsize=9); ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)

ax=axes[1,0]; ax.set_facecolor(CARD)
churn_cidade=df.groupby("cidade")["churn"].mean().sort_values()*100; media=churn_cidade.mean()
cores_c=[AMARELO if v>media else AMBER+"99" for v in churn_cidade.values]
bars=ax.barh(churn_cidade.index,churn_cidade.values,color=cores_c,edgecolor="none",height=0.6)
ax.axvline(media,color=CREAM,linewidth=1.5,linestyle="--",alpha=0.7,label=f"Média: {media:.1f}%")
ax.set_xlabel("Taxa de Churn (%)",color=MUTED); ax.set_title("Taxa de Churn por Cidade",color=TEXT)
ax.legend(fontsize=9); ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)
for bar,val in zip(bars,churn_cidade.values):
    ax.text(val+0.3,bar.get_y()+bar.get_height()/2,f"{val:.1f}%",va="center",fontsize=9,color=TEXT)

ax=axes[1,1]; ax.set_facecolor(CARD)
mask_ativo=df["churn"]==0
ax.scatter(df[mask_ativo]["corridas_por_semana"],df[mask_ativo]["ganho_medio_semanal_r$"],c=VERDE,alpha=0.25,s=18,label="Ativo")
ax.scatter(df[~mask_ativo]["corridas_por_semana"],df[~mask_ativo]["ganho_medio_semanal_r$"],c=VERMELHO,alpha=0.35,s=18,label="Churn")
ax.axhline(500,color=AMARELO,linewidth=1.5,linestyle="--",alpha=0.8,label="R$ 500/sem")
ax.set_xlabel("Corridas por Semana",color=MUTED); ax.set_ylabel("Ganho Médio Semanal (R$)",color=MUTED)
ax.set_title("Corridas × Ganho por Status",color=TEXT); ax.legend(fontsize=9)
ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)

plt.tight_layout(); plt.savefig("fig1 visao geral.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close()
print("✅ fig1 salva")

# ── FIG 2: Fatores ──────────────────────────────────────────
fig,axes=plt.subplots(1,3,figsize=(17,5)); fig.patch.set_facecolor(BG)
fig.suptitle("Fatores que Influenciam o Churn de Motoristas",fontsize=16,fontweight="bold",color=AMARELO)

ax=axes[0]; ax.set_facecolor(CARD)
motivos_count=df[df["churn"]==1]["motivo_saida"].value_counts()
cores_m=[AMARELO,AMBER,GOLD,CREAM+"cc",MUTED]
bars=ax.bar(range(len(motivos_count)),motivos_count.values,color=cores_m[:len(motivos_count)],edgecolor="none",width=0.6)
ax.set_xticks(range(len(motivos_count)))
ax.set_xticklabels(motivos_count.index,rotation=28,ha="right",fontsize=8.5,color=TEXT)
ax.set_ylabel("Nº de Motoristas",color=MUTED); ax.set_title("Motivos de Saída",color=TEXT)
ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)
for bar,val in zip(bars,motivos_count.values):
    ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+1,str(val),ha="center",fontsize=10,fontweight="bold",color=AMARELO)

ax=axes[1]; ax.set_facecolor(CARD)
bins=[0,400,600,800,1000,1800]; labels_ganho=["<400","400–600","600–800","800–1k",">1k"]
df["faixa_ganho"]=pd.cut(df["ganho_medio_semanal_r$"],bins=bins,labels=labels_ganho)
churn_ganho=df.groupby("faixa_ganho",observed=True)["churn"].mean()*100
cores_g=[VERMELHO if v>40 else AMBER if v>25 else AMARELO for v in churn_ganho.values]
bars=ax.bar(churn_ganho.index,churn_ganho.values,color=cores_g,edgecolor="none",width=0.6)
ax.set_xlabel("Ganho Médio Semanal (R$)",color=MUTED); ax.set_ylabel("Taxa de Churn (%)",color=MUTED)
ax.set_title("Churn por Faixa de Ganho",color=TEXT)
ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)
for bar,val in zip(bars,churn_ganho.values):
    ax.text(bar.get_x()+bar.get_width()/2,bar.get_height()+0.5,f"{val:.1f}%",ha="center",fontsize=10,fontweight="bold",color=TEXT)

ax=axes[2]; ax.set_facecolor(CARD)
bins_t=[0,3,6,12,24,36]; labels_t=["0–3m","3–6m","6–12m","12–24m","24–36m"]
df["faixa_tempo"]=pd.cut(df["tempo_plataforma_meses"],bins=bins_t,labels=labels_t)
churn_tempo=df.groupby("faixa_tempo",observed=True)["churn"].mean()*100
ax.fill_between(range(len(churn_tempo)),churn_tempo.values,alpha=0.18,color=AMARELO)
ax.plot(range(len(churn_tempo)),churn_tempo.values,color=AMARELO,linewidth=2.8,marker="o",markersize=9,
    markerfacecolor=BG,markeredgecolor=AMARELO,markeredgewidth=2.5)
ax.set_xticks(range(len(churn_tempo))); ax.set_xticklabels(churn_tempo.index,color=TEXT)
ax.set_ylabel("Taxa de Churn (%)",color=MUTED); ax.set_title("Churn por Tempo na Plataforma",color=TEXT)
ax.spines["left"].set_color(BORDER); ax.spines["bottom"].set_color(BORDER)
for i,val in enumerate(churn_tempo.values):
    ax.text(i,val+1.2,f"{val:.1f}%",ha="center",fontsize=9,fontweight="bold",color=TEXT)

plt.tight_layout(); plt.savefig("fig2 fatores churn.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close()
print("✅ fig2 salva")

# ── FIG 3: Correlação ────────────────────────────────────────
fig,ax=plt.subplots(figsize=(10,7)); fig.patch.set_facecolor(BG); ax.set_facecolor(CARD)
cols_num=["churn","avaliacao_media","ganho_medio_semanal_r$","corridas_por_semana",
          "cancelamentos_mes","tempo_plataforma_meses","suporte_acionado","bonus_recebido"]
corr=df[cols_num].corr()
labels_pt=["Churn","Avaliação","Ganho Sem.","Corridas/Sem.","Cancelamentos","Tempo Plataf.","Suporte","Bônus"]
mask=np.triu(np.ones_like(corr,dtype=bool))
cmap_99=LinearSegmentedColormap.from_list("99dark",[VERMELHO,"#2E2E2E",AMARELO])
sns.heatmap(corr,mask=mask,annot=True,fmt=".2f",cmap=cmap_99,center=0,ax=ax,
    xticklabels=labels_pt,yticklabels=labels_pt,linewidths=0.8,linecolor=BG,
    annot_kws={"size":10,"color":TEXT},cbar_kws={"shrink":0.75})
ax.set_xticklabels(ax.get_xticklabels(),color=TEXT,fontsize=9,rotation=35,ha="right")
ax.set_yticklabels(ax.get_yticklabels(),color=TEXT,fontsize=9,rotation=0)
ax.set_title("Correlação entre Variáveis e Churn",fontsize=14,fontweight="bold",color=AMARELO,pad=16)
ax.collections[0].colorbar.ax.yaxis.set_tick_params(color=MUTED)
plt.setp(ax.collections[0].colorbar.ax.yaxis.get_ticklabels(),color=MUTED)
plt.tight_layout(); plt.savefig("fig3 correlacao.png",dpi=150,bbox_inches="tight",facecolor=BG); plt.close()
print("✅ fig3 salva")
print("\n🎉 Todos os gráficos gerados!")
