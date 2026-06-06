# 🚖 Análise de Retenção de Motoristas — Contexto 99

Projeto de análise de dados com foco em **retenção de motoristas parceiros** em plataformas de ride hailing.

-----

## 📌 Contexto

Empresas de ride hailing como a 99 dependem diretamente da disponibilidade de motoristas parceiros para garantir a qualidade do serviço. Manter esses parceiros ativos e engajados é um dos principais desafios operacionais do setor.

**Pergunta central do projeto:**

> O que faz um motorista abandonar a plataforma?

-----

## 🎯 Objetivo

Identificar os principais fatores associados ao **churn** (inatividade) de motoristas, gerando insumos para ações de retenção baseadas em dados.

-----

## 📊 Sobre os dados

Os dados utilizados são **simulados** com base no contexto real do mercado de ride hailing no Brasil. Foram criados 1.200 registros de motoristas com as seguintes variáveis:

|Variável                |Descrição                                                   |
|------------------------|------------------------------------------------------------|
|`cidade`                |Cidade de operação (SP, RJ, BH, Curitiba, Fortaleza, Recife)|
|`tempo_plataforma_meses`|Tempo de cadastro na plataforma                             |
|`corridas_por_semana`   |Frequência média de corridas                                |
|`avaliacao_media`       |Nota média recebida dos passageiros (1–5)                   |
|`ganho_medio_semanal_r$`|Ganho médio semanal em reais                                |
|`cancelamentos_mes`     |Média de cancelamentos no mês                               |
|`suporte_acionado`      |Se o motorista já abriu chamado no suporte                  |
|`bonus_recebido`        |Se recebeu bônus da plataforma no período                   |
|`churn`                 |**Variável alvo** — 1 = inativo, 0 = ativo                  |


> ⚠️ *Dados simulados exclusivamente para fins de portfólio.*

-----

## 🔍 Principais achados

|Fator                          |Impacto no Churn                               |
|-------------------------------|-----------------------------------------------|
|Ganho semanal abaixo de R$ 500 |Alto — principal driver de saída               |
|Menos de 3 corridas por semana |Alto — baixo engajamento prediz inatividade    |
|Primeiros 6 meses na plataforma|Período crítico — maior taxa de abandono       |
|Recebimento de bônus           |Protetor — reduz significativamente o churn    |
|Avaliação média abaixo de 4.0  |Moderado — motoristas mal avaliados saem mais  |
|Suporte acionado               |Moderado — indica insatisfação com a plataforma|



## 💡 Recomendações de negócio

1. **Onboarding reforçado** nos primeiros 6 meses — período de maior risco
1. **Alertas proativos** para motoristas com ganho semanal abaixo de R$ 500
1. **Política de bônus** como alavanca de retenção
1. **Melhoria no fluxo de suporte** — quem aciona suporte tem maior propensão ao churn



## 🗂️ Arquivos do projeto

```
📁 retencao-motoristas-99/
├── retencao_motoristas_99.ipynb   # Notebook principal com toda a análise
├── dataset_motoristas_99.csv      # Dataset simulado
├── fig1_visao_geral.png           # Painel geral: distribuição, avaliação, cidade, corridas
├── fig2_fatores_churn.png         # Motivos de saída, faixa de ganho, tempo na plataforma
└── fig3_correlacao.png            # Heatmap de correlação entre variáveis
```


## 🛠️ Ferramentas Utilizadas

| Categoria | Ferramenta | Uso |
|-----------|-----------|-----|
| Linguagem | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) | Desenvolvimento completo |
| Dados | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) | Manipulação e análise |
| Numérico | ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) | Cálculos estatísticos |
| Visualização | ![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat&logo=python&logoColor=white) | Gráficos e painéis |
| Visualização | ![Seaborn](https://img.shields.io/badge/Seaborn-4C72B0?style=flat&logo=python&logoColor=white) | Heatmap e distribuições |
| Ambiente | ![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=flat&logo=jupyter&logoColor=white) | Notebook interativo |
| Versionamento | ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) | Controle de versão |
| Repositório | ![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white) | Hospedagem do projeto |

---



## 👩‍💻 Sobre

Projeto desenvolvido por **Yasmin Guedes** como parte do portfólio de área de dados.  
Conecte-se comigo no LinkedIn (linkedin.com/in/yasmin-guedes-0101)
