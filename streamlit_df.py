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
import post_processing_final
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

if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False

if 'analyze' not in st.session_state:
    st.session_state.analyze = False

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


# Create Dictionary to Save all Computed Features
features = {}
def analyze_post(uploaded_image, caption):
    # If user Click Analyze, then compute features
    file_path = save_uploaded_file('user_image', uploaded_image)
    #st.write(f"Image saved at: {file_path}")

    with st.spinner('Analyzing Instagram posts..'):
        # Process User's Image and Caption and Save as JSON
        process_pictures.process_new_post(file_path, caption, "bb-BestBoba")

        top5_file_path = 'results/top5.json'
        top5_user_file_path = 'results/top5_user.json'
        user_file_path = 'results/new_post.json'

        # Open the JSON file and load its content into a variable
        with open(top5_file_path, 'r') as top5_file:
            top5 = json.load(top5_file)
        
        with open(top5_user_file_path, 'r') as top5_user_file:
            top5_user = json.load(top5_user_file)

        with open(user_file_path, 'r') as user_file:
            client_post = json.load(user_file)

    
        # b_brightness_comp, b_saturation_comp, b_contrast_comp, b_shadows_comp, b_brightness_host, b_saturation_host, b_contrast_host, b_shadows_host = post_processing_final.process_features(top5, client_post, top5_user)        
        
        output = post_processing_updated.process_features_gpt(top5, client_post)
        output = json.loads(output)
        output_user = post_processing_updated.process_features_gpt(top5_user, client_post)
        output_user = json.loads(output_user)

        # Add above output to the dictionary
        # features["b_brightness_comp"] = b_brightness_comp
        # features["b_saturation_comp"] = b_saturation_comp
        # features["b_contrast_comp"] = b_contrast_comp
        # features["b_shadows_comp"] = b_shadows_comp
        # features["b_brightness_host"] = b_brightness_host
        # features["b_saturation_host"] = b_saturation_host
        # features["b_contrast_host"] = b_contrast_host
        # features["b_shadows_host"] = b_shadows_host
        features["output"] = output
        features["output_user"] = output_user

        # save the dictionary into a file
        with open('features.json', 'w') as f:
            json.dump(features, f)
        
        st.session_state.analyze = True

with st.sidebar:

# df = load_csv_file()
    st.write("## Enter Instagram Usernames for Comparison")
    username = st.text_input('Your Instagram Username', 'taichibubbletea')
    competitiors = st_tags_sidebar(
        label='',
        text='Press enter to add more',
        maxtags = 10,
        key='1',
        value=["0andco", "gongchatea", "kungfuteausa", "superemoji_usa", "tenoneteahouse_us", "tigersugar.usa", "vivibubbletea"])
    
    if st.sidebar.button("Submit"):
        st.session_state.button_clicked = True
    
    # User Current Post: Image + Caption
    st.write("## Enter Image and Caption You want to Use")
    uploaded_image = st.file_uploader("Upload Image file")
    caption = st.text_input('Caption You Want to Use', 'Hello Instagram #Insta')

    # Once User ready to Analyze their post, save their image
    # analyze = st.button("Improve my Post")

    st.write("## Your Post")
    if uploaded_image:
        # st.image(uploaded_image)
        st.image("https://i.ibb.co/NN0XphP/Test-Image.jpg")
        st.write('<div style="padding: 10px; border: 1px solid black; border-radius: 5px;">' + 
                            caption + '</div>', unsafe_allow_html=True)
        st.write(" ")

    if st.sidebar.button("Improve my Post"):
        # st.session_state.analyze = True
        # if st.session_state.analyze and uploaded_image is not None and caption is not None:
        if uploaded_image is not None and caption is not None:
            analyze_post(uploaded_image, caption)


# if st.session_state.analyze and uploaded_image is not None and caption is not None:
#     # download the image and caption user uploaded
#     # Save the uploaded image and get the path of saved image
#     file_path = save_uploaded_file('user_image', uploaded_image)
#     # st.write(f"Image saved at: {file_path}")

#     # Process User's Image and Caption and Save as JSON
#     ###### ################## TODO change "bb-BestBoba" to user's username whenever needed 
#     process_pictures.process_new_post(file_path, caption, "bb-BestBoba")
    
#     top5_file_path = 'results/top5.json'
#     user_file_path = 'results/new_post.json'

#     # Open the JSON file and load its content into a variable
#     with open(top5_file_path, 'r') as top5_file:
#         top5 = json.load(top5_file)
#         #st.write(top5)

#     with open(user_file_path, 'r') as user_file:
#         client_post = json.load(user_file)

# st.write(result)

# df = load_csv_file()
tab1, tab2, tab3 = st.tabs([":mag_right: Competitor Analysis", ":female-detective: Your Account Analysis", ":lower_left_paintbrush: Get Recommendations"])

with tab1:
    if not st.session_state.button_clicked:
        st.info('''
            How to use this app?
                
            - Step 1: Enter your Instagram usernames 
            - Step 2: Enter competitor's Instagram usernames to compare
            - Step 3: Upload your image and enter your initial caption
                
                ''')
    if st.session_state.button_clicked:
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
    if not st.session_state.button_clicked:
        st.info('''
            How to use this app?
                
            - Step 1: Enter the Instagram usernames you want to compare
            - Step 2: Upload your image and enter your initial caption
                
                ''')
    if st.session_state.button_clicked:
        df = pd.read_csv("OurStore/taichi_combined.csv")

        # Extract Features from Image
        st.header("Your Top 10 Most Popular Posts")

        if df is not None:
            df = df.sort_values(by=['likes/followers'], ascending=False).reset_index()
            df = df.drop(columns=['index'])

            top_10 = df.sort_values(by=['likes/followers'], ascending=False)
            top_10 = top_10.groupby('username', group_keys=False).apply(select_top_3)
            top_10 = top_10.sort_values(by=['likes/followers'], ascending=False)

            top10 = top_10.head(10)

            os.makedirs("image_streamlit", exist_ok=True)

            images_url2 = ["https://i.ibb.co/fn4ZYjp/2024-02-13-05-48-57-UTC.jpg", 
                        "https://i.ibb.co/q7jrCqR/2024-02-14-09-03-23-UTC.jpg", 
			"https://i.ibb.co/j5V855Y/2024-02-22-08-54-42-UTC.jpg",
			"https://i.ibb.co/P6CdM23/2024-02-17-01-23-31-UTC.jpg",
			"https://i.ibb.co/xYc6y2C/2024-02-16-02-57-18-UTC.jpg",
			"https://i.ibb.co/vPCMNM2/2024-02-24-03-42-50-UTC.jpg",
			"https://i.ibb.co/SK0PZBD/2024-02-26-16-24-02-UTC.jpg",
			"https://i.ibb.co/hCZN7Nj/2024-02-18-02-46-21-UTC.jpg",
			"https://i.ibb.co/fnvvgLf/2024-02-12-00-33-46-UTC.jpg",
			"https://i.ibb.co/NWZ6Kcf/2024-02-27-07-13-26-UTC.jpg"]
            
            captions = [i for i in top10['caption']]
            likes = [i for i in top10['likes']]
            followers = [i for i in top10['followers']]
            comments = [i for i in top10['comments']]
            users = [i for i in top10['username']]
            bio = [i for i in top10['bio']]

            hashtag_counts = count_hashtags_in_posts(captions)
            
            image_caption_map = dict(zip(images_url2, captions))
            image_like_map = dict(zip(images_url2, likes))
            image_followers_map = dict(zip(images_url2, followers))
            image_comments_map = dict(zip(images_url2, comments))
            image_users_map = dict(zip(images_url2, users))
            image_bio_map = dict(zip(images_url2, bio))

            imageCarouselComponent2 = components.declare_component("image-carousel-component2", path="frontend/public")
            
            selectedImageUrl2 = imageCarouselComponent2(imageUrls=images_url2, height=200)

            col1, col2 = st.columns([1, 2])

            if selectedImageUrl2 is not None:
                with col1:
                    st.image(selectedImageUrl2)
                with col2:
                    st.write('<img src="https://i.ibb.co/v3s6zgW/vecteezy-icono-de-instagram-logo-png-17743717.png" width="20" height="20">', "<b>" + image_users_map[selectedImageUrl2] + "</b>", unsafe_allow_html=True)
                    st.write("**Bio:**", image_bio_map[selectedImageUrl2])
                    st.write("**Followers:**", image_followers_map[selectedImageUrl2])
                    st.write("**Likes:**", image_like_map[selectedImageUrl2])
                    st.write("**Comments:**", image_comments_map[selectedImageUrl2])

                st.write("**Caption:**")
                st.write('<div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px;">' + 
                         image_caption_map[selectedImageUrl2] + '</div>', unsafe_allow_html=True)

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


with tab3:
    # Create a page to display the features
    # Load features.json file and Check if features is empty
    if os.path.exists('features.json'):
        with open('features.json', 'r') as f:
            features = json.load(f)
    else:
        features = {}

    if features != {} and st.session_state.analyze:
        with st.form(key='my_form'):
            # Open the JSON file and load its content into a variable
            top5_file_path = 'results/top5.json'
            top5_user_file_path = 'results/top5_user.json'
            user_file_path = 'results/new_post.json'
            with open(top5_file_path, 'r') as top5_file:
                top5 = json.load(top5_file)
            
            with open(top5_user_file_path, 'r') as top5_user_file:
                top5_user = json.load(top5_user_file)

            with open(user_file_path, 'r') as user_file:
                client_post = json.load(user_file)

        
            (b_brightness_comp, b_saturation_comp, b_contrast_comp, b_shadows_comp, b_brightness_host, b_saturation_host, b_contrast_host, b_shadows_host, b_text_comp, b_text_host, b_colors_comp, b_colors_host,
            results_comp, color_mapping_comp, text_present_comp, results_host, color_mapping_host, text_present_host,
            brightness_in_range_comp, shadows_in_range_comp, saturation_in_range_comp, contrast_in_range_comp, brightness_in_range_host, shadows_in_range_host, saturation_in_range_host, contrast_in_range_host, colors_recommendation_comp, colors_recommendation_host, text_present_comp, text_recommendation_comp, text_recommendation_host) = post_processing_final.process_features(top5, client_post, top5_user)        
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.write(" ")
                st.write(" ")
                st.markdown("### Personalized recommendations for your post based on competitors' posts")

                st.markdown("#### Photo")
                checkbox_background_comp = st.checkbox("- **Background**: " +  features["output"]['Background'])
                checkbox_objects_comp = st.checkbox("- **Objects**: " + features["output"]['Objects'])
                checkbox_vibe_comp = st.checkbox("- **Vibe**: " + features["output"]['Vibe'])

                st.markdown("#### Caption")
                checkbox_caption_comp = st.checkbox(features["output"]['Caption'])

            with col2:
                st.write(" ")
                st.write(" ")
                st.markdown("### Personalized recommendations for your post based on your previous posts")

                st.markdown("#### Photo")
                checkbox_background_host = st.checkbox("- **Background**: " +  features["output_user"]['Background'])
                checkbox_objects_host = st.checkbox("- **Objects**: " + features["output_user"]['Objects'])
                checkbox_vibe_host = st.checkbox("- **Vibe**: " + features["output_user"]['Vibe'])

                st.markdown("#### Caption")
                checkbox_caption_host = st.checkbox(features["output_user"]['Caption'])

            submit_form = st.form_submit_button("Submit")

        if submit_form:
            st.session_state['result'] = True

    if 'result' in st.session_state:
        st.markdown("## Summary")

        st.subheader("Photo")

        # depending on checkboxes values, choose the corresponding recommendations
        if b_brightness_comp and not b_brightness_host:
            if not brightness_in_range_comp:
                st.write("- **Brightness**: " + f"A suggested brightness for your photo is {results_comp[1][0]}")
            else:
                st.write("- **Brightness**: " + "The brightness of your photo is good")
        elif not b_brightness_comp and b_brightness_host:
            if not brightness_in_range_host:
                st.write("- **Brightness**: " + f"A suggested brightness for your photo is {results_host[1][0]}")
            else:
                st.write("- **Brightness**: " + "The brightness of your photo is good")
        else:
            st.write("- **Brightness**: " + "The brightness of your photo is good")

        if b_saturation_comp and not b_saturation_host:
            if not saturation_in_range_comp:
                st.write("- **Saturation**: " + f"A suggested saturation for your photo is {results_comp[2][0]}")
            else:
                st.write("- **Saturation**: " + "The saturation of your photo is good")
        elif not b_saturation_comp and b_saturation_host:
            if not saturation_in_range_host:
                st.write("- **Saturation**: " + f"A suggested saturation for your photo is {results_host[2][0]}")
            else:
                st.write("- **Saturation**: " + "The saturation of your photo is good")
        else:
            st.write("- **Saturation**: " + "The saturation of your photo is good")

        if b_contrast_comp and not b_contrast_host:
            if not contrast_in_range_comp:
                st.write("- **Contrast**: " + f"A suggested contrast for your photo is {results_comp[0][0]}")
            else:
                st.write("- **Contrast**: " + "The contrast of your photo is good")
        elif not b_contrast_comp and b_contrast_host:
            if not contrast_in_range_host:
                st.write("- **Contrast**: " + f"A suggested contrast for your photo is {results_host[0][0]}")
            else:
                st.write("- **Contrast**: " + "The contrast of your photo is good")
        else:
            st.write("- **Contrast**: " + "The contrast of your photo is good")

        if b_shadows_comp and not b_shadows_host:
            if not shadows_in_range_comp:
                st.write("- **Shadow**: " + f"A suggested shadows for your photo is {results_comp[3][0]}")
            else:
                st.write("- **Shadow**: " + "The shadows of your photo are good")
        elif not b_shadows_comp and b_shadows_host:
            if not shadows_in_range_host:
                st.write("- **Shadow**: " + f"A suggested shadows for your photo is {results_host[3][0]}")
            else:
                st.write("- **Shadow**: " + "The shadows of your photo are good")
        else:
            st.write("- **Shadow**: " + "The shadows of your photo are good")

        if b_text_comp and not b_text_host:
            st.write("- **Text**: " + text_recommendation_comp)
        elif not b_text_comp and b_text_host:
            st.write("- **Text**: " + text_recommendation_host)

        if b_colors_comp and not b_colors_host:
            st.write("- **Color**: " + colors_recommendation_comp)
        elif not b_colors_comp and b_colors_host:
            st.write("- **Color**: " +colors_recommendation_host)


        if checkbox_background_comp and not checkbox_background_host:
            st.write("- **Background**: " + features["output"]['Background'])
        elif not checkbox_background_comp and checkbox_background_host:
            st.write("- **Background**: " + features["output_user"]['Background'])
        else:
            st.write("- **Background**: " + "No change needed")
        if checkbox_objects_comp and not checkbox_objects_host:
            st.write("- **Objects**: " + features["output"]['Objects'])
        elif not checkbox_objects_comp and checkbox_objects_host:
            st.write("- **Objects**: " + features["output_user"]['Objects'])
        else:
            st.write("- **Objects**: " + "No change needed")
        if checkbox_vibe_comp and not checkbox_vibe_host:
            st.write("- **Vibe**: " + features["output"]['Vibe'])
        elif not checkbox_vibe_comp and checkbox_vibe_host:
            st.write("- **Vibe**: " + features["output_user"]['Vibe'])

        st.subheader("Caption")

        if checkbox_caption_comp and not checkbox_caption_host:
            st.write("- **Text**: " + features["output"]['Caption'])
        elif not checkbox_caption_comp and checkbox_caption_host:
            st.write("- **Text**: " + features["output_user"]['Caption'])

