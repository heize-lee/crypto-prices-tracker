import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import pyupbit

import datetime

import requests
from bs4 import BeautifulSoup

#wide
st.set_page_config(layout="wide")

#title
st.markdown("<h1 style='text-align: center;'>코인 OHLCV 데이터 조회 및 시각화</h1>", unsafe_allow_html=True)
# st.markdown("<h3 style='text-align: center; color: grey; font-size: 20px;'></h3>", unsafe_allow_html=True)

#2nd
col1, col2, col3 = st.columns([6,2,2])

with col1:
   st.header("")

#사용자에게 코인 이름 받기
with col2:
   st.header("")
#    coin_name = st.text_input('코인 이름을 입력하세요. (예: KRW-BTC)')

#사용자에게 원하는 날짜 받기
with col3:
   st.header("")
   input_date = st.date_input("조회할 날짜를 선택하세요.", datetime.date.today())

#3rd
col1, col2, col3 = st.columns([4,4,2])

with col1:
   st.markdown("<h2 style='text-align: center; color: blue;'>UPBIT Historical Data Viewer</h2>", unsafe_allow_html=True)
   st.markdown(f"<p style='font-size: 23px; text-align: right;'>Date: {input_date}</p>", unsafe_allow_html=True)
   
   # 코인 심볼과 날짜 입력 받기
   coin_name = st.text_input("Enter Coin Symbol (e.g., KRW-BTC):")
   
   # 선택한 날짜를 기준으로 -6일을 계산하여 시작 날짜 설정
   start_date = input_date - datetime.timedelta(days=6)

   # 종료일을 선택한 날짜의 다음 날로 설정하여 데이터를 가져옴
   end_date = input_date + datetime.timedelta(days=1)

   # PyUpbit을 사용하여 OHLCV 데이터 가져오기
   df = pyupbit.get_ohlcv(coin_name, "day", to=end_date, count=7)

   # 에러 메시지를 구성하여 사용자가 날짜를 오늘 날짜 이후로 선택했을 때 안내 제공
   if input_date > datetime.date.today():
       st.error("선택한 날짜가 오늘보다 미래입니다. 가장 최근 데이터를 가져옵니다.")
       input_date = datetime.date.today()

   # 데이터가 비어 있는지 확인
   if df is not None and not df.empty:
       # 데이터 출력
       st.write("Historical Data:")
    # 데이터는 잘 가져오니까 가리기..
    #    st.write(df)
    # 데이터를 시각화
       plt.figure(figsize=(10, 6))
       plt.plot(df.index, df['close'], marker='o', color='b', linestyle='-')
       plt.title(f"{coin_name} price")
       plt.xlabel("")
       plt.ylabel("Close Price (KRW)")
       plt.xticks(rotation=45)
       plt.grid(True)
       st.pyplot(plt)

       start_date = df.index[0]
       end_date = df.index[-1]
       plt.xlim(start_date, end_date)
   else:
      st.write("")

with col2:
    st.markdown("<h2 style='text-align: center; color: orange;'>Binance Historical Data Viewer</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 23px; text-align: right;'>Date: {input_date}</p>", unsafe_allow_html=True)

    def fetch_historical_data(symbol, start_date):
        # Binance API URL
        api_url = "https://api.binance.com"

        # API 요청하여 가격 가져오기
        response = requests.get(f"{api_url}/api/v3/klines",
                                params={"symbol": symbol, "interval": "1d", "startTime": start_date, "limit": 7})
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume", "Close Time", "Quote Asset Volume", "Number of Trades", "Taker Buy Base Asset Volume", "Taker Buy Quote Asset Volume", "Ignore"])
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms", utc=True)  # UTC 시간대로 변환
            df["Close"] = pd.to_numeric(df["Close"])  # 가격 데이터를 숫자형으로 변환
            return df
        else:
            st.error("Error fetching data from Binance API")

    def main():
        # 코인 심볼과 날짜 입력 받기
        symbol = st.text_input("Enter Coin Symbol (e.g., BTCUSDT):")

        # 선택한 날짜를 기준으로 -6일을 계산하여 시작 날짜 설정
        start_date = input_date - datetime.timedelta(days=6)

        if symbol and input_date:
            start_timestamp = int(pd.Timestamp(start_date).timestamp()) * 1000
            data = fetch_historical_data(symbol.upper(), start_timestamp)
            if data is not None:
                st.write("Historical Data:")

                # Matplotlib을 사용하여 시계열 차트 그리기
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.plot(data["Timestamp"], data["Close"], marker='o', linestyle='-')
                ax.set_title(f"{symbol.upper()} Price (7 Days)")
                ax.set_xlabel("Date (UTC)")
                ax.set_ylabel("Price")
                ax.tick_params(axis='x', rotation=45)
                st.pyplot(fig)
            else:
                st.write("No data available")

    if __name__ == "__main__":
        main()



with col3:
   st.markdown("<h2 style='text-align: center;'>Exchange Rates</h2>", unsafe_allow_html=True)
   
   def get_exchange_rates():
    # 환율 정보를 저장할 딕셔너리
    exchange_rates = {}
    # 환율 정보를 가져올 페이지 URL
    url = "https://finance.naver.com/marketindex/exchangeDailyQuote.nhn?marketindexCd=FX_USDKRW&page=1&fdtc=1"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # 날짜별로 환율 정보를 가져옵니다.
        rows = soup.find_all("tr")
        for row in rows:
            date_elem = row.find("td", class_="date")
            if date_elem:
                # 날짜를 키로 하고 환율 정보를 값으로 딕셔너리에 저장합니다.
                date = date_elem.text.strip()
                exchange_rate_elem = row.find("td", class_="num")
                if exchange_rate_elem:
                    exchange_rate = exchange_rate_elem.text.strip()
                    exchange_rates[date] = exchange_rate
    return exchange_rates

   def main():
    if st.button("확인"):
        exchange_rates = get_exchange_rates()
        if input_date.strftime("%Y.%m.%d") in exchange_rates:
            exchange_rate = exchange_rates[input_date.strftime("%Y.%m.%d")]
            st.write(f"{input_date.strftime('%Y.%m.%d')}의 USD/KRW 환율은 {exchange_rate}원 입니다.")
        else:
            st.write("선택한 날짜에 대한 환율 정보를 찾을 수 없습니다.")

   if __name__ == "__main__": 
       main()