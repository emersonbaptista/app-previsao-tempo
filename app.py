import streamlit as st
import requests

# Configuração da página para navegação responsiva em dispositivos móveis
st.set_page_config(page_title="Previsão do Tempo", page_icon="🌤️", layout="centered")

st.title("🌤️ Previsão do Tempo")
st.write("Digite o local desejado para verificar o clima atual.")

# Campo de entrada
localizacao = st.text_input("Cidade, Estado ou País:", value="Bebedouro")

if st.button("Buscar Clima", type="primary"):
    if not localizacao.strip():
        st.warning("Por favor, digite um local válido.")
    else:
        api_key = st.secrets["API_KEY"]
        url = "http://api.weatherapi.com/v1/forecast.json"
        
        parametros = {
            "key": api_key,
            "q": localizacao,
            "lang": "pt",
            "aqi": "yes",
            "days": 1
        }

        try:
            resposta = requests.get(url, params=parametros)

            if resposta.status_code == 200:
                dados = resposta.json()

                # Informações do local
                st.markdown(f"### 📍 {dados['location']['name']}, {dados['location']['region']} - {dados['location']['country']}")
                st.divider()

                # Exibição dos dados em colunas
                col1, col2 = st.columns(2)
                col1.metric("Temperatura", f"{dados['current']['temp_c']} °C")
                col2.metric("Sensação Térmica", f"{dados['current']['feelslike_c']} °C")

                col3, col4 = st.columns(2)
                col3.metric("Umidade", f"{dados['current']['humidity']} %")
                col4.metric("Vento", f"{dados['current']['wind_kph']} km/h")

                st.info(f"**Condição:** {dados['current']['condition']['text']}")
            else:
                st.error("Não foi possível encontrar este local. Verifique a digitação.")
        except Exception as e:
            st.error("Erro ao conectar com a API de clima.")