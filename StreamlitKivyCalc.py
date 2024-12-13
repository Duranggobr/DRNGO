import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calcular_investimentos(investimento_inicial, aporte_mensal, periodo, selic, cdi, ipca, taxa_custodia, taxa_admin):
    resultados = []

    total_investido = investimento_inicial + (aporte_mensal * periodo)

    # LCI e LCA
    lci_lca = total_investido * (1 + cdi * 0.85)**(periodo / 12)
    rentabilidade_lci_lca = ((lci_lca - total_investido) / total_investido) * 100
    resultados.append(("LCI e LCA", lci_lca, rentabilidade_lci_lca))

    # CDB
    cdb = total_investido * (1 + cdi)**(periodo / 12)
    rentabilidade_cdb = ((cdb - total_investido) / total_investido) * 100
    resultados.append(("CDB", cdb, rentabilidade_cdb))

    # Tesouro Selic
    selic_total = total_investido * (1 + selic)**(periodo / 12) - (total_investido * taxa_custodia)
    rentabilidade_selic = ((selic_total - total_investido) / total_investido) * 100
    resultados.append(("Tesouro Selic", selic_total, rentabilidade_selic))

    # Fundo DI
    fundo_di = total_investido * (1 + cdi * 0.9817)**(periodo / 12) - (total_investido * taxa_admin)
    rentabilidade_fundo_di = ((fundo_di - total_investido) / total_investido) * 100
    resultados.append(("Fundo DI", fundo_di, rentabilidade_fundo_di))

    # Tesouro Prefixado
    tesouro_prefixado = total_investido * (1 + selic)**(periodo / 12) - (total_investido * taxa_custodia)
    rentabilidade_prefixado = ((tesouro_prefixado - total_investido) / total_investido) * 100
    resultados.append(("Tesouro Prefixado", tesouro_prefixado, rentabilidade_prefixado))

    # Tesouro IPCA+
    tesouro_ipca = total_investido * (1 + ipca + 0.055)**(periodo / 12) - (total_investido * taxa_custodia)
    rentabilidade_ipca = ((tesouro_ipca - total_investido) / total_investido) * 100
    resultados.append(("Tesouro IPCA+", tesouro_ipca, rentabilidade_ipca))

    # Poupança
    poupanca = total_investido * (1 + 0.006091)**periodo
    rentabilidade_poupanca = ((poupanca - total_investido) / total_investido) * 100
    resultados.append(("Poupança", poupanca, rentabilidade_poupanca))

    return resultados, total_investido

# Interface com Streamlit
st.title("Calculadora de Investimentos")
st.markdown("<style>.stButton>button {background-color: #6200ea; color: white; border-radius: 5px;} </style>", unsafe_allow_html=True)

# Entradas do usuário
investimento_inicial = st.number_input("Investimento Inicial (R$):", value=10000.0, format="%.2f")
aporte_mensal = st.number_input("Aporte Mensal (R$):", value=3000.0, format="%.2f")
periodo = st.number_input("Período (meses):", value=12, step=1)
selic = st.number_input("Selic (% a.a.):", value=11.15) / 100
cdi = st.number_input("CDI (% a.a.):", value=11.15) / 100
ipca = st.number_input("IPCA (% a.a.):", value=4.64) / 100
taxa_custodia = st.number_input("Taxa de Custódia (%):", value=0.20) / 100
taxa_admin = st.number_input("Taxa de Administração (%):", value=0.25) / 100

if st.button("Calcular"):
    resultados, total_investido = calcular_investimentos(
        investimento_inicial, aporte_mensal, periodo, selic, cdi, ipca, taxa_custodia, taxa_admin
    )

    # Exibição dos resultados
    st.subheader("Resultados")
    st.write(f"Total Investido: R$ {total_investido:,.2f}")

    # Criando um DataFrame para exibição e análise
    df_resultados = pd.DataFrame(resultados, columns=["Investimento", "Valor Líquido", "Rentabilidade Líquida (%)"])
    df_resultados["Valor Líquido"] = df_resultados["Valor Líquido"].apply(lambda x: f"R$ {float(x):,.2f}")
    df_resultados["Rentabilidade Líquida (%)"] = df_resultados["Rentabilidade Líquida (%)"].apply(lambda x: f"{float(x):.2f}%")
    st.table(df_resultados)

    # Identificando o investimento mais vantajoso
    melhor_investimento = max(resultados, key=lambda x: x[2])
    st.markdown(
        f"### Melhor investimento: **{melhor_investimento[0]}** com rentabilidade líquida de **{melhor_investimento[2]:.2f}%**"
    )

    # Gráfico de barras
    st.subheader("Comparativo de Rentabilidade")
    fig, ax = plt.subplots(figsize=(10, 5))
    investimentos = [r[0] for r in resultados]
    rentabilidades = [r[2] for r in resultados]
    ax.bar(investimentos, rentabilidades, color="#6200ea")
    ax.set_ylabel("Rentabilidade Líquida (%)")
    ax.set_xlabel("Investimentos")
    ax.set_title("Rentabilidade por Tipo de Investimento")
    plt.xticks(rotation=45, ha="right")  # Melhora a legibilidade dos rótulos no eixo X
    st.pyplot(fig)
