import streamlit as st
import yfinance as yf
import pandas as pd
import ta

# Función para descargar datos de yFinance


def load_data(ticker):
    data = yf.download(ticker, start="2022-01-01", end="2024-01-01")
    return data

# Función para agregar indicadores técnicos


def add_technical_indicators(data):
    if data.empty or 'Close' not in data.columns:
        st.error(
            "Error: El dataframe está vacío o la columna 'Close' no está presente.")
        return data

    # Añadir el indicador SMA de 20 días
    try:
        data['SMA_20'] = ta.trend.sma_indicator(data['Close'], window=20)
    except Exception as e:
        st.error(f"Error al calcular SMA_20: {e}")
        return data

    # Añadir el indicador RSI
    try:
        data['RSI'] = ta.momentum.rsi(data['Close'], window=14)
    except Exception as e:
        st.error(f"Error al calcular RSI: {e}")
        return data

    return data

# Función principal de la app Streamlit


def main():
    st.title("Stock Dashboard App")

    # Seleccionar el ticker
    ticker = st.text_input("Selecciona un ticker (ej. AAPL, MSFT):", "AAPL")

    # Cargar los datos
    if ticker:
        data = load_data(ticker)
        st.write(f"Datos cargados para: {ticker}")
        st.write(data.tail())

        # Agregar indicadores técnicos
        data = add_technical_indicators(data)

        # Mostrar los datos con indicadores
        if not data.empty:
            st.write("Datos con indicadores técnicos:")
            st.write(data.tail())
        else:
            st.error("No hay datos para mostrar.")


# Ejecutar la aplicación
if __name__ == "__main__":
    main()
