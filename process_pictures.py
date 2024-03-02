import requests
from PIL import Image
from io import BytesIO
import pandas as pd
import base64
import json
from gpt_api import image_to_text, encode_image
import numpy as np

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


def get_prompt(username):
    return f''' This picture comes from a social media post from a restaurant (whose Instagram username is {username}). You need to analyze the picture and extract the following information, structured as a Python dictionary. Don't run any Python code to calculate scores, and output ONLY the plain dictionary, without any comments or any explanation.
    - "background_description": Description of the background of the picture
    - "objects_description": Description of the main objects present in the picture
    - "text": Is some text present in the picture? If yes, provide the text. If no, write 'No'
    - "vibe": Use a few words to describe the vibe of the picture (e.g. joyful, calm, etc.) as a list of strings
    - "colors": Extract the main colors from the picture as a list of strings
    - "contrast": Provide a value for the contrast of the picture (integer between -100 and 100, where -100 indicates a very low contrast, and 100 a very high contrast)
    - "brightness": Provide a value for the brightness of the picture (integer between -100 and 100, where -100 indicates very low brightness, and 100 a very high brightness)
    - "saturation": Provide a value for the saturation of the picture (integer between -100 and 100, where -100 indicates a very low saturation, and 100 a very high saturation)
    - "shadows": Provide a value for the presence of shadows in the picture (integer between -100 and 100, where -100 indicates no shadow, and 100 many shadows)

    For the values between -100 and 100, it can take any integer value. Make sure to have precise numbers and not always close to 0.
    '''

def get_metrics(image_url, dataframe):
    keys = ["caption", "likes", "comments", "date", "url", "likes/followers", "comments/followers", "username", "bio", "posts"]
    # get the row for the image_url
    row = dataframe.loc[dataframe['url'] == image_url]
    return {key: row[key].values[0] for key in keys}
    

def process_image(image_url, dataframe, dic):

    metrics = get_metrics(image_url, dataframe)
    username = metrics["username"]
    prompt = get_prompt(username)
    
    # Send a GET request to the image URL
    response = requests.get(dic[image_url])

    # Check if the request was successful
    if response.status_code == 200:
        # Open the image from the binary response content
        image = Image.open(BytesIO(response.content))
    
        # Define the local path where you want to save the image
        local_image_path = "dummy.jpg"
        
        # Save the image to the specified path
        image.save(local_image_path)
                
        # Encode the saved image
        encoded_image = encode_image(local_image_path)
    else:
        print("Failed to retrieve the image")

    output = image_to_text(encoded_image, prompt)
    # keep the string between { and }
    print(output)
    output = output.split("{")[1].split("}")[0]
    output = json.loads("{"+output+"}")
    # merge metrics and output
    output.update(metrics)

    # transform Nan to None
    for key in output:
        if type(output[key]) != list and pd.isna(output[key]):
            output[key] = None
    return output

    
def top3_each_account(dataframe, metrics):
    ''' Filters the dataframe and keep only the top 3 posts for each account (username) '''
    top3_df = dataframe.groupby("username").apply(lambda x: x.nlargest(3, metrics))
    return top3_df.reset_index(drop=True)

def process_dataframe(path_dataframe, top=10, metrics="likes/followers"):
    list_dics = []
    df = pd.read_csv(path_dataframe)
    df = top3_each_account(df, metrics)
    top_df = df.nlargest(top, metrics)
    #sort by likes/followers
    top_df = top_df.sort_values(by=metrics, ascending=False)
    image_url_lists = top_df['url'].tolist()
    image_url_lists_new = ["https://i.ibb.co/cCrHJBz/image.jpg", 
                        "https://i.ibb.co/8gRM1mt/image.jpg", 
                        "https://i.ibb.co/d2jZ4VR/image.jpg", 
                        "https://i.ibb.co/PjvgCqF/image.jpg", 
                        "https://i.ibb.co/8jcHYWZ/image.jpg",
                        "https://i.ibb.co/6yp9c41/image.jpg",
                        "https://i.ibb.co/gFvw6Py/image.jpg",
                        "https://i.ibb.co/R4Qck7y/image.jpg",
                        "https://i.ibb.co/4RpCkhD/image.jpg",
                        "https://i.ibb.co/tYG3r3r/image.jpg"]
    # dic to go from old link to new link
    dic = {old: new for old, new in zip(image_url_lists, image_url_lists_new)}
    for url in image_url_lists:
        print("Processing image: ", url)
        output = process_image(url, top_df, dic)
        print(output)
        list_dics.append(output)
        print("=====")
    # save dictionary in a json file
    with open("results/top5_user.json", "w") as f:
        json.dump(list_dics, f, cls=NpEncoder)
    


def process_new_post(image_path, caption, username):
    ''' Takes as input the new post (picture and caption) that must be compared to the top 5 other posts '''
    image = Image.open(image_path)
    if image.mode == 'RGBA':
        # Convert the image to RGB mode
        image = image.convert('RGB')
    image.save("dummy2.jpg")
    encoded_image = encode_image("dummy2.jpg")
    prompt = get_prompt(username)
    output = image_to_text(encoded_image, prompt)
    # keep the string between { and }
    output = output.split("{")[1].split("}")[0]
    output = json.loads("{"+output+"}")
    additional_info = {"caption": caption, "username": username}
    output.update(additional_info)
    # transform Nan to None
    for key in output:
        if type(output[key]) != list and pd.isna(output[key]):
            output[key] = None
    # save output in a json file
    with open("results/new_post.json", "w") as f:
        json.dump(output, f, cls=NpEncoder)


if __name__ == "__main__":
    # image_url = "https://scontent-bos5-1.cdninstagram.com/v/t39.30808-6/428627034_799487848875812_2385044735053402427_n.jpg?stp=dst-jpg_e15&efg=eyJ2ZW5jb2RlX3RhZyI6ImltYWdlX3VybGdlbi4xMDgweDEwODAuc2RyIn0&_nc_ht=scontent-bos5-1.cdninstagram.com&_nc_cat=108&_nc_ohc=t85-Hy5lDuYAX-nqQCu&edm=ALQROFkAAAAA&ccb=7-5&ig_cache_key=MzMwNDg4MzQxMzc5MTgzNDg0NA%3D%3D.2-ccb7-5&oh=00_AfB1B9oYkJi7qDP4bIzTijh7eVgspEVrl5LQuO6U1CpH3w&oe=65D580DB&_nc_sid=fc8dfb"
    # prompt = "Provide a long and detailed description of the image. Someone without the image should be able to clearly understand what is in the image."
    # print(process_image(image_url, "bubble_tea_store/bubble_tea_post_data.csv"))

    process_dataframe("bubble_tea_store/bubble_tea_combined_data.csv")