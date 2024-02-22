import streamlit as st
import os
import json
import instaloader
import pandas as pd

#dummy examples
best_competitor_post_1 = {
    "caption": "Check out this delicious breakfast!",
    "likes": 100,
    "comments": 20,
    "date": "2024-02-18",
    "url": "https://www.instagram.com/p/123456789",
    "likes/followers": 0.05,
    "comments/followers": 0.01,
    "username": "foodie_123",
    "bio": "Food lover 🍔🍰 | Chef in the making 🍳 | Sharing my culinary adventures!",
    "posts": 500,
    "background_description": "Solid pink background",
    "objects_description": "Top spoon with crispy cereal and a drip of milk, bottom spoon with glossy black spheres resembling tapioca pearls",
    "text": "No",
    "vibe": ["Playful", "quirky"],
    "colors": ["Pink", "Gold", "White", "Black", "Brown"],
    "contrast": 0.5,
    "brightness": 0.8,
    "saturation": 0.7,
    "shadows": 0.2
}

best_competitor_post_2 = {
    "caption": "Morning vibes with a cup of coffee ☕️",
    "likes": 250,
    "comments": 30,
    "date": "2024-02-18",
    "url": "https://www.instagram.com/p/234567890",
    "likes/followers": 0.08,
    "comments/followers": 0.015,
    "username": "caffeine_addict",
    "bio": "Coffee enthusiast ☕️ | Travel lover 🌍 | Exploring the world one cup at a time!",
    "posts": 800,
    "background_description": "Wooden table",
    "objects_description": "Coffee mug with steam",
    "text": "No",
    "vibe": ["Cozy", "relaxed"],
    "colors": ["Brown", "White"],
    "contrast": 0.6,
    "brightness": 0.7,
    "saturation": 0.6,
    "shadows": 0.3
}

best_competitor_post_3 = {
    "caption": "Sunny day at the beach 🏖️",
    "likes": 300,
    "comments": 40,
    "date": "2024-02-18",
    "url": "https://www.instagram.com/p/345678901",
    "likes/followers": 0.09,
    "comments/followers": 0.02,
    "username": "beachlover_87",
    "bio": "Beach bum 🌊 | Sun worshiper ☀️ | Salt in the air, sand in my hair!",
    "posts": 1000,
    "background_description": "Sandy beach",
    "objects_description": "Umbrella, beach towel, flip-flops",
    "text (presence of text in the picture)": "No",
    "vibe": ["Relaxing", "carefree"],
    "colors": ["Blue", "Yellow", "White"],
    "contrast": 0.7,
    "brightness": 0.9,
    "saturation": 0.8,
    "shadows": 0.4
}

best_competitor_post_4 = {
    "caption": "Exploring the wilderness 🌲",
    "likes": 150,
    "comments": 25,
    "date": "2024-02-18",
    "url": "https://www.instagram.com/p/456789012",
    "likes/followers": 0.06,
    "comments/followers": 0.012,
    "username": "nature_lover_99",
    "bio": "Outdoor enthusiast 🏞️ | Hiking addict 🥾 | Nature's playground!",
    "posts": 600,
    "background_description": "Forest",
    "objects_description": "Trees, rocks, hiking gear",
    "text": "No",
    "vibe": ["Adventurous", "serene"],
    "colors": ["Green", "Brown", "Grey"],
    "contrast": 0.4,
    "brightness": 0.6,
    "saturation": 0.5,
    "shadows": 0.1
}

best_competitor_post_5 = {
    "caption": "City lights ✨",
    "likes": 400,
    "comments": 50,
    "date": "2024-02-18",
    "url": "https://www.instagram.com/p/567890123",
    "likes/followers": 0.1,
    "comments/followers": 0.025,
    "username": "cityscape_photog",
    "bio": "Urban explorer 🌆 | Night owl 🦉 | Chasing neon dreams!",
    "posts": 1200,
    "background_description": "City skyline",
    "objects_description": "Skyscrapers, street lights",
    "text (presence of text in the picture)": "No",
    "vibe": ["Vibrant", "dynamic"],
    "colors": ["Blue", "Yellow", "Orange", "White"],
    "contrast": 0.8,
    "brightness": 0.85,
    "saturation": 0.75,
    "shadows": 0.6
}

client_post = {
    "caption": "City lights ✨",
    "likes": 400,
    "comments": 50,
    "date": "2024-02-18",
    "url": "https://www.instagram.com/p/567890123",
    "likes/followers": 0.1,
    "comments/followers": 0.025,
    "username": "cityscape_photog",
    "bio": "Urban explorer 🌆 | Night owl 🦉 | Chasing neon dreams!",
    "posts": 1200,
    "background_description": "City skyline",
    "objects_description": "Skyscrapers, street lights",
    "text": "No",
    "vibe": ["Vibrant", "dynamic"],
    "colors": ["Blue", "Yellow", "Orange", "White"],
    "contrast": 0.8,
    "brightness": 0.85,
    "saturation": 0.75,
    "shadows": 0.6
}

best_competitor_post_list = [best_competitor_post_1, best_competitor_post_2, best_competitor_post_3, best_competitor_post_4, best_competitor_post_5]

def process_features(best_competitor_post_list, client_post):
    mean_contrast = 0
    min_contrast = float('inf')
    max_contrast = -float('inf')

    mean_brightness = 0
    min_brightness = float('inf')
    max_brightness = -float('inf')

    mean_saturation = 0
    min_saturation = float('inf')
    max_saturation = -float('inf')

    mean_shadows = 0
    min_shadows = float('inf')
    max_shadows = -float('inf')
    
    text_present = 0
    color_mapping = {}

    for post_features in best_competitor_post_list:
        mean_shadows += post_features['shadows']
        min_shadows = min(min_shadows, post_features['shadows'])
        max_shadows = max(max_shadows, post_features['shadows'])

        mean_contrast += post_features['contrast']
        min_contrast = min(min_contrast, post_features['contrast'])
        max_contrast = max(max_contrast, post_features['contrast'])

        mean_saturation += post_features['saturation']
        min_saturation = min(min_saturation, post_features['saturation'])
        max_saturation = max(max_saturation, post_features['saturation'])

        mean_brightness += post_features['brightness']
        min_brightness = min(min_brightness, post_features['brightness'])
        max_brightness = max(max_brightness, post_features['brightness'])
        
        if post_features['text'].lower() == "yes":
            text_present += 1
        
        for color in post_features['colors']:
            color = color.lower()
            color_mapping[color] = color_mapping.get(color, 0) + 1

    mean_shadows = mean_shadows/len(best_competitor_post_list)
    mean_brightness = mean_brightness/len(best_competitor_post_list)
    mean_contrast = mean_contrast/len(best_competitor_post_list)
    mean_saturation = mean_saturation/len(best_competitor_post_list)
    
    brightness_in_range = False
    shadows_in_range = False
    saturation_in_range = False
    contrast_in_range = False
    
    if client_post['shadows'] >= min_shadows and client_post['shadows'] <= max_shadows:
        shadows_in_range = True
    
    if client_post['brightness'] >= min_brightness and client_post['brightness'] <= max_brightness:
        brightness_in_range = True
    
    if client_post['saturation'] >= min_saturation and client_post['saturation'] <= max_saturation:
        saturation_in_range = True
    
    if client_post['contrast'] >= min_contrast and client_post['contrast'] <= max_contrast:
        contrast_in_range = True
    
    results = [
        [mean_contrast, min_contrast, max_contrast],
        [mean_brightness, min_brightness, max_brightness],
        [mean_saturation, min_saturation, max_saturation],
        [mean_shadows, min_shadows, max_shadows]
    ]
    
    
    st.write(" ")
    if brightness_in_range:
        st.write(f"After analyzing the top 5 posts of the competitors you requested for, the minimum brightness in the competitor posts is {results[1][1]} and the maximum brightness is {results[1][2]}. The brightness of the image in your post falls within this range and doesn't need to be changed")
    else:
        st.write(f"After analyzing the top 5 posts of the competitors you requested for, the minimum brightness in the competitor posts is {results[1][1]} and the maximum brightness is {results[1][2]}. Your brightness falls outside this range. A suggested brightness for your post is {results[1][0]}, which is the average brightness across all the competitor posts.")

    st.write(" ")
    if shadows_in_range:
        st.write(f"After analyzing the top 5 posts of the competitors you requested for, the minimum shadows in the competitor posts is {results[3][1]} and the maximum shadows is {results[3][2]}. Your shadows fall within this range and don't need to be changed")
    else:
        st.write(f"After analyzing the top 5 posts of the competitors you requested for, the minimum shadows in the competitor posts is {results[3][1]} and the maximum shadows is {results[3][2]}. Your shadows fall outside this range. A suggested value for shadows in your post is {results[3][0]}, which is the average shadows across all the competitor posts.")

    st.write(" ")
    if saturation_in_range:
        st.write(f"After analyzing the top 5 posts of the competitors you requested for, the minimum saturation in the competitor posts is {results[2][1]} and the maximum saturation is {results[2][2]}. Your saturation falls within this range and doesn't need to be changed")
    else:
        st.write(f"After analyzing the top 5 posts of the competitors you requested for, the minimum saturation in the competitor posts is {results[2][1]} and the maximum saturation is {results[2][2]}. Your saturation falls outside this range. A suggested saturation for your post is {results[2][0]}, which is the average saturation across all the competitor posts.")

    st.write(" ")
    if contrast_in_range:
        st.write(f"After analyzing the top 5 posts of the competitors you requested for, the minimum contrast in the competitor posts is {results[0][1]} and the maximum contrast is {results[0][2]}. Your contrast falls within this range and doesn't need to be changed")
    else:
        st.write(f"After analyzing the top 5 posts of the competitors you requested for, the minimum contrast in the competitor posts is {results[0][1]} and the maximum contrast is {results[0][2]}. Your contrast falls outside this range. A suggested contrast for your post is {results[0][0]}, which is the average contrast across all the competitor posts.")
        
    sorted_colors = sorted(color_mapping, key=color_mapping.get, reverse=True)

    count = 0
    top_3_colors = []
    for color in sorted_colors:
        frequency = color_mapping[color]
        count += 1
        top_3_colors.append(color)
        if count == 3:
            break

    st.text(" ")
    st.write("Top 3 used colors in competitor posts:")
    st.text(" ")
    for color in top_3_colors:
        st.write(color)

    st.text(" ")
    st.write("You could consider adding these colors to the images in your posts")

    st.text(" ")
    if text_present >= 3 and client_post['text'].lower() == "no": #only print if majority of competitors have text and you don't have text on the image
        st.write(f"Of the top 5 competitor posts, {text_present} of them have text on the images associated with the post. You could consider text on the image in your post to get more traction.")
        
            
            
        
        

        # return brightness_in_range, shadows_in_range, saturation_in_range, contrast_in_range, results, color_mapping, text_present

    # brightness_in_range, shadows_in_range, saturation_in_range, contrast_in_range, results, color_mapping, text_present = process_features(best_competitor_post_list, client_post)

