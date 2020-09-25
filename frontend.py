import streamlit as st
import my_tweet_flow as mtf
from PIL import Image

st.beta_set_page_config(page_title="Tweet Flow", layout='centered', page_icon=":shark:")

st.image(Image.open('twitter.png'), output_format='PNG', width=100)
st.title('Time to clean your timeline :smirk:')
st.title('Get your insights now !')

username = st.text_input('Enter your Twitter username and press enter :')

known_time = 0.0077
unknown_time = 0.4355

if username != '':
    try:
        with st.spinner('Wait for it... We are collecting data from all accounts you follow'):
            following_list = mtf.get_following_list(username)
            hit = mtf.get_db_hit_ratio(following_list)
            total = len(following_list)
            time = round((hit * known_time + (total - hit) * unknown_time) // 60) + 1
            with st.spinner(f'From the {total} accounts you follow, we already know {hit} of them. It should take us less than {time} minute'+'s, have a :cocktail:'*(time>1)):
                contributors = mtf.get_tweet_flow_contributors(username).iloc[:, 1:]
            st.balloons()
        st.success('Success !')
        tph = contributors['Tweets per hour'].sum()
        spt = int(3600 / tph)
        if spt > 3599:
            st.markdown(
                f"You should get a new tweet every {spt // 3600} hours and {(spt % 3600) // 60} minutes and here are the main contributors :")
        elif spt > 59:
            st.markdown(
                f"You should get a new tweet every {spt // 60} minutes and {spt % 60} seconds and here are the main contributors :")
        else:
            st.markdown(f"You should get a new tweet every {spt} seconds and here are the main contributors :")

        st.dataframe(contributors, width=2100, height=2000)
        st.write("These metrics are based on the 200 last tweets of each account. We don't include data from protected account.")
    except Exception as e:
        st.error(e)
