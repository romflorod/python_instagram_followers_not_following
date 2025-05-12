import requests
import json
import urllib.parse

username = "your user"  # Replace with the target username
# Replace with your actual cookie
COOKIES = {
    'cookie': 'datr=XXX; ig_did=XXX; mid=XX;dad21d57428c0507471d ... ... sessionid=XXX
}

def get_user_id(username):
    """Retrieves the user ID from Instagram."""
    url = f"https://www.instagram.com/web/search/topsearch/?query={username}"
    response = requests.get(url, headers=COOKIES)
    response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
    data = response.json()
    for user in data['users']:
        if user['user']['username'] == username:
            return user['user']['pk']
    return None

def get_followers(user_id, after=None):
    """Retrieves followers for a given user ID."""
    query_hash = "c76146de99bb02f6415203be841dd25a"
    variables = {
        "id": user_id,
        "include_reel": True,
        "fetch_mutual": True,
        "first": 50,
        "after": after
    }
    url = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={urllib.parse.quote(json.dumps(variables))}"
    response = requests.get(url, headers=COOKIES)
    response.raise_for_status()
    data = response.json()
    return data

def get_following(user_id, after=None):
    """Retrieves those the user is following for a given user ID."""
    query_hash = "d04b0a864b4b54837c0d870b0e77e076"
    variables = {
        "id": user_id,
        "include_reel": True,
        "fetch_mutual": True,
        "first": 50,
        "after": after
    }
    url = f"https://www.instagram.com/graphql/query/?query_hash={query_hash}&variables={urllib.parse.quote(json.dumps(variables))}"
    response = requests.get(url, headers=COOKIES)
    response.raise_for_status()
    data = response.json()
    return data

def save_users_to_txt(filename, user_list):
    """Saves a list of users to a text file."""
    with open(filename, 'w', encoding='utf-8') as f:
        for user in user_list:
            f.write(f"{user['username']},{user['full_name']}\n")

def main():
    """Main function to orchestrate the scraping."""
    try:
        print("Process started! Give it a couple of seconds...")

        user_id = get_user_id(username)
        if not user_id:
            print(f"User '{username}' not found.")
            return

        followers = []
        after = None
        has_next = True

        while has_next:
            followers_data = get_followers(user_id, after)
            has_next = followers_data['data']['user']['edge_followed_by']['page_info']['has_next_page']
            after = followers_data['data']['user']['edge_followed_by']['page_info']['end_cursor']
            edges = followers_data['data']['user']['edge_followed_by']['edges']
            followers.extend([{'username': node['node']['username'], 'full_name': node['node']['full_name']} for node in edges])

        print(f"Followers generated")
        save_users_to_txt('followers.txt', followers)  # Save followers to file

        following = []
        after = None
        has_next = True

        while has_next:
            following_data = get_following(user_id, after)
            has_next = following_data['data']['user']['edge_follow']['page_info']['has_next_page']
            after = following_data['data']['user']['edge_follow']['page_info']['end_cursor']
            edges = following_data['data']['user']['edge_follow']['edges']
            following.extend([{'username': node['node']['username'], 'full_name': node['node']['full_name']} for node in edges])

        print(f"Following generated")
        save_users_to_txt('following.txt', following)  # Save following to file

        dont_follow_me_back = [f for f in following if f['username'] not in [follower['username'] for follower in followers]]
        i_dont_follow_back = [f for f in followers if f['username'] not in [followee['username'] for followee in following]]

        print(f"Don't Follow Me Back generated")
        save_users_to_txt('dont_follow_me_back.txt', dont_follow_me_back)  # Save to file
        print(f"I Don't Follow Back generated")
        save_users_to_txt('i_dont_follow_back.txt', i_dont_follow_back)  # Save to file

        print("Process is done!")

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except (KeyError, TypeError) as e:
        print(f"Error processing JSON: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
