from pandas_datareader import data as pdr
from datetime import datetime, timedelta
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def get_list():
    d = {}
    with open("data/info", 'r') as f:
        arr = f.read().split('\n')
        for st in arr:
            l = st.find('\t')
            ticker = st[:l]
            company = st[l + 1:]
            d[company] = ticker

    st_list = "ИМЯ компании: ТИКЕР\n\n"
    for i in d:
        if i != '':
            st_list += ("❗️%s: %s\n" % (i, d[i]))
    return st_list


def get_d():
    d = {}
    with open("data/info", 'r') as f:
        arr = f.read().split('\n')
        for st in arr:
            l = st.find('\t')
            ticker = st[:l]
            company = st[l + 1:]
            d[company] = ticker

    return d


def get_prediction(ticker):
    start_date = (datetime.today() - timedelta(days=30)).date()
    end_date = datetime.today()
    df = pdr.get_data_yahoo(ticker, start_date, end_date).dropna()[['Open', 'High', 'Low', 'Close']]

    df['Open&Close'] = df.Open - df.Close
    df['High&Low'] = df.High - df.Low
    X = df.dropna()[['Open&Close', 'High&Low']]
    Y = np.where(df['Close'].shift(-1) > df['Close'], 1, -1)

    x_train, y_train, x_test, y_test = X.iloc[:-1], Y[:-1], X.iloc[-1], Y[-1]
    knn = KNeighborsClassifier(n_neighbors=3)

    knn.fit(X, Y)

    return knn.predict([x_test])


def pred_message(a):
    if a == -1:
        st = "Я проанализировал закономерности, изучил последние 30 дней, мои источники говорят:\n" \
             "Все-таки стоит продать акции сегодня, ведь есть очевидная тендеция на спад цен📉"
        return st
    if a == 1:
        st = "Я проанализировал закономерности, изучил последние 30 дней\n" \
             "Обоснованно заявляю: сегодняшние акции будут стоит завтра дороже, срочно покупайте📈"
        return st
