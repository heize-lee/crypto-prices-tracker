# crypto-prices-tracker

> coin price를 추적하고, 특정 날짜 기간의 차트를 제공합니다.

1. 원하는 날짜의 코인 가격을 제공합니다.
2. 원하는 날짜의 과거 7일간의 데이터를 차트로 시각화하여 확인할 수 있습니다.
3. 국내거래소와 해외거래소의 가격차이를 차트로만 확인할 수 있습니다. (심할때만..)

```python
pip install pyupbit #Python Wrapper for Upbit API

```

## 개발 환경 설정

```python

#to be continue...
```

## 업데이트 내역

* 0.0.1
  * feat: Upbit Historical Data Viewer 기능 추가
- Upbit 라이브러리를 사용하여 코인의 일일 가격 데이터를 조회하고 시각화하는 기능 추가
- 사용자가 코인 심볼과 시작 날짜를 입력할 수 있음
- 선택한 날짜를 기준으로 7일간의 가격 데이터를 조회하여 그래프로 표시

* 0.0.2
  * feat: Binance Historical Data Viewer 기능 추가
- Binance API를 사용하여 코인의 일일 가격 데이터를 조회하고 시각화하는 기능 추가
- 사용자가 코인 심볼과 시작 날짜를 입력할 수 있음
- 선택한 날짜를 기준으로 7일간의 가격 데이터를 조회하여 그래프로 표시

  * feat: 환율 조회 기능 추가
- 네이버 금융에서 USD/KRW 환율을 조회하는 기능 추가
- 사용자가 날짜를 선택하여 해당 날짜의 환율을 확인할 수 있음

## 정보
[https://github.com/heize-lee/crypto-prices-tracker](https://github.com/heize-lee/crypto-prices-tracker)

## 기여 방법

1. ([https://github.com/heize-lee/crypto-prices-tracker/fork](https://github.com/yourname/yourproject/fork))을 포크합니다.
2. (`git checkout -b feature/fooBar`) 명령어로 새 브랜치를 만드세요.
3. (`git commit -am 'Add some fooBar'`) 명령어로 커밋하세요.
4. (`git push origin feature/fooBar`) 명령어로 브랜치에 푸시하세요.
5. 풀리퀘스트를 보내주세요.

<!-- Markdown link & img dfn's -->
