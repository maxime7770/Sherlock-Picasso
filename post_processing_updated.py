import streamlit as st
import os
import json
import instaloader
import pandas as pd
from gpt_api import text_to_text_v2
import streamlit as st
import altair as alt


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

    mean_shadows = int(mean_shadows//len(best_competitor_post_list))
    mean_brightness = int(mean_brightness//len(best_competitor_post_list))
    mean_contrast = int(mean_contrast//len(best_competitor_post_list))
    mean_saturation = int(mean_saturation//len(best_competitor_post_list))
    
    brightness_in_range = False
    shadows_in_range = False
    saturation_in_range = False
    contrast_in_range = False
    text_present = True
    
    if client_post['shadows'] >= min_shadows and client_post['shadows'] <= max_shadows:
        shadows_in_range = True
    
    if client_post['brightness'] >= min_brightness and client_post['brightness'] <= max_brightness:
        brightness_in_range = True
    
    if client_post['saturation'] >= min_saturation and client_post['saturation'] <= max_saturation:
        saturation_in_range = True
    
    if client_post['contrast'] >= min_contrast and client_post['contrast'] <= max_contrast:
        contrast_in_range = True
    
    #store mean, min, max of all metrics across the 5 competitor images
    results = [
        [mean_contrast, min_contrast, max_contrast],
        [mean_brightness, min_brightness, max_brightness],
        [mean_saturation, min_saturation, max_saturation],
        [mean_shadows, min_shadows, max_shadows]
    ]
        
    brightness_recommendation = "Brightness does not need to be changed."
    saturation_recommendation = "Saturation does not need to be changed."
    contrast_recommendation = "Contrast does not need to be changed."
    shadow_recommendation = "Shadow does not need to be changed."
    text_recommendation = "No text needs to be added on the image."
    
    #recommendations if contrast, brightness, saturation, shadows don't fall in range
    if not contrast_in_range:
        # contrast_recommendation = f"A suggested saturation for your post is {results[0][0]}"
        contrast_gap = results[0][0]-client_post['contrast']
        if contrast_gap > 0:
            contrast_recommendation = f"Consider increase the contrast of your post by {contrast_gap}"
        else:
            contrast_recommendation = f"Consider decrease the contrast of your post by {abs(contrast_gap)}"

    if not brightness_in_range:
        # brightness_recommendation = f"A suggested brightness for your post is {results[1][0]}"
        brightness_gap = results[1][0]-client_post['brightness']
        if brightness_gap > 0:
            brightness_recommendation = f"Consider increase the brightness of your post by {brightness_gap}"
        else:
            brightness_recommendation = f"Consider decrease the brightness of your post by {abs(brightness_gap)}"
    
    if not saturation_in_range:
        # saturation_recommendation = f"A suggested saturation for your post is {results[2][0]}"
        saturation_gap = results[2][0]-client_post['saturation']
        if saturation_gap > 0:
            saturation_recommendation = f"Consider increase the saturation of your post by {saturation_gap}"
        else:
            saturation_recommendation = f"Consider decrease the saturation of your post by {abs(saturation_gap)}"
        
    if not shadows_in_range:
        # shadow_recommendation = f"A suggested shadow for your post is {results[3][0]}"
        shadow_gap = results[3][0]-client_post['shadows']
        if shadow_gap > 0:
            shadow_recommendation = f"Consider increase the shadow of your post by {shadow_gap}"
        else:
            shadow_recommendation = f"Consider decrease the shadow of your post by {abs(shadow_gap)}"

    sorted_colors = sorted(color_mapping, key=color_mapping.get, reverse=True)
    
    #getting top 3 most frequently used colors across the 5 competitor posts
    count = 0
    top_3_colors = []
    for color in sorted_colors:
        count += 1
        top_3_colors.append(color)
        if count == 3:
            break
    
    #colors recommendation based on top 3 most frequently used colors
    colors_recommendation = f"More of these colors can be used in the image for your post: {top_3_colors[0]}, {top_3_colors[1]}, and {top_3_colors[2]}"
    
    #if at least 3 of the top 5 performing posts and client doesn't have text already on image, recommend text on image
    
    if text_present >= 3 and client_post['text'].lower() == "no":
        text_present = False
        text_recommendation = f"You could consider adding text on the image in your post to get more traction."
    

    
    import streamlit as st
    import altair as alt
    import pandas as pd

    # Define the data for brightness
    brightness_data = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                    'Positions': [min_brightness, client_post['brightness'], max_brightness]})
    brightness_legend_labels = {'Min': 'Minimum Brightness across Competitor Posts', 'Yours': "Your Image's Brightness", 'Max': 'Maximum Brightness across Competitor Posts'}
    brightness_data['Values'] = brightness_data['Values'].map(brightness_legend_labels)

    # Create the number line plot for brightness


    brightness_number_line = alt.Chart(brightness_data).mark_point(size=50, filled=True, opacity=0.7).encode(
        x=alt.X('Positions:Q', scale=alt.Scale(domain=[-100, 100])),
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Brightness", labelLimit=0)),
        tooltip='Positions:N'
    ).properties(
        width=800,
        height=100
    )
    
    # Display the number line plot for brightness
    #st.write(brightness_number_line)
    
    # Define the data for contrast (similar to brightness)
    contrast_data = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                              'Positions': [min_contrast, client_post['contrast'], max_contrast]})
    contrast_legend_labels = {'Min': 'Minimum Contrast across Competitor Posts', 'Yours': "Your Image's Contrast", 'Max': 'Maximum Contrast across Competitor Posts'}
    contrast_data['Values'] = contrast_data['Values'].map(contrast_legend_labels)


    contrast_number_line = alt.Chart(contrast_data).mark_point(size=50, filled=True, opacity=0.7).encode(
        x=alt.X('Positions:Q', scale=alt.Scale(domain=[-100, 100])),  # Set domain explicitly
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Contrast", labelLimit=0)),
        tooltip='Positions:N'
    ).properties(
        width=800,
        height=100
    )

    # Display the number line plot for contrast
    #st.write(contrast_number_line)
    
    # Define the data for saturation (similar to brightness)
    saturation_data = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                'Positions': [min_saturation, client_post['saturation'], max_saturation]})
    saturation_legend_labels = {'Min': 'Minimum Saturation across Competitor Posts', 'Yours': "Your Image's Saturation", 'Max': 'Maximum Saturation across Competitor Posts'}
    saturation_data['Values'] = saturation_data['Values'].map(saturation_legend_labels)
    
    # Create the number line plot for saturation

    saturation_number_line = alt.Chart(saturation_data).mark_point(size=50, filled=True, opacity=0.7).encode(
        x=alt.X('Positions:Q', scale=alt.Scale(domain=[-100, 100])),  # Set domain explicitly
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Saturation", labelLimit=0)),
        tooltip='Positions:N'
    ).properties(
        width=800,
        height=100
    )

    # Display the number line plot for saturation
    #st.write(saturation_number_line)
    
    # Define the data for shadow (similar to brightness)
    shadow_data = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                'Positions': [min_shadows, client_post['shadows'], max_shadows]})
    shadow_legend_labels = {'Min': 'Minimum Shadow across Competitor Posts', 'Yours': "Your Image's Brightness", 'Max': 'Maximum Shadow across Competitor Posts'}
    shadow_data['Values'] = shadow_data['Values'].map(shadow_legend_labels)

    # Create the number line plot for shadow

    shadow_number_line = alt.Chart(shadow_data).mark_point(size=50, filled=True, opacity=0.7).encode(
        x=alt.X('Positions:Q', scale=alt.Scale(domain=[-100, 100])),  # Set domain explicitly
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Shadow", labelLimit=0)),
        tooltip='Positions:N'
    ).properties(
        width=800,
        height=100
    )
    
    st.markdown("### Image Features Analysis")

    st.markdown("#### Brightness")
    if brightness_in_range:
        st.success(brightness_recommendation)
    else:
        st.error(brightness_recommendation)
    st.altair_chart(brightness_number_line)


    st.markdown("#### Saturation")
    if saturation_in_range:
        st.success(saturation_recommendation)
    else:
        st.error(saturation_recommendation)
    st.altair_chart(saturation_number_line)

    st.markdown("#### Contrast")
    if contrast_in_range:
        st.success(contrast_recommendation)
    else:
        st.error(contrast_recommendation)
    st.altair_chart(contrast_number_line)

    st.markdown("#### Presence of Shadows")
    if shadows_in_range:
        st.success(shadow_recommendation)
    else:
        st.error(shadow_recommendation)
    st.altair_chart(shadow_number_line)
    
    st.markdown("#### Colors")
    st.error(colors_recommendation)
    
    st.markdown("#### Presence of Text")
    if text_present:
        st.success(text_recommendation)
    else:
        st.error(text_recommendation)
    
    return brightness_in_range, shadows_in_range, saturation_in_range, contrast_in_range, results, color_mapping, text_present

def process_features_gpt(best_competitor_post_list, client_post):

    # clean the list, remove the key "url" for each element
    for i in range(len(best_competitor_post_list)):
        best_competitor_post_list[i].pop("url")
        best_competitor_post_list[i].pop("date")
        

    prompt = f'''
    The following are Python dictionaries for 10 very popular instagram posts. Each dictionary contains information about the instagram account and the post. The last dictionary is for a new post that a user would like to compare to popular posts.

    You have to generate new features for the new post / new caption as a JSON format from these bullet points. DON'T provide anything else in the output. Each point will be further used to take a decision on a new post photo and caption.
    - "Caption": reformulate the caption based on popular posts to make it more engaging: give a reformulation that is similar to popular posts captions.
    - "Background": only generate a description for the new background description that should be used based on popular posts: it should be almost identical to existing background descriptions in most popular posts.
    - "Objects": what objects to change or add in the picture, give specific examples of objects to include based on the objects in popular posts.
    - "Vibe": what to change in vibe and the overall mood of the picture: give specific examples of popular vibes that would fit the picture based on the popular posts.

    
    ** LIST OF POPULAR POSTS **

    {best_competitor_post_list}

    ---------------

    ** NEW POST **

    {client_post}
    '''
    print(prompt)
    return  text_to_text_v2(prompt)
