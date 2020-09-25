import streamlit as st
import my_tweet_flow as mtf

st.title('Get your Twitter timeline insights !')

username = st.text_input('Enter your Twitter username and press enter :')

if username != '':
    try:
        contributors = mtf.get_tweet_flow_contributors(username).iloc[:, 1:]
        tph = contributors['Tweets per hour'].sum()
        spt = int(3600 / tph)
        if spt > 3599:
            st.write(
                f"You should get a new tweet every {spt // 3600} hours and {(spt % 3600) // 60} minutes and here are the main contributors :")
        elif spt > 59:
            st.write(
                f"You should get a new tweet every {spt // 60} minutes and {spt % 60} seconds and here are the main contributors :")
        else:
            st.write(f"You should get a new tweet every {spt} seconds and here are the main contributors :")

        st.dataframe(contributors, width=2100, height=2000)
    except Exception as e:
        st.error(e)
