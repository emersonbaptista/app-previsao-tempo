import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Previsão do Tempo", page_icon="🌤️", layout="centered")

st.title("🌤️ Previsão do Tempo Completa")
st.write("Digite o local desejado para verificar o clima atual, alertas e previsão.")

# Entrada da cidade
cidade = st.text_input("Cidade, Estado ou País:", "Bebedouro")

if st.button("Buscar Clima"):
    if cidade:
        try:
            # Chave guardada no st.secrets
            api_key = st.secrets["API_KEY"]
            
            # Endpoint com aqi=yes (Qualidade do ar) e alerts=yes (Alertas oficiais)
            url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={cidade}&days=3&aqi=yes&alerts=yes&lang=pt"
            
            resposta = requests.get(url)
            dados = resposta.json()

            if resposta.status_code == 200:
                # 1. Localização
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
                direcao_vento = atual.get("wind_dir", "N/A")
                rajada_vento = atual.get("gust_kph", "N/A")
                condicao = atual["condition"]["text"]
                icone_atual = "https:" + atual["condition"]["icon"]
                
                # Probabilidade de Chuva do Dia de Hoje
                chance_chuva_hoje = dados["forecast"]["forecastday"][0]["day"]["daily_chance_of_rain"]
                
                uv = atual.get("uv", "N/A")
                visibilidade = atual.get("vis_km", "N/A")
                
                # Exibição do topo (Ícone e condição)
                col_img, col_info = st.columns([1, 4])
                with col_img:
                    st.image(icone_atual, width=80)
                with col_info:
                    st.markdown(f"**Condição:** {condicao.capitalize()}")

                # Métricas Principais (4 Colunas)
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Temperatura", f"{temp_atual} °C")
                col2.metric("Sensação", f"{sensacao} °C")
                col3.metric("Umidade", f"{umidade} %")
                col4.metric("Vento", f"{vento} km/h")
                
                # Linha 2 de Detalhes (Direção, Rajada e Chuva)
                c_v1, c_v2, c_v3 = st.columns(3)
                with c_v1:
                    st.metric("Direção do Vento", direcao_vento)
                with c_v2:
                    st.metric("Rajada Máxima", f"{rajada_vento} km/h")
                with c_v3:
                    st.metric("Chance de Chuva", f"{chance_chuva_hoje} %")

                st.divider()

                # 3. Alertas Meteorológicos Oficiais
                alertas = dados.get("alerts", {}).get("alert", [])
                if alertas:
                    st.subheader("⚠️ Alertas Meteorológicos Oficiais")
                    for alerta in alertas:
                        evento = alerta.get("event", "Alerta Meteorológico")
                        descricao = alerta.get("headline", "Sem detalhes disponíveis.")
                        st.error(f"**{evento}**: {descricao}")
                    st.divider()

                # 4. Qualidade do Ar Completa (Poluentes)
                st.subheader("🍃 Qualidade do Ar e Poluentes")
                aqi = atual.get("air_quality", {})
                if aqi:
                    co = round(aqi.get("co", 0), 1)
                    no2 = round(aqi.get("no2", 0), 1)
                    o3 = round(aqi.get("o3", 0), 1)
                    pm2_5 = round(aqi.get("pm2_5", 0), 1)
                    pm10 = round(aqi.get("pm10", 0), 1)

                    col_aq1, col_aq2, col_aq3, col_aq4, col_aq5 = st.columns(5)
                    col_aq1.metric("CO", f"{co} µg/m³")
                    col_aq2.metric("NO₂", f"{no2} µg/m³")
                    col_aq3.metric("O₃", f"{o3} µg/m³")
                    col_aq4.metric("PM2.5", f"{pm2_5} µg/m³")
                    col_aq5.metric("PM10", f"{pm10} µg/m³")
                else:
                    st.info("Dados de qualidade do ar não disponíveis para esta localização.")

                st.divider()

                # 5. Informações de Saúde e Astronomia
                st.subheader("💡 Saúde e Astronomia")
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

                # 6. Previsão para os Próximos Dias (Data em Formato BR)
                st.subheader("📅 Previsão para os Próximos Dias")
                dias = dados["forecast"]["forecastday"]
                cols_dias = st.columns(len(dias))

                for i, dia in enumerate(dias):
                    # Conversão de AAAA-MM-DD para DD/MM/AAAA
                    data_obj = datetime.strptime(dia["date"], "%Y-%m-%d")
                    data_fmt = data_obj.strftime("%d/%m/%Y")
                    
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
            st.error("Erro ao conectar com o serviço de clima. Verifique suas configurações de API.")
    else:
        st.warning("Por favor, digite o nome de uma cidade.")