import streamlit as st
import requests

st.set_page_config(page_title="Previsão do Tempo", page_icon="🌤️", layout="centered")

st.title("🌤️ Previsão do Tempo Completa")
st.write("Digite o local desejado para verificar o clima atual e a previsão.")

# Entrada da cidade
cidade = st.text_input("Cidade, Estado ou País:", "Bebedouro")

if st.button("Buscar Clima"):
    if cidade:
        try:
            # Chave guardada no st.secrets
            api_key = st.secrets["API_KEY"]
            
            # Endpoint de forecast para obter previsão de 3 dias, qualidade do ar e dados astronômicos
            url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={cidade}&days=3&aqi=yes&lang=pt"
            
            resposta = requests.get(url)
            dados = resposta.json()

            if resposta.status_code == 200:
                # 1. Informações Básicas da Localização
                nome_cidade = dados["location"]["name"]
                estado = dados["location"]["region"]
                pais = dados["location"]["country"]
                
                st.subheader(f"📍 {nome_cidade}, {estado} - {pais}")
                
                # 2. Clima Atual
                atual = dados["current"]
                temp_atual = atual["temp_c"]
                sensacao = atual["feelslike_c"]
                umidade = atual["humidity"]
                vento = atual["wind_kph"]
                condicao = atual["condition"]["text"]
                icone_atual = "https:" + atual["condition"]["icon"]
                
                # Dados Extras: Saúde & Visibilidade
                uv = atual.get("uv", "N/A")
                visibilidade = atual.get("vis_km", "N/A")
                
                col_img, col_info = st.columns([1, 4])
                with col_img:
                    st.image(icone_atual, width=80)
                with col_info:
                    st.markdown(f"**Condição:** {condicao.capitalize()}")

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Temperatura", f"{temp_atual} °C")
                col2.metric("Sensação", f"{sensacao} °C")
                col3.metric("Umidade", f"{umidade} %")
                col4.metric("Vento", f"{vento} km/h")
                
                st.divider()

                # 3. Informações de Saúde e Astronomia (Hoje)
                st.subheader("💡 Informações de Saúde e Astronomia")
                
                astronomia = dados["forecast"]["forecastday"][0]["astro"]
                nascer_sol = astronomia["sunrise"]
                por_sol = astronomia["sunset"]
                fase_lua = astronomia["moon_phase"]

                col_s1, col_s2, col_s3, col_s4 = st.columns(4)
                col_s1.metric("Índice UV", uv)
                col_s2.metric("Visibilidade", f"{visibilidade} km")
                col_s3.metric("Nascer do Sol", nascer_sol)
                col_s4.metric("Pôr do Sol", por_sol)
                
                st.info(f"🌔 **Fase da Lua:** {fase_lua}")

                st.divider()

                # 4. Previsão para os Próximos Dias
                st.subheader("📅 Previsão para os Próximos Dias")
                
                dias = dados["forecast"]["forecastday"]
                cols_dias = st.columns(len(dias))

                for i, dia in enumerate(dias):
                    data_fmt = dia["date"]
                    max_temp = dia["day"]["maxtemp_c"]
                    min_temp = dia["day"]["mintemp_c"]
                    chance_chuva = dia["day"]["daily_chance_of_rain"]
                    cond_dia = dia["day"]["condition"]["text"]
                    icone_dia = "https:" + dia["day"]["condition"]["icon"]

                    with cols_dias[i]:
                        st.markdown(f"**{data_fmt}**")
                        st.image(icone_dia, width=50)
                        st.caption(f"{cond_dia.capitalize()}")
                        st.write(f"🌡️ **Max:** {max_temp}°C")
                        st.write(f"❄️ **Min:** {min_temp}°C")
                        st.write(f"🌧️ **Chuva:** {chance_chuva}%")

            else:
                st.error("Cidade não encontrada. Verifique o nome digitado.")

        except Exception as e:
            st.error("Erro ao conectar com o serviço de clima. Verifique sua chave de API nos Secrets.")
    else:
        st.warning("Por favor, digite o nome de uma cidade.")