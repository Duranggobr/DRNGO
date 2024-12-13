import streamlit as st
import pandas as pd
import plotly.express as px
import base64
from io import BytesIO

def calcular_investimentos(investimento_inicial, aporte_mensal, periodo, selic, cdi, ipca, taxa_custodia, taxa_admin, imposto_renda):
    resultados = []

    total_investido = investimento_inicial + (aporte_mensal * periodo)

    # LCI e LCA (isento de IR)
    lci_lca = total_investido * (1 + cdi * 0.85)**(periodo / 12)
    rentabilidade_lci_lca = ((lci_lca - total_investido) / total_investido) * 100
    resultados.append(("LCI e LCA", lci_lca, rentabilidade_lci_lca, "Baixo"))

    # CDB
    cdb_bruto = total_investido * (1 + cdi)**(periodo / 12)
    cdb_liquido = cdb_bruto * (1 - imposto_renda)
    rentabilidade_cdb = ((cdb_liquido - total_investido) / total_investido) * 100
    resultados.append(("CDB", cdb_liquido, rentabilidade_cdb, "Médio"))

    # Tesouro Selic
    selic_bruto = total_investido * (1 + selic)**(periodo / 12) - (total_investido * taxa_custodia)
    selic_liquido = selic_bruto * (1 - imposto_renda)
    rentabilidade_selic = ((selic_liquido - total_investido) / total_investido) * 100
    resultados.append(("Tesouro Selic", selic_liquido, rentabilidade_selic, "Baixo"))

    # Fundo DI
    fundo_di_bruto = total_investido * (1 + cdi * 0.9817)**(periodo / 12) - (total_investido * taxa_admin)
    fundo_di_liquido = fundo_di_bruto * (1 - imposto_renda)
    rentabilidade_fundo_di = ((fundo_di_liquido - total_investido) / total_investido) * 100
    resultados.append(("Fundo DI", fundo_di_liquido, rentabilidade_fundo_di, "Médio"))

    # Tesouro Prefixado
    prefixado_bruto = total_investido * (1 + selic)**(periodo / 12) - (total_investido * taxa_custodia)
    prefixado_liquido = prefixado_bruto * (1 - imposto_renda)
    rentabilidade_prefixado = ((prefixado_liquido - total_investido) / total_investido) * 100
    resultados.append(("Tesouro Prefixado", prefixado_liquido, rentabilidade_prefixado, "Médio"))

    # Tesouro IPCA+
    ipca_bruto = total_investido * (1 + ipca + 0.055)**(periodo / 12) - (total_investido * taxa_custodia)
    ipca_liquido = ipca_bruto * (1 - imposto_renda)
    rentabilidade_ipca = ((ipca_liquido - total_investido) / total_investido) * 100
    resultados.append(("Tesouro IPCA+", ipca_liquido, rentabilidade_ipca, "Baixo"))

    # Poupança
    poupanca = total_investido * (1 + 0.006091)**periodo
    rentabilidade_poupanca = ((poupanca - total_investido) / total_investido) * 100
    resultados.append(("Poupança", poupanca, rentabilidade_poupanca, "Baixo"))

    return resultados, total_investido

def download_link(object_to_download, download_filename, download_link_text):
    """Generates a link to download the given object_to_download."""
    if isinstance(object_to_download, pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

# Interface com Streamlit
st.title("Calculadora de Investimentos")
st.markdown(
    "<style>.stButton>button {background-color: #6200ea; color: white; border-radius: 5px;} body {background-color: #f9f9f9;}</style>",
    unsafe_allow_html=True
)

# Entradas do usuário
investimento_inicial = st.number_input("Investimento Inicial (R$):", value=10000.0, format="%.2f")
aporte_mensal = st.number_input("Aporte Mensal (R$):", value=3000.0, format="%.2f")
periodo = st.number_input("Período (meses):", value=12, step=1)
selic = st.number_input("Selic (% a.a.):", value=11.15) / 100
cdi = st.number_input("CDI (% a.a.):", value=11.15) / 100
ipca = st.number_input("IPCA (% a.a.):", value=4.64) / 100
taxa_custodia = st.number_input("Taxa de Custódia (%):", value=0.20) / 100
taxa_admin = st.number_input("Taxa de Administração (%):", value=0.25) / 100
imposto_renda = st.number_input("Imposto de Renda (% sobre lucro):", value=15.0) / 100

if st.button("Calcular"):
    resultados, total_investido = calcular_investimentos(
        investimento_inicial, aporte_mensal, periodo, selic, cdi, ipca, taxa_custodia, taxa_admin, imposto_renda
    )

    # Exibição dos resultados
    st.subheader("Resultados")
    st.write(f"Total Investido: R$ {total_investido:,.2f}")

    # Criando um DataFrame para exibição e análise
    df_resultados = pd.DataFrame(resultados, columns=["Investimento", "Valor Líquido", "Rentabilidade Líquida (%)", "Risco"])
    df_resultados["Valor Líquido"] = df_resultados["Valor Líquido"].apply(lambda x: f"R$ {float(x):,.2f}")
    df_resultados["Rentabilidade Líquida (%)"] = df_resultados["Rentabilidade Líquida (%)"].apply(lambda x: f"{float(x):.2f}%")
    st.table(df_resultados)

    # Identificando o investimento mais vantajoso
    melhor_investimento = max(resultados, key=lambda x: x[2])
    st.markdown(
        f"### Melhor investimento: **{melhor_investimento[0]}** com rentabilidade líquida de **{melhor_investimento[2]:.2f}%**"
    )

    # Gráfico de barras interativo
    st.subheader("Comparativo de Rentabilidade")
    df_chart = pd.DataFrame(
        {
            "Investimentos": [r[0] for r in resultados],
            "Rentabilidade Líquida (%)": [r[2] for r in resultados],
        }
    )
    fig = px.bar(
        df_chart,
        x="Investimentos",
        y="Rentabilidade Líquida (%)",
        color="Investimentos",
        title="Rentabilidade por Tipo de Investimento",
        text_auto=True,
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig)

    # Exportar resultados
    csv_link = download_link(df_resultados, "resultados_investimentos.csv", "Baixar Resultados em CSV")
    st.markdown(csv_link, unsafe_allow_html=True)

# Seção Educativa
st.sidebar.header("Educação Financeira")
st.sidebar.markdown(
    """
    **Tipos de Investimentos:**
    - **LCI/LCA:** Isentos de IR, risco baixo, atrelados ao CDI.
    - **CDB:** Tributados, maior risco que LCI, atrelados ao CDI.
    - **Tesouro Selic:** Renda fixa, seguro, acompanha a taxa Selic.
    - **Tesouro IPCA+:** Proteção contra inflação, rendimento acima do IPCA.
    - **Fundo DI:** Rentabilidade variável, taxa de administração aplicada.
    - **Poupança:** Rendimento baixo, isento de IR.
    """
)
