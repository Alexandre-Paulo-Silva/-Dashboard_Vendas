import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import io  # Adicionado para exportar como Excel

# Configurações iniciais
st.set_page_config(page_title="Dashboard Comercial", layout="wide")
st.title("📊 Dashboard de Vendas - Comercial ")

# Estilo visual
st.markdown("""
    <style>
    body, .stApp {
        background-color: #0f2c5c;
        color: white;
    }
    label, .stMultiSelect label, .stSlider label, .stSelectbox label {
        color: white !important;
        font-weight: bold !important;
    }
    div[data-baseweb="select"] * {
        color: white !important;
    }
    .stSlider .css-1y4p8pa {
        color: white !important;
    }
    .stMetric label {
        color: white !important;
    }
    #MainMenu {display: none;}
    header {display: none;}
    footer {display: none;}
    </style>
""", unsafe_allow_html=True)

# Carregar dados com proteção
try:
    df = pd.read_csv("equiv.csv", sep=",", parse_dates=["Data"])
    if df.empty:
        st.error("O arquivo 'equiv.csv' está vazio. Verifique o conteúdo.")
        st.stop()
except FileNotFoundError:
    st.error("Arquivo 'equiv.csv' não encontrado. Coloque o arquivo na mesma pasta do script.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao carregar o arquivo: {e}")
    st.stop()

# Filtros e editor dentro da barra lateral
with st.sidebar:
    st.header("🎯 Filtros")
    produtos = st.multiselect("Produto", df["Produto"].unique(), default=df["Produto"].unique())
    regioes = st.multiselect("Região", df["Região"].unique(), default=df["Região"].unique())
    canais = st.multiselect("Canal", df["Canal"].unique(), default=df["Canal"].unique())
    datas = st.date_input("Período", [df["Data"].min(), df["Data"].max()])

    # Botão para abrir editor
    abrir_editor = st.toggle("📂 Editor de Dados")

    if abrir_editor:
        st.markdown("### ✏️ Editar Dados")
        df_editado = st.data_editor(df, num_rows="dynamic", use_container_width=True)

        if st.button("💾 Salvar alterações"):
            try:
                df_editado.to_csv("equiv.csv", index=False, sep=",", encoding="utf-8")
                st.success("Arquivo atualizado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

# Proteção contra seleção incompleta de datas
if isinstance(datas, (list, tuple)) and len(datas) == 2:
    data_inicio, data_fim = pd.to_datetime(datas[0]), pd.to_datetime(datas[1])
elif isinstance(datas, (list, tuple)) and len(datas) == 1:
    data_inicio = data_fim = pd.to_datetime(datas[0])
else:
    data_inicio = data_fim = pd.to_datetime(datas)

# Aplicar filtros
df_filtrado = df[
    (df["Produto"].isin(produtos)) &
    (df["Região"].isin(regioes)) &
    (df["Canal"].isin(canais)) &
    (df["Data"].between(data_inicio, data_fim))
]

# KPIs
total_vendas = df_filtrado["Vendas"].sum()
total_visitas = df_filtrado["Visitas"].sum()
ticket_medio = total_vendas / len(df_filtrado) if len(df_filtrado) > 0 else 0
taxa_conversao = (total_vendas / total_visitas * 100) if total_visitas > 0 else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Faturamento Total", f"R$ {total_vendas:,.2f}")
col2.metric("🛒 Ticket Médio", f"R$ {ticket_medio:,.2f}")
col3.metric("👥 Visitas", f"{total_visitas:,}")
col4.metric("⚡ Taxa de Conversão", f"{taxa_conversao:.2f}%")

# Gráficos lado a lado: Produto e Região
col5, col6 = st.columns(2)

with col5:
    st.subheader("📦 Vendas por Produto")
    vendas_produto = df_filtrado.groupby("Produto")["Vendas"].sum().reset_index()
    if not vendas_produto.empty:
        fig2, ax2 = plt.subplots(figsize=(5, 3))
        sns.barplot(data=vendas_produto, x="Produto", y="Vendas", palette="Blues", ax=ax2)
        ax2.set_ylabel("Vendas (R$)")
        st.pyplot(fig2)
    else:
        st.warning("Sem dados para o gráfico de Vendas por Produto.")

with col6:
    st.subheader("🌍 Vendas por Região")
    vendas_regiao = df_filtrado.groupby("Região")["Vendas"].sum().reset_index()
    if not vendas_regiao.empty:
        fig3, ax3 = plt.subplots(figsize=(5, 3))
        sns.barplot(data=vendas_regiao, x="Região", y="Vendas", palette="Greens", ax=ax3)
        ax3.set_ylabel("Vendas (R$)")
        st.pyplot(fig3)
    else:
        st.warning("Sem dados para o gráfico de Vendas por Região.")

# Gráficos lado a lado: Faturamento por Mês e Metas vs Resultados
col7, col8 = st.columns(2)

with col7:
    st.subheader("📆 Faturamento por Mês")
    df_mes = df_filtrado.copy()
    df_mes["Mês"] = df_mes["Data"].dt.to_period("M").astype(str)
    vendas_mes = df_mes.groupby("Mês")["Vendas"].sum().reset_index()
    if not vendas_mes.empty:
        fig1, ax1 = plt.subplots(figsize=(5, 3))
        sns.lineplot(data=vendas_mes, x="Mês", y="Vendas", marker="o", ax=ax1)
        ax1.set_ylabel("Faturamento (R$)")
        ax1.set_xlabel("Mês")
        st.pyplot(fig1)
    else:
        st.warning("Sem dados para o gráfico de Faturamento por Mês.")

with col8:
    st.subheader("🎯 Metas vs Resultados")
    df_comparativo = df_filtrado.groupby("Produto")[["Vendas", "Meta"]].sum().reset_index()
    if not df_comparativo.empty:
        fig4, ax4 = plt.subplots(figsize=(5, 3))
        df_comparativo.plot(kind="bar", x="Produto", ax=ax4)
        ax4.set_ylabel("Valor (R$)")
        ax4.set_title("Comparativo por Produto")
        st.pyplot(fig4)
    else:
        st.warning("Sem dados para o gráfico de Metas vs Resultados.")

# Tabela final
st.subheader("🔍 Dados Detalhados")
st.dataframe(df_filtrado)

# Exportar como Excel
if not df_filtrado.empty:
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name="Vendas")
    st.download_button(
        label="📥 Baixar Excel",
        data=buffer.getvalue(),
        file_name="vendas_filtradas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.warning("Nenhum dado disponível para exportar com os filtros atuais.")

# Rodapé
st.markdown("---")
st.caption("Desenvolvido por Alexandre • Case Comercial Amazonas • Powered by Streamlit & Pandas")