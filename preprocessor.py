import re
import pandas as pd
def preprocess(data):
    pattern = "\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s"
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if (entry[1:]):
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)
    year = []
    Y = []
    D = []
    M = []
    for a in df['date']:
        if (a[7] == ','):
            year.append(a[:7].strip())
        else:
            year.append(a[:8].strip())
    for y in year:
        k = y.split('/')
        Y.append('20' + k[-1])
        D.append(k[1])
        M.append(k[0])

    Year_ = []
    for y in Y:
        if (',' in y):
            Year_.append(y[:len(y) - 1])
        else:
            Year_.append(y)
    Month = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June', 7: 'July', 8: 'August',
             9: 'September', 10: 'October', 11: 'November', 12: 'December'}
    Month_ = []
    for m in M:
        Month_.append(Month[int(m)])
    H = []
    M = []
    n=df.shape[0]
    for i in range(n):
        li = df['date'][i].split(',')
        k = li[1].split(':')
        H.append(k[0].strip())
        M.append(k[1][:2])
    df['year'] = Year_
    df['month'] = Month_
    df['day'] = D
    df['hour'] = H
    df['minute'] = M
    return df
