import streamlit as st
from openai import OpenAI
import gpt_api as image
#import api_keys
import requests
from PIL import Image
from io import BytesIO
import streamlit.components.v1 as components
from streamlit_tags import st_tags, st_tags_sidebar
import base64
import io
import imgbbpy
import process_pictures
import post_processing
import post_processing_updated

import pandas as pd
import numpy as np
import os
import json
import random
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import time
import altair as alt
from utils import display_dial_v2



# page config for wide mode
st.set_page_config(layout="wide", page_icon="logo/google-product-hackathon-logo.png")


if 'stage' not in st.session_state:
    st.session_state.stage = 0


def get_base64_of_bin_file(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

def add_logo_to_sidebar(logo_path, width=200):
    # Open the image and convert it to base64
    with open(logo_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # Create an HTML img tag with the base64 encoded image
    img_html = f"<img src='data:image/png;base64,{encoded_string}' width='{width}' />"
    
    # Display the image in the sidebar using HTML
    st.sidebar.markdown(img_html, unsafe_allow_html=True)


def add_logo_main(logo_path, width=150):
    # Open the image and convert it to base64
    with open(logo_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    # Create an HTML img tag with the base64 encoded image
    img_html = f"<img src='data:image/png;base64,{encoded_string}' width='{width}' />"
    
    # Display the image in the sidebar using HTML
    st.markdown(img_html, unsafe_allow_html=True)


add_logo_to_sidebar("logo/google-product-hackathon-logo.png")

# add_logo_main("logo/google-product-hackathon-logo.png")

# def animated_page_title_with_gradient(title):
#     st.markdown(f"""
#     <style>
#     @keyframes revealTitle {{
#         from {{ width: 0; }}
#         to {{ width: 100%; }}
#     }}

#     .animated-title-container {{
#         overflow: hidden;
#         white-space: nowrap;
#         font-size: 3rem;
#         font-weight: bold;
#         background: -webkit-linear-gradient(294deg, #8B4513, #111111);
#         background: linear-gradient(294deg, #8B4513, #111111);
#         -webkit-background-clip: text;
#         background-clip: text;
#         -webkit-text-fill-color: transparent;
#         text-fill-color: transparent;
#     }}
#     </style>
#     <div class="animated-title-container">{title}</div>
#     """, unsafe_allow_html=True)

def animated_page_title_with_gradient(title):
    # Splitting the title to apply gradient only to "Sherlock Picasso"
    gradient_part = "Sherlock Picasso"
    rest_of_title = title.replace(gradient_part, "")  # Removes "Sherlock Picasso" from the rest of the title

    st.markdown(f"""
    <style>
    @keyframes revealTitle {{
        from {{ width: 0; }}
        to {{ width: 100%; }}
    }}

    .gradient-text {{
        font-size: 3rem;
        font-weight: bold;
        background: -webkit-linear-gradient(294deg, #805c34, #302414);
        background: linear-gradient(294deg, #805c34, #302414);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        text-fill-color: transparent;
    }}

    .animated-title-container {{
        overflow: hidden;
        white-space: nowrap;
        font-size: 3rem;
        font-weight: bold;
        color: #805c34;
    }}
                
    @media (max-width: 768px) {{
        .animated-title-container {{
            font-size: 3rem; /* Smaller font size on smaller screens */
            white-space: normal; /* Allows text wrapping */
        }}
    }}
    </style>
    <div class="animated-title-container">
        <span class="gradient-text">{gradient_part}</span>{rest_of_title}
    </div>
    """, unsafe_allow_html=True)

# Example usage
animated_page_title_with_gradient("Sherlock Picasso")
# st.title("Sherlock Picasso - Analyze and Improve Your Instagram Post!")


def set_state(i):
    st.session_state.stage = i

# Function to load CSV file
def load_csv_file():
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, index_col=0)
        return df
    else:
        return None

def save_image_to_folder(image, index):
    image_path = f"image_streamlit/image_{index}.jpg"
    try:
        image.save(image_path)
        st.write(f"Image {index} saved to {image_path}")
        return image_path
    except Exception as e:
        st.error(f"Error saving image {index}: {e}")
        return None

def save_uploaded_file(directory, file):
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(os.path.join(directory, file.name), "wb") as f:
        f.write(file.getbuffer())
    file_path = os.path.join(directory, file.name)
    return file_path

def count_hashtags_in_posts(captions):
    # Create a dictionary to store the count of each hashtag
    hashtag_counts = {}
    
    # Iterate over each caption in the list of captions
    for caption in captions:
        # Use regular expression to find all hashtags in the caption
        # hashtags = re.findall(r'#\w+', caption)
        hashtags = [word[1:] for word in caption.split() if word.startswith("#")]
        # Count the occurrences of each hashtag in this caption
        for hashtag in hashtags:
            if hashtag in hashtag_counts:
                hashtag_counts[hashtag] += 1
            else:
                hashtag_counts[hashtag] = 1
    
    return hashtag_counts

def select_top_3(group):
    return group.head(3)

with st.sidebar:

# df = load_csv_file()
    st.write("## Enter Instagram Usernames for Comparison")
    competitiors = st_tags_sidebar(
        label='',
        text='Press enter to add more',
        maxtags = 10,
        key='1',
        value=["0andco", "gongchatea", "kungfuteausa", "superemoji_usa", "tenoneteahouse_us", "tigersugar.usa", "vivibubbletea"])
    
    submit_button = st.button("Submit", on_click=set_state, args=[1])
    
    # User Current Post: Image + Caption
    st.write("## Enter Image and Caption You want to Use")
    uploaded_image = st.file_uploader("Upload Image file")
    caption = st.text_input('Caption You Want to Use', 'Hello Instagram #Insta')

    # Once User ready to Analyze their post, save their image
    analyze = st.button("Improve my Post")

    st.write("## Your Post")
    if uploaded_image:
        st.image(uploaded_image)
        st.write('<div style="padding: 10px; border: 1px solid black; border-radius: 5px;">' + 
                         caption + '</div>', unsafe_allow_html=True)
        st.write(" ")

if analyze and uploaded_image is not None and caption is not None:
    # download the image and caption user uploaded
    # Save the uploaded image and get the path of saved image
    file_path = save_uploaded_file('user_image', uploaded_image)
    # st.write(f"Image saved at: {file_path}")

    # Process User's Image and Caption and Save as JSON
    ###### ################## TODO change "bb-BestBoba" to user's username whenever needed 
    process_pictures.process_new_post(file_path, caption, "bb-BestBoba")
    
    top5_file_path = 'results/top5.json'
    user_file_path = 'results/new_post.json'

    # Open the JSON file and load its content into a variable
    with open(top5_file_path, 'r') as top5_file:
        top5 = json.load(top5_file)
        #st.write(top5)

    with open(user_file_path, 'r') as user_file:
        client_post = json.load(user_file)

# st.write(result)

# df = load_csv_file()
tab1, tab2 = st.tabs([":mag_right: Competitor Analysis", ":lower_left_paintbrush: Get Recommendations"])

with tab1:
    if st.session_state.stage == 0:
        st.info('''
            How to use this app?
                
            - Step 1: Enter the Instagram usernames you want to compare
            - Step 2: Upload your image and enter your initial caption
                
                ''')
    if st.session_state.stage >= 1:
        df = pd.read_csv("bubble_tea_store/bubble_tea_combined_data.csv")

        # Extract Features from Image
        st.header("Top 10 Most Popular Posts")

        if df is not None:
            # df['score'] = df['likes/followers']*df["likes/followers"]
            df = df.sort_values(by=['likes/followers'], ascending=False).reset_index()
            df = df.drop(columns=['index'])

            # st.write(df)

            top_10 = df.sort_values(by=['likes/followers'], ascending=False)
            top_10 = top_10.groupby('username', group_keys=False).apply(select_top_3)
            top_10 = top_10.sort_values(by=['likes/followers'], ascending=False)

            top10 = top_10.head(10)

            os.makedirs("image_streamlit", exist_ok=True)

            images_url = ["https://i.ibb.co/cCrHJBz/image.jpg", 
                        "https://i.ibb.co/8gRM1mt/image.jpg", 
                        "https://i.ibb.co/d2jZ4VR/image.jpg", 
                        "https://i.ibb.co/PjvgCqF/image.jpg", 
                        "https://i.ibb.co/8jcHYWZ/image.jpg",
                        "https://i.ibb.co/6yp9c41/image.jpg",
                        "https://i.ibb.co/gFvw6Py/image.jpg",
                        "https://i.ibb.co/R4Qck7y/image.jpg",
                        "https://i.ibb.co/4RpCkhD/image.jpg",
                        "https://i.ibb.co/tYG3r3r/image.jpg"]
            
            captions = [i for i in top10['caption']]
            likes = [i for i in top10['likes']]
            followers = [i for i in top10['followers']]
            comments = [i for i in top10['comments']]
            users = [i for i in top10['username']]
            bio = [i for i in top10['bio']]

            hashtag_counts = count_hashtags_in_posts(captions)

            # images_url = []

            # client = imgbbpy.SyncClient('bb48c1935e87294f7d3a04fa02074c05')

            # imgbb_api_key = "bb48c1935e87294f7d3a04fa02074c05"

            # for index, row in top10.iterrows():
            #     response = requests.get(row['url'])
            #     image = Image.open(BytesIO(response.content))
            #     save_image_to_folder(image, index+1)
            #     image_path = f"image_streamlit/image_{index+1}.jpg"

            #     image_upload = client.upload(file=image_path)

            #     st.write(f"Image uploaded successfully: {image_upload.url}")
            #     images_url.append(image_upload.url)
            
            image_caption_map = dict(zip(images_url, captions))
            image_like_map = dict(zip(images_url, likes))
            image_followers_map = dict(zip(images_url, followers))
            image_comments_map = dict(zip(images_url, comments))
            image_users_map = dict(zip(images_url, users))
            image_bio_map = dict(zip(images_url, bio))

            imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")
            
            selectedImageUrl = imageCarouselComponent(imageUrls=images_url, height=200)

            col1, col2 = st.columns([1, 2])

            if selectedImageUrl is not None:
                with col1:
                    st.image(selectedImageUrl)
                with col2:
                    st.write('<img src="https://i.ibb.co/v3s6zgW/vecteezy-icono-de-instagram-logo-png-17743717.png" width="20" height="20">', "<b>" + image_users_map[selectedImageUrl] + "</b>", unsafe_allow_html=True)
                    st.write("**Bio:**", image_bio_map[selectedImageUrl])
                    st.write("**Followers:**", image_followers_map[selectedImageUrl])
                    st.write("**Likes:**", image_like_map[selectedImageUrl])
                    st.write("**Comments:**", image_comments_map[selectedImageUrl])

                st.write("**Caption:**")
                st.write('<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">' + 
                         image_caption_map[selectedImageUrl] + '</div>', unsafe_allow_html=True)

            st.write(" ")
            st.write(" ")
            # add a drop down
            with st.expander("Statistics"):
                st.write(" ")
                st.write("**Top Hashtags**")
                wordcloud = WordCloud(width=600, height=300, background_color="white").generate_from_frequencies(hashtag_counts)
                wordcloud_image = wordcloud.to_image()

                st.image(wordcloud_image)

                st.write(" ")
                st.write("**What are Popular Captions About?**")
                list_caption = [i for i in top10['caption']]
                wordcloud = WordCloud(width=600, height=300, background_color="white").generate(' '.join(list_caption))
                wordcloud_image = wordcloud.to_image()

                st.image(wordcloud_image)

                st.write(" ")
                mean_likes = (top10['likes/followers']*top10["followers"]).mean().round(2)
                mean_comments = (top10['comments/followers']*top10["followers"]).mean().round(2)
                display_dial_v2(st, "Average Likes", f"{mean_likes:.2f}", "#26369B")
                display_dial_v2(st, "Average Comments", f"{mean_comments:.2f}", "#26369B")
                st.write(" ")
                # remove outlier with comments/followers > 0.1
                df_filtered = df[df['comments/followers'] < 0.1]
                chart = alt.Chart(df_filtered).mark_circle(size=60).encode(
                    x='comments/followers:Q',  # Quantitative scale for comments/followers
                    y='likes/followers:Q',    # Quantitative scale for likes/followers
                    color='username:N',       # Nominal scale for usernames
                    tooltip=['username:N', 'comments/followers:Q', 'likes/followers:Q']  # Show info on hover
                ).properties(
                    width=700,
                    height=500,
                    title='Instagram Engagement: Comments/Followers vs. Likes/Followers'
                ).interactive()  # Enable zoom & pan

                # Display the chart in Streamlit
                st.altair_chart(chart, use_container_width=False)

                # Create the Altair chart for the histogram
                histogram = alt.Chart(df).mark_bar().encode(
                    x=alt.X('likes/followers:Q', bin=True, title='Likes/Followers'),
                    y=alt.Y('count()', title='Number of Posts'),
                ).properties(
                    width=700,
                    height=500,
                    title='Distribution of Likes/Followers Ratio',
                )
                # Display the chart in Streamlit
                st.altair_chart(histogram, use_container_width=False)

                # histogram with number of posts (column "posts") for each username "username", different color for each username but without legend
                histogram2 = alt.Chart(df).mark_bar().encode(
                    x=alt.X('username:N', title='Username'),
                    y=alt.Y('posts:Q', title='Number of Posts'),
                    color=alt.Color('username:N', legend=None),
                    tooltip=[alt.Tooltip('username:N', title='Username'), alt.Tooltip('posts:Q', title='Number of Posts')]
                ).properties(
                    width=700,
                    height=500,
                    title='Number of Posts for each Account',
                )
                # Display the chart in Streamlit
                st.altair_chart(histogram2, use_container_width=False)





with tab2:
    if st.session_state.stage == 0:
        st.info('''
            How to use this app?
                
            - Step 1: Enter the Instagram usernames you want to compare
            - Step 2: Upload your image and enter your initial caption
                ''')
        
    if st.session_state.stage >= 1:
        if analyze and uploaded_image is not None and caption is not None:
            # download the image and caption user uploaded
            # Save the uploaded image and get the path of saved image
            file_path = save_uploaded_file('user_image', uploaded_image)
            #st.write(f"Image saved at: {file_path}")

            with st.spinner('Analyzing Instagram posts..'):
                # Process User's Image and Caption and Save as JSON
                process_pictures.process_new_post(file_path, caption, "bb-BestBoba")

                # Process top 5 (or 10) images and save as JSON
                process_pictures.process_dataframe("bubble_tea_store/bubble_tea_combined_data.csv")
                #time.sleep(5)

            top5_file_path = 'results/top5.json'
            user_file_path = 'results/new_post.json'

            # Open the JSON file and load its content into a variable
            with open(top5_file_path, 'r') as top5_file:
                top5 = json.load(top5_file)
                #st.write(top5)

            with open(user_file_path, 'r') as user_file:
                client_post = json.load(user_file)

            post_processing_updated.process_features(top5, client_post)

            print("TYPE  ", type(top5))
            output = post_processing_updated.process_features_gpt(top5, client_post)
            print(output)
            output = json.loads(output)
            # output_caption = output.split("- **Background**:")[0]
            # output_photo = "- **Background**: " + output.split("- **Background**:")[1]
            print(type(output))

            st.write(" ")
            st.write(" ")
            st.markdown("### Personalized recommendations for your photo and caption")

            st.markdown("#### Photo")
            st.write("- **Background**: ", output['Background'])
            st.write("- **Objects**: ", output['Objects'])
            st.write("- **Vibe**: ", output['Vibe'])

            st.markdown("#### Caption")
            st.write(output['Caption'])


