import streamlit as st

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

    return resultados


# Interface do Streamlit
st.title("Calculadora de Investimentos")

# Entradas do usuário
investimento_inicial = st.number_input("Investimento Inicial (R$):", value=10000.0)
aporte_mensal = st.number_input("Aporte Mensal (R$):", value=3000.0)
periodo = st.number_input("Período (meses):", value=12, step=1)
selic = st.number_input("Selic (% a.a.):", value=11.15) / 100
cdi = st.number_input("CDI (% a.a.):", value=11.15) / 100
ipca = st.number_input("IPCA (% a.a.):", value=4.64) / 100
taxa_custodia = st.number_input("Taxa de Custódia (%):", value=0.20) / 100
taxa_admin = st.number_input("Taxa de Administração (%):", value=0.25) / 100

if st.button("Calcular"):
    resultados = calcular_investimentos(investimento_inicial, aporte_mensal, periodo, selic, cdi, ipca, taxa_custodia, taxa_admin)

    # Exibição dos resultados
    st.subheader("Resultados")
    st.write("Total Investido: R$ {:.2f}".format(investimento_inicial + (aporte_mensal * periodo)))
    st.table(resultados)
