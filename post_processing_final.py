import streamlit as st
import altair as alt
import pandas as pd

def process_features(best_competitor_post_list, client_post, best_host_posts):
    mean_contrast_comp = 0
    min_contrast_comp = float('inf')
    max_contrast_comp = -float('inf')

    mean_brightness_comp = 0
    min_brightness_comp = float('inf')
    max_brightness_comp = -float('inf')

    mean_saturation_comp = 0
    min_saturation_comp = float('inf')
    max_saturation_comp = -float('inf')

    mean_shadows_comp = 0
    min_shadows_comp = float('inf')
    max_shadows_comp = -float('inf')
    
    text_present_comp = 0
    color_mapping_comp = {}

    for post_features in best_competitor_post_list:
        mean_shadows_comp += post_features['shadows']
        min_shadows_comp = min(min_shadows_comp, post_features['shadows'])
        max_shadows_comp = max(max_shadows_comp, post_features['shadows'])

        mean_contrast_comp += post_features['contrast']
        min_contrast_comp = min(min_contrast_comp, post_features['contrast'])
        max_contrast_comp = max(max_contrast_comp, post_features['contrast'])

        mean_saturation_comp += post_features['saturation']
        min_saturation_comp = min(min_saturation_comp, post_features['saturation'])
        max_saturation_comp = max(max_saturation_comp, post_features['saturation'])

        mean_brightness_comp += post_features['brightness']
        min_brightness_comp = min(min_brightness_comp, post_features['brightness'])
        max_brightness_comp = max(max_brightness_comp, post_features['brightness'])
        
        if post_features['text'].lower() == "yes":
            text_present_comp += 1
        
        for color in post_features['colors']:
            color = color.lower()
            color_mapping_comp[color] = color_mapping_comp.get(color, 0) + 1

    mean_shadows_comp = int(mean_shadows_comp//len(best_competitor_post_list))
    mean_brightness_comp = int(mean_brightness_comp//len(best_competitor_post_list))
    mean_contrast_comp = int(mean_contrast_comp//len(best_competitor_post_list))
    mean_saturation_comp = int(mean_saturation_comp//len(best_competitor_post_list))
    
    brightness_in_range_comp = False
    shadows_in_range_comp = False
    saturation_in_range_comp = False
    contrast_in_range_comp = False
    text_present_comp = False
    
    if client_post['shadows'] >= min_shadows_comp and client_post['shadows'] <= max_shadows_comp:
        shadows_in_range_comp = True
    
    if client_post['brightness'] >= min_brightness_comp and client_post['brightness'] <= max_brightness_comp:
        brightness_in_range_comp = True
    
    if client_post['saturation'] >= min_saturation_comp and client_post['saturation'] <= max_saturation_comp:
        saturation_in_range_comp = True
    
    if client_post['contrast'] >= min_contrast_comp and client_post['contrast'] <= max_contrast_comp:
        contrast_in_range_comp = True
    
    #store mean, min, max of all metrics across the 5 competitor images
    results_comp = [
        [mean_contrast_comp, min_contrast_comp, max_contrast_comp],
        [mean_brightness_comp, min_brightness_comp, max_brightness_comp],
        [mean_saturation_comp, min_saturation_comp, max_saturation_comp],
        [mean_shadows_comp, min_shadows_comp, max_shadows_comp]
    ]
        
    brightness_recommendation_comp = "Brightness does not need to be changed."
    saturation_recommendation_comp = "Saturation does not need to be changed."
    contrast_recommendation_comp = "Contrast does not need to be changed."
    shadow_recommendation_comp = "Shadow does not need to be changed."
    text_recommendation_comp = "No text needs to be added on the image."
    
    #recommendations if contrast, brightness, saturation, shadows don't fall in range
        #recommendations if contrast, brightness, saturation, shadows don't fall in range
    if not contrast_in_range_comp:
        # contrast_recommendation = f"A suggested saturation for your post is {results[0][0]}"
        contrast_gap_comp = results_comp[0][0]-client_post['contrast']
        if contrast_gap_comp > 0:
            contrast_recommendation_comp = f"Consider increase the contrast of your post by {contrast_gap_comp}."
        else:
            contrast_recommendation_comp = f"Consider decrease the contrast of your post by {abs(contrast_gap_comp)}."
    
    if not brightness_in_range_comp:
        # contrast_recommendation = f"A suggested saturation for your post is {results[0][0]}"
        brightness_gap_comp = results_comp[1][0]-client_post['brightness']
        if brightness_gap_comp > 0:
            brightness_recommendation_comp = f"Consider increase the brightness of your post by {brightness_gap_comp}."
        else:
            brightness_recommendation_comp = f"Consider decrease the brightness of your post by {abs(brightness_gap_comp)}."
    
    if not saturation_in_range_comp:
        # saturation_recommendation = f"A suggested saturation for your post is {results[2][0]}"
        saturation_gap_comp = results_comp[2][0]-client_post['saturation']
        if saturation_gap_comp > 0:
            saturation_recommendation_comp = f"Consider increase the saturation of your post by {saturation_gap_comp}."
        else:
            saturation_recommendation_comp = f"Consider decrease the saturation of your post by {abs(saturation_gap_comp)})."
        
    if not shadows_in_range_comp:
        # shadow_recommendation = f"A suggested shadow for your post is {results[3][0]}"
        shadow_gap_comp = results_comp[3][0]-client_post['shadows']
        if shadow_gap_comp > 0:
            shadow_recommendation_comp = f"Consider increase the shadow of your post by {shadow_gap_comp}."
        else:
            shadow_recommendation_comp = f"Consider decrease the shadow of your post by {abs(shadow_gap_comp)}."

    sorted_colors_comp = sorted(color_mapping_comp, key=color_mapping_comp.get, reverse=True)
    
    #getting top 3 most frequently used colors across the 5 competitor posts
    count_comp = 0
    top_3_colors_comp = []
    for color in sorted_colors_comp:
        count_comp += 1
        top_3_colors_comp.append(color)
        if count_comp == 3:
            break
    
    #colors recommendation based on top 3 most frequently used colors
    colors_recommendation_comp = f"More of these colors can be used in the image for your post: **{top_3_colors_comp[0]}, {top_3_colors_comp[1]}, and {top_3_colors_comp[2]}**"
    
    #if at least 3 of the top 5 performing posts and client doesn't have text already on image, recommend text on image
    
    if text_present_comp >= 3 and client_post['text'].lower() == "no":
        text_present_comp = True
        text_recommendation_comp = f"You could consider adding text on the image in your post to get more traction."
    
    mean_contrast_host = 0
    min_contrast_host = float('inf')
    max_contrast_host = -float('inf')

    mean_brightness_host = 0
    min_brightness_host = float('inf')
    max_brightness_host = -float('inf')

    mean_saturation_host = 0
    min_saturation_host = float('inf')
    max_saturation_host = -float('inf')

    mean_shadows_host = 0
    min_shadows_host = float('inf')
    max_shadows_host = -float('inf')
    
    text_present_host = 0
    color_mapping_host = {}

    for post_features in best_host_posts:
        mean_shadows_host += post_features['shadows']
        min_shadows_host = min(min_shadows_host, post_features['shadows'])
        max_shadows_host = max(max_shadows_host, post_features['shadows'])

        mean_contrast_host += post_features['contrast']
        min_contrast_host = min(min_contrast_host, post_features['contrast'])
        max_contrast_host = max(max_contrast_host, post_features['contrast'])

        mean_saturation_host += post_features['saturation']
        min_saturation_host = min(min_saturation_host, post_features['saturation'])
        max_saturation_host = max(max_saturation_host, post_features['saturation'])

        mean_brightness_host += post_features['brightness']
        min_brightness_host = min(min_brightness_host, post_features['brightness'])
        max_brightness_host = max(max_brightness_host, post_features['brightness'])
        
        if post_features['text'].lower() == "yes":
            text_present_host += 1
        
        for color in post_features['colors']:
            color = color.lower()
            color_mapping_host[color] = color_mapping_host.get(color, 0) + 1

    mean_shadows_host = int(mean_shadows_host//len(best_host_posts))
    mean_brightness_host = int(mean_brightness_host//len(best_host_posts))
    mean_contrast_host = int(mean_contrast_host//len(best_host_posts))
    mean_saturation_host = int(mean_saturation_host//len(best_host_posts))
    
    brightness_in_range_host = False
    shadows_in_range_host = False
    saturation_in_range_host = False
    contrast_in_range_host = False
    text_present_host = False
    
    if client_post['shadows'] >= min_shadows_host and client_post['shadows'] <= max_shadows_host:
        shadows_in_range_host = True
    
    if client_post['brightness'] >= min_brightness_host and client_post['brightness'] <= max_brightness_host:
        brightness_in_range_host = True
    
    if client_post['saturation'] >= min_saturation_host and client_post['saturation'] <= max_saturation_host:
        saturation_in_range_host = True
    
    if client_post['contrast'] >= min_contrast_host and client_post['contrast'] <= max_contrast_host:
        contrast_in_range_host = True
    
    results_host = [
        [mean_contrast_host, min_contrast_host, max_contrast_host],
        [mean_brightness_host, min_brightness_host, max_brightness_host],
        [mean_saturation_host, min_saturation_host, max_saturation_host],
        [mean_shadows_host, min_shadows_host, max_shadows_host]
    ]
        
    brightness_recommendation_host = "Brightness does not need to be changed."
    saturation_recommendation_host = "Saturation does not need to be changed."
    contrast_recommendation_host = "Contrast does not need to be changed."
    shadow_recommendation_host = "Shadow does not need to be changed."
    text_recommendation_host = "No text needs to be added on the image."
    
    #recommendations if contrast, brightness, saturation, shadows don't fall in range
    if not contrast_in_range_host:
        # contrast_recommendation = f"A suggested saturation for your post is {results[0][0]}"
        contrast_gap_host = results_host[0][0]-client_post['contrast']
        if contrast_gap_host > 0:
            contrast_recommendation_host = f"Consider increase the contrast of your post by {contrast_gap_host}."
        else:
            contrast_recommendation_host = f"Consider decrease the contrast of your post by {abs(contrast_gap_host)}."
    
    if not brightness_in_range_host:
        # contrast_recommendation = f"A suggested saturation for your post is {results[0][0]}"
        brightness_gap_host = results_host[1][0]-client_post['brightness']
        if brightness_gap_host > 0:
            brightness_recommendation_host = f"Consider increase the brightness of your post by {brightness_gap_host}."
        else:
            brightness_recommendation_host = f"Consider decrease the brightness of your post by {abs(brightness_gap_host)}."
    
    if not saturation_in_range_host:
        # saturation_recommendation = f"A suggested saturation for your post is {results[2][0]}"
        saturation_gap_host = results_host[2][0]-client_post['saturation']
        if saturation_gap_host > 0:
            saturation_recommendation_host = f"Consider increase the saturation of your post by {saturation_gap_host}."
        else:
            saturation_recommendation_host = f"Consider decrease the saturation of your post by {abs(saturation_gap_host)}."
        
    if not shadows_in_range_host:
        # shadow_recommendation = f"A suggested shadow for your post is {results[3][0]}"
        shadow_gap_host = results_host[3][0]-client_post['shadows']
        if shadow_gap_host > 0:
            shadow_recommendation_host = f"Consider increase the shadow of your post by {shadow_gap_host}."
        else:
            shadow_recommendation_host = f"Consider decrease the shadow of your post by {abs(shadow_gap_host)}."

    sorted_colors_host = sorted(color_mapping_host, key=color_mapping_host.get, reverse=True)
    
    #getting top 3 most frequently used colors across the 5 host posts
    count_host = 0
    top_3_colors_host = []
    for color in sorted_colors_host:
        count_host += 1
        top_3_colors_host.append(color)
        if count_host == 3:
            break
    
    #colors recommendation based on top 3 most frequently used colors
    colors_recommendation_host = f"More of these colors can be used in the image for your post: **{top_3_colors_host[0]}, {top_3_colors_host[1]}, and {top_3_colors_host[2]}**"
    
    #if at least 3 of the top 5 performing posts and client doesn't have text already on image, recommend text on image
    
    if text_present_host >= 3 and client_post['text'].lower() == "no":
        text_present_host = True
        text_recommendation_host = f"You could consider adding text on the image in your post to get more traction."
    
    # Define the data for brightness
    brightness_data_comp = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                    'Positions': [min_brightness_comp, client_post['brightness'], max_brightness_comp]})
    brightness_legend_labels_comp = {'Min': 'Minimum', 'Yours': "Your Image's", 'Max': 'Maximum'}
    brightness_data_comp['Values'] = brightness_data_comp['Values'].map(brightness_legend_labels_comp)

    # Create the number line plot for brightness
    brightness_number_line_comp = alt.Chart(brightness_data_comp).mark_point(size=50, filled=True).encode(
        x='Positions:Q',
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Brightness")),
        tooltip='Positions:N'
    ).properties(
        width=400,
        height=100
    )
    
    # Define the data for contrast (similar to brightness)
    contrast_data_comp = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                              'Positions': [min_contrast_comp, client_post['contrast'], max_contrast_comp]})
    contrast_legend_labels_comp = {'Min': 'Minimum', 'Yours': "Your Image's", 'Max': 'Maximum'}
    contrast_data_comp['Values'] = contrast_data_comp['Values'].map(contrast_legend_labels_comp)

    # Create the number line plot for contrast
    contrast_number_line_comp = alt.Chart(contrast_data_comp).mark_point(size=50, filled=True).encode(
        x='Positions:Q',
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Contrast")),
        tooltip='Positions:N'
    ).properties(
        width=400,
        height=100
    )
    
    # Define the data for saturation (similar to brightness)
    saturation_data_comp = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                'Positions': [min_saturation_comp, client_post['saturation'], max_saturation_comp]})
    saturation_legend_labels_comp = {'Min': 'Minimum', 'Yours': "Your Image's", 'Max': 'Maximum'}
    saturation_data_comp['Values'] = saturation_data_comp['Values'].map(saturation_legend_labels_comp)
    
    # Create the number line plot for saturation
    saturation_number_line_comp = alt.Chart(saturation_data_comp).mark_point(size=50, filled=True).encode(
        x='Positions:Q',
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Saturation")),
        tooltip='Positions:N'
    ).properties(
        width=400,
        height=100
    )

    # Define the data for shadow (similar to brightness)
    shadow_data_comp = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                'Positions': [min_shadows_comp, client_post['shadows'], max_shadows_comp]})
    shadow_legend_labels_comp = {'Min': 'Minimum', 'Yours': "Your Image's", 'Max': 'Maximum'}
    shadow_data_comp['Values'] = shadow_data_comp['Values'].map(shadow_legend_labels_comp)

    # Create the number line plot for shadow
    shadow_number_line_comp = alt.Chart(shadow_data_comp).mark_point(size=50, filled=True).encode(
        x='Positions:Q',
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Shadow")),
        tooltip='Positions:N'
    ).properties(
        width=400,
        height=100
    )

    # Define the data for brightness host
    brightness_data_host = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                    'Positions': [min_brightness_host, client_post['brightness'], max_brightness_host]})
    brightness_legend_labels_host = {'Min': 'Minimum', 'Yours': "Your Image's", 'Max': 'Maximum'}
    brightness_data_host['Values'] = brightness_data_host['Values'].map(brightness_legend_labels_host)

    # Create the number line plot for brightness host
    brightness_number_line_host = alt.Chart(brightness_data_host).mark_point(size=50, filled=True).encode(
        x='Positions:Q',
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Brightness")),
        tooltip='Positions:N'
    ).properties(
        width=400,
        height=100
    )
    
    # Define the data for contrast host (similar to brightness)
    contrast_data_host = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                              'Positions': [min_contrast_host, client_post['contrast'], max_contrast_host]})
    contrast_legend_labels_host = {'Min': 'Minimum', 'Yours': "Your Image's", 'Max': 'Maximum'}
    contrast_data_host['Values'] = contrast_data_host['Values'].map(contrast_legend_labels_host)

    # Create the number line plot for contrast host
    contrast_number_line_host = alt.Chart(contrast_data_host).mark_point(size=50, filled=True).encode(
        x='Positions:Q',
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Contrast")),
        tooltip='Positions:N'
    ).properties(
        width=400,
        height=100
    )
    
    # Define the data for saturation host (similar to brightness)
    saturation_data_host = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                'Positions': [min_saturation_host, client_post['saturation'], max_saturation_host]})
    saturation_legend_labels_host = {'Min': 'Minimum', 'Yours': "Your Image's", 'Max': 'Maximum'}
    saturation_data_host['Values'] = saturation_data_host['Values'].map(saturation_legend_labels_host)
    
    # Create the number line plot for saturation host
    saturation_number_line_host = alt.Chart(saturation_data_host).mark_point(size=50, filled=True).encode(
        x='Positions:Q',
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Saturation")),
        tooltip='Positions:N'
    ).properties(
        width=400,
        height=100
    )

    # Define the data for shadow host (similar to brightness)
    shadow_data_host = pd.DataFrame({'Values': ['Min', 'Yours', 'Max'], 
                                'Positions': [min_shadows_host, client_post['shadows'], max_shadows_host]})
    shadow_legend_labels_host = {'Min': 'Minimum Shadow', 'Yours': "Your Image's", 'Max': 'Maximum Shadow'}
    shadow_data_host['Values'] = shadow_data_host['Values'].map(shadow_legend_labels_host)

    # Create the number line plot for shadow host
    shadow_number_line_host = alt.Chart(shadow_data_host).mark_point(size=50, filled=True).encode(
        x='Positions:Q',
        y=alt.value(0),
        color=alt.Color('Values:N', legend=alt.Legend(title="Shadow")),
        tooltip='Positions:N'
    ).properties(
        width=400,
        height=100
    )

    col1, col2 = st.columns(2)

    with col1:
        st.header("Competitor Analysis")

        # Brightness
        st.subheader("Brightness")
        if brightness_in_range_comp:
            b_brightness_comp = st.checkbox('Select', key='checkbox_brightness_comp')  
            st.success(brightness_recommendation_comp)
        else:
            b_brightness_comp = st.checkbox('Select', key='checkbox_brightness_comp')  
            st.error(brightness_recommendation_comp)
        st.altair_chart(brightness_number_line_comp, use_container_width=True)

        # Saturation
        st.subheader("Saturation")
        if saturation_in_range_comp:
            b_saturation_comp = st.checkbox('Select', key='checkbox_saturation_comp')  
            st.success(saturation_recommendation_comp)
        else:
            b_saturation_comp = st.checkbox('Select', key='checkbox_saturation_comp')  
            st.error(saturation_recommendation_comp)
        st.altair_chart(saturation_number_line_comp, use_container_width=True)
        
        # Contrast
        st.subheader("Contrast")
        if contrast_in_range_comp:
            b_contrast_comp = st.checkbox('Select', key='checkbox_contrast_comp')  
            st.success(contrast_recommendation_comp)
        else:
            b_contrast_comp = st.checkbox('Select', key='checkbox_contrast_comp')  
            st.error(contrast_recommendation_comp)
        st.altair_chart(contrast_number_line_comp, use_container_width=True)

        # Shadows
        st.subheader("Shadows")
        if shadows_in_range_comp:
            b_shadows_comp = st.checkbox('Select', key='checkbox_shadows_comp')  
            st.success(shadow_recommendation_comp)
        else:
            b_shadows_comp = st.checkbox('Select', key='checkbox_shadows_comp')  
            st.error(shadow_recommendation_comp)
        st.altair_chart(shadow_number_line_comp, use_container_width=True)

        #Colors
        st.subheader("Colors")
        b_colors_comp = st.checkbox('Select', key='checkbox_colors_comp')  
        st.error(colors_recommendation_comp)
        
        #Text
        st.subheader("Text")
        if not text_present_comp:
            b_text_comp = st.checkbox('Select', key='checkbox_text_comp')  
            st.success(text_recommendation_comp)
        else:
            b_text_comp = st.checkbox('Select', key='checkbox_text_comp')  
            st.error(text_recommendation_comp)

    with col2:
        st.header("Customer Analysis")

        # Brightness
        st.subheader("Brightness")
        if brightness_in_range_host:
            b_brightness_host = st.checkbox('Select', key='checkbox_brightness_host')  
            st.success(brightness_recommendation_host)
        else:
            b_brightness_host = st.checkbox('Select', key='checkbox_brightness_host')  
            st.error(brightness_recommendation_host)
        st.altair_chart(brightness_number_line_host, use_container_width=True)

        # Saturation
        st.subheader("Saturation")
        if saturation_in_range_host:
            b_saturation_host = st.checkbox('Select', key='checkbox_saturation_host')  
            st.success(saturation_recommendation_host)
        else:
            b_saturation_host = st.checkbox('Select', key='checkbox_saturation_host')  
            st.error(saturation_recommendation_host)
        st.altair_chart(saturation_number_line_host, use_container_width=True)

        # Contrast
        st.subheader("Contrast")
        if contrast_in_range_host:
            b_contrast_host = st.checkbox('Select', key='checkbox_contrast_host')  
            st.success(contrast_recommendation_host)
        else:
            b_contrast_host = st.checkbox('Select', key='checkbox_contrast_host')  
            st.error(contrast_recommendation_host)
        st.altair_chart(contrast_number_line_host, use_container_width=True)

        # Shadows
        st.subheader("Shadows")
        if shadows_in_range_host:
            b_shadows_host = st.checkbox('Select', key='checkbox_shadows_host')  
            st.success(shadow_recommendation_host)
        else:
            b_shadows_host = st.checkbox('Select', key='checkbox_shadows_host')  
            st.error(shadow_recommendation_host)
        st.altair_chart(shadow_number_line_host, use_container_width=True)

        st.subheader("Colors")
        b_colors_host = st.checkbox('Select', key='checkbox_colors_host')  
        st.error(colors_recommendation_host)

        st.subheader("Text")
        if not text_present_host:
            b_text_host = st.checkbox('Select', key='checkbox_text_host')  
            st.success(text_recommendation_host)
        else:
            b_text_host = st.checkbox('Select', key='checkbox_text_host')  
            
            st.error(text_recommendation_host)
    # return checkboxes values
    return (b_brightness_comp, b_saturation_comp, b_contrast_comp, b_shadows_comp, b_brightness_host, b_saturation_host, b_contrast_host, b_shadows_host, b_text_comp, b_text_host, b_colors_comp, b_colors_host,
            results_comp, color_mapping_comp, text_present_comp, results_host, color_mapping_host, text_present_host,
            brightness_in_range_comp, shadows_in_range_comp, saturation_in_range_comp, contrast_in_range_comp, brightness_in_range_host, shadows_in_range_host, saturation_in_range_host, contrast_in_range_host, colors_recommendation_comp, colors_recommendation_host, text_present_comp, text_recommendation_comp, text_recommendation_host)

    # return (brightness_in_range_comp, shadows_in_range_comp, saturation_in_range_comp, 
    #         contrast_in_range_comp, results_comp, color_mapping_comp, text_present_comp), (
    #        brightness_in_range_host, shadows_in_range_host, saturation_in_range_host, 
    #        contrast_in_range_host, results_host, color_mapping_host, text_present_host)