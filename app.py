import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import emoji
st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue() #data is in bytes of stream format
    data = bytes_data.decode("utf-8") # converting data into string format
    #st.text(data)
    df = preprocessor.preprocess(data)


    #fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if(st.sidebar.button('Show Analysis')):
        #Stats Area
        num_mssges,words,num_media_messages,links = helper.fetch_stats(selected_user,df)
        st.title('Top Statistics')
        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_mssges)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(links)
    #timeline

    #Monthly Timeline
    st.title('Monthly Timeline')
    timeline  = helper.monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['message'],color = 'green')
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)

    # #Daily Timeline
    # st.title('Daily Timeline')
    # timeline = helper.monthly_timeline(selected_user, df)
    # fig, ax = plt.subplots()
    # ax.plot(timeline['time'], timeline['message'], color='green')
    # plt.xticks(rotation='vertical')
    # st.pyplot(fig)
    

    if(selected_user == 'Overall'):
        st.title('Most Busy Users')
        x,new_df = helper.most_busy_users(df)
        fig,ax= plt.subplots()


        col1,col2 = st.columns(2)
        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(new_df)

        #Word Cloud
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        #most common words
        most_common_df = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        #Emoji Analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(),labels=emoji_df[0].head())
            st.pyplot(fig)







