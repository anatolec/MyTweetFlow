import streamlit as st
import my_tweet_flow as mtf

st.title('Analyse your Twitter home in one click !')

username = st.text_input('Twitter username', '@...')

if username != '@...':
    st.dataframe(mtf.get_tweet_flow_contributors(username).iloc[:, 1:])
