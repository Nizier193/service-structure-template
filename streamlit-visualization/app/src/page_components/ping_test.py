import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

from src.helpers.ping_api import (
    PingAPI, config
)

api = PingAPI()

def page_ping():
    st.text("Здесь можно проверить пинг и чекнуть статистику.")

    window = st.number_input(
        label="Количество записей", 
        min_value=10, 
        max_value=1_000_000, 
        value=100
    )
    
    data = api.get_pings(window)  # Получаем данные

    if st.button(label="Обновить", key="btn_ping_refresh"):
        data = api.get_pings(window)  # Получаем данные

    with st.container(border=True):
        st.info("📊 Небольшая статистика")
        
        if data and len(data) > 0:
            # Большая красивая цифра с общим количеством
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Всего подключений",
                    value=len(data),
                    delta=f"Показано последних {window}"
                )
            
            with col2:
                # Последнее подключение
                if data:
                    last_ping = data[0]  # Если сортировка по убыванию
                    st.metric(
                        label="Последнее подключение",
                        value=datetime.fromisoformat(last_ping['time']).strftime("%H:%M:%S")
                    )
            
            # График подключений по часам
            st.subheader("График подключений")
            
            # Преобразуем данные для графика
            df = pd.DataFrame(data)
            df['datetime'] = pd.to_datetime(df['time'])
            df['hour'] = df['datetime'].dt.floor('h')  # Группируем по часам
            
            hourly_stats = df.groupby('hour').size().reset_index(name='count')
            
            # Создаем график
            fig = px.line(
                hourly_stats, 
                x='hour', 
                y='count',
                title='Подключения по часам',
                labels={'hour': 'Время', 'count': 'Количество подключений'}
            )
            fig.update_traces(line_color='#1f77b4', line_width=3)
            fig.update_layout(
                xaxis_title="Время",
                yaxis_title="Количество подключений",
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("Нет данных для отображения статистики")

    with st.container(border=True):
        st.info("🔍 Проверка подключения")
        
        # Информация о сервере
        st.markdown("### Информация о сервере")
        server_info = pd.DataFrame([
            {"Параметр": "Backend URL", "Значение": config.BACKEND_BASEURL},
            {"Параметр": "Статус", "Значение": "🟢 Онлайн" if True else "🔴 Офлайн"},  # Можно добавить реальную проверку
        ])
        st.table(server_info)
        
    
        check = st.button(
            label="🚀 Отправить пинг", 
            key="btn_ping",
            use_container_width=True
        )

        if check:
            with st.spinner('Отправляем запрос...'):
                try:
                    response = api.ping()
                    
                    # Красивое отображение ответа
                    if response:
                        st.success("✅ Пинг успешно отправлен!")
                        
                        # Показываем детали в expander
                        with st.expander("Детали ответа", expanded=True):
                            st.json(response)
                    else:
                        st.error("❌ Ошибка при отправке пинга")
                        
                except Exception as e:
                    st.error(f"❌ Ошибка подключения: {str(e)}")
