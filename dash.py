import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_excel('COMISSAO.xlsx')

df["DATA_EMISSAO_NOTA"] = pd.to_datetime(df["DATA_EMISSAO_NOTA"])
df["DATA_ENTRADA_NOTA"] = pd.to_datetime(df["DATA_ENTRADA_NOTA"])
df["DATA_BAIXA"] = pd.to_datetime(df["DATA_BAIXA"])
df["DATA_CONTRATO"] = pd.to_datetime(df["DATA_CONTRATO"])

df["TOTAL_NOTA"] = pd.to_numeric(df["TOTAL_NOTA"])

df = df.sort_values("DATA_BAIXA")

df["Dt_Baixa"] = df["DATA_BAIXA"].apply(lambda x: str(x.day) + "/" + str(x.month) + "/" + str(x.year))
df["Mes"] = df["DATA_BAIXA"].apply(lambda x: str(x.month) + "/" + str(x.year))
date = st.sidebar.selectbox("Baixa", df['Mes'].unique())

# enterprise = st.sidebar.selectbox("Empreendimento", df['EMPREENDIMENTO'].unique())

df_filtred = df[df["Mes"] == date]
# df_filtred = df[df["EMPREENDIMENTO"] == enterprise]
df_filtred

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

fig_data = px.bar(df_filtred, x="EMPREENDIMENTO", y="TOTAL_NOTA", color="Dt_Baixa", barmode='group', title="Comissão por corretor")
col1.plotly_chart(fig_data)

fig_prod = px.bar(df_filtred, x="Dt_Baixa", y="EMPREENDIMENTO", color="TOTAL_NOTA", title="Status Baixa", orientation="h")
col2.plotly_chart(fig_prod)

enterprise_total = df_filtred.groupby("EMPREENDIMENTO")[["TOTAL_NOTA"]].sum().reset_index()
fig_enterprise = px.bar(enterprise_total, x="EMPREENDIMENTO", y="TOTAL_NOTA", title="Filial")
col3.plotly_chart(fig_enterprise)

payment_total = df_filtred.groupby("EMPREENDIMENTO")[["TOTAL_NOTA"]].sum().reset_index()
fig_kind = px.pie(payment_total, values="TOTAL_NOTA", names="EMPREENDIMENTO", title="Pagamento" )
col4.plotly_chart(fig_kind)
fig_kind.update_traces(textposition='inside', textinfo='percent+label')

# enterprise_total = df_filtred.groupby("EMPREENDIMENTO")[["TOTAL_NOTA"]].sum().reset_index()

