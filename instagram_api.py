import instaloader
import os
import json
from secrets import INSTAGRAM_LOGIN, INSTAGRAM_PASSWORD

L = instaloader.Instaloader()
username = INSTAGRAM_LOGIN
password = INSTAGRAM_PASSWORD

L.login(username, password)

def scrape_data(username):

    profile = instaloader.Profile.from_username(L.context, username)
    # create folder
    if not os.path.exists(f"posts_{username}"):
        os.makedirs(f"posts_{username}")


    limit = 10 # to be adapted
    posts_ = profile.get_posts()
    i = 0
    for post in posts_:
        if i > limit:
            break
        i += 1
        # save locally
        L.download_post(post, f"posts_{username}")
        data = {
            "caption": post.caption,
            "likes": post.likes,
            "comments": post.comments,
            "location": post.location,
            "date": post.date.isoformat(),
            "url": post.url
        }

        with open(f"posts_{username}/data.json", "w") as f:
            json.dump(data, f)


def profile_stats(username):
    profile = instaloader.Profile.from_username(L.context, username)

    # store as a json
    data = {
        "username": profile.username,
        "followers": profile.followers,
        "following": profile.followees,
        "bio": profile.biography,
        "posts": profile.mediacount
    }

    # save as json
    with open(f"stats_{username}.json", "w") as f:
        json.dump(data, f)



if __name__ == "__main__":
    scrape_data("cristiano")
