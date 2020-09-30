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

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

force_suffix = "--force"
verbose_suffix = "--verbose"

if username != '':

    force_update = False
    verbose = False

    if force_suffix in username:
        username = username.replace(force_suffix, '')
        force_update = True

    if verbose_suffix in username:
        username = username.replace(verbose_suffix, '')
        verbose = True
    try:
        following_list = mtf.get_following_list(username)
        hit = mtf.get_db_hit_ratio(following_list)
        total = len(following_list)
        time = round((hit * known_time + (total - hit) * unknown_time) // 60) + 1
        with st.spinner(f'It should take us around {time} minute'+'s'*(time > 1)+f' to retrieve the {total} accounts followed by {username}'+', have a :cocktail: and relax...'):
            contributors = mtf.get_tweet_flow_contributors(username, depth=50, force_update=force_update).iloc[:, 1:]
        st.balloons()

        st.success('Success !')
        tph = contributors['Tweets per hour'].sum()
        spt = int(3600 / tph)
        if spt > 3599:
            st.markdown(
                f"{username} should get new tweets every {spt // 3600} hours and {(spt % 3600) // 60} minutes and here are the main contributors :")
        elif spt > 59:
            st.markdown(
                f"{username} should get new tweets every {spt // 60} minutes and {spt % 60} seconds and here are the main contributors :")
        else:
            st.markdown(f"{username} should get new tweets every {spt} seconds and here are the main contributors :")

        st.dataframe(contributors, width=2100, height=2000)
        st.write("These metrics are based on the 50 last tweets of each account. We don't include data from protected account.")
    except Exception as e:
        st.error(e)
        if verbose:
            raise e
