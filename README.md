# 📊 Dashboard de Vendas - Comercial

Este projeto é um painel interativo desenvolvido com [Streamlit](https://streamlit.io/) para análise de desempenho comercial. Ele permite visualizar métricas de vendas, aplicar filtros dinâmicos, editar dados diretamente na interface e exportar relatórios em Excel.

---

## 🚀 Funcionalidades

- Exibição de **logo da empresa personalizada** no topo da interface
- Filtros por **produto**, **região**, **canal** e **período**
- Indicadores de desempenho:
  - Faturamento Total
  - Ticket Médio
  - Total de Visitas
  - Taxa de Conversão
- Gráficos interativos:
  - Vendas por Produto
  - Vendas por Região
  - Faturamento por Mês
  - Metas vs Resultados
- Editor de dados integrado
- Exportação dos dados filtrados em formato `.xlsx`

---

## 🖼️ Exemplo da Interface

Abaixo está uma prévia da dashboard em funcionamento:

<img width="1832" height="988" alt="image" src="https://github.com/user-attachments/assets/a238c49b-800a-4074-bc8f-8ebe019c5c72" />



## 🧰 Tecnologias utilizadas

- Python 3.13+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- XlsxWriter

---


## 📦 Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/dashboard-comercial.git
   cd dashboard-comercial
pip install -r requirements.txt

streamlit run App.py
