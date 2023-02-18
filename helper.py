from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
extract = URLExtract()
def fetch_stats(selected_user,df):

    if(selected_user == 'Overall'):
        #1.fetching number of messages
        num_messages = df.shape[0]
    #2 fetching number of words
        words=[]
        for message in df['message']:
            words.extend(message.split())
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
        links = []
        for message in df['message']:
            links.extend(extract.find_urls(message))
        return num_messages,len(words),num_media_messages,len(links)
    else:
        new_df = df[df['user'] == selected_user]
        num_messages = df[df['user'] == selected_user].shape[0]
        num_media_messages = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]
        words = []
        for message in new_df['message']:
            words.extend(message.split())
        links = []
        for message in new_df['message']:
            links.extend(extract.find_urls(message))

        return num_messages, len(words),num_media_messages,len(links)
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df  = round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df

#Word Cloud

def create_wordcloud(selected_user,df):
    if(selected_user != 'Overall'):
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='black')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))
    return df_wc
def most_common_words(selected_user,df):
    f = open('higlish_stopwords.txt','r')
    stop_words = f.read()
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = df[df['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def emoji_helper(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df

def monthly_timeline(selected_user,df):
    if (selected_user != 'Overall'):
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year','month']).count()['message'].reset_index()
    time =  []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

# def daily_timeline(selected_user,df):
#     if (selected_user != 'Overall'):
#         df = df[df['user'] == selected_user]
#     time=[]
#     for i in range(df.shape[0]):
#         time.append(str(df['day'][i]) +"-" +str(df['month'][i]) +"-" +str(df['year']))
#     df['date_time'] = time
#     return df