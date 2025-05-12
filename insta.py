import requests
import json
import urllib.parse
import time
import os
from tqdm import tqdm  # For progress bars - install with pip install tqdm

username = "your user"  # Replace with the target username
# Replace with your actual cookie
COOKIES = {
    'cookie': 'datr=XXX; ig_did=XXX; mid=XX;dad21d57428c0507471d ... ... sessionid=XXX
}


# Constants
OUTPUT_DIR = "results"
DELAY_BETWEEN_REQUESTS = 1  # Seconds to wait between API calls

def create_output_dir():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}")

def get_user_id(username):
    """Retrieves the user ID from Instagram."""
    url = f"https://www.instagram.com/web/search/topsearch/?query={username}"
    try:
        response = requests.get(url, headers=COOKIES)
        response.raise_for_status()
        data = response.json()
        
        for user in data.get('users', []):
            if user['user']['username'] == username:
                return user['user']['pk']
        
        print(f"Username '{username}' not found in search results")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching user ID: {e}")
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
    time.sleep(DELAY_BETWEEN_REQUESTS)  # Add delay to avoid rate limiting
    return response.json()

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
    time.sleep(DELAY_BETWEEN_REQUESTS)  # Add delay to avoid rate limiting
    return response.json()

def save_users_to_txt(filename, user_list):
    """Saves a list of users to a text file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        for user in user_list:
            f.write(f"{user['username']},{user['full_name']}\n")
    print(f"Saved {len(user_list)} users to {filepath}")

def save_users_to_json(filename, user_list):
    """Saves a list of users to a JSON file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(user_list, f, indent=2)
    print(f"Saved {len(user_list)} users to {filepath}")

def fetch_all_users(fetch_function, user_id, description):
    """Generic function to fetch all users from paginated API."""
    results = []
    after = None
    has_next = True
    page = 1
    
    with tqdm(desc=f"Fetching {description}", unit="page") as progress:
        while has_next:
            data = fetch_function(user_id, after)
            
            # Handle different response structures based on the fetch function
            if "edge_followed_by" in data.get("data", {}).get("user", {}):
                page_info = data["data"]["user"]["edge_followed_by"]["page_info"]
                edges = data["data"]["user"]["edge_followed_by"]["edges"]
            else:  # Assuming it's following data
                page_info = data["data"]["user"]["edge_follow"]["page_info"]
                edges = data["data"]["user"]["edge_follow"]["edges"]
            
            has_next = page_info["has_next_page"]
            after = page_info["end_cursor"]
            
            results.extend([{
                'username': node['node']['username'], 
                'full_name': node['node']['full_name']
            } for node in edges])
            
            progress.update(1)
            progress.set_postfix({"users": len(results)})
            page += 1
            
    return results

def analyze_relationships(followers, following):
    """Analyze and return relationship data between followers and following."""
    # Convert to sets for more efficient lookup
    follower_usernames = {user['username'] for user in followers}
    following_usernames = {user['username'] for user in following}
    
    # Find users who don't follow back
    dont_follow_me_back_usernames = following_usernames - follower_usernames
    dont_follow_me_back = [user for user in following if user['username'] in dont_follow_me_back_usernames]
    
    # Find users I don't follow back
    i_dont_follow_back_usernames = follower_usernames - following_usernames
    i_dont_follow_back = [user for user in followers if user['username'] in i_dont_follow_back_usernames]
    
    return dont_follow_me_back, i_dont_follow_back

def main():
    """Main function to orchestrate the scraping."""
    try:
        print(f"🚀 Starting Instagram follower analysis for @{username}")
        create_output_dir()
        
        # Get user ID
        user_id = get_user_id(username)
        if not user_id:
            print("❌ Could not retrieve user ID. Process aborted.")
            return
        
        print(f"📊 User ID found: {user_id}")
        
        # Fetch followers
        followers = fetch_all_users(get_followers, user_id, "followers")
        print(f"✅ Found {len(followers)} followers")
        save_users_to_txt('followers.txt', followers)
        save_users_to_json('followers.json', followers)
        
        # Fetch following
        following = fetch_all_users(get_following, user_id, "following")
        print(f"✅ Found {len(following)} accounts you follow")
        save_users_to_txt('following.txt', following)
        save_users_to_json('following.json', following)
        
        # Analyze relationships
        dont_follow_me_back, i_dont_follow_back = analyze_relationships(followers, following)
        
        # Save relationship data
        print(f"✅ Found {len(dont_follow_me_back)} accounts that don't follow you back")
        save_users_to_txt('dont_follow_me_back.txt', dont_follow_me_back)
        save_users_to_json('dont_follow_me_back.json', dont_follow_me_back)
        
        print(f"✅ Found {len(i_dont_follow_back)} followers you don't follow back")
        save_users_to_txt('i_dont_follow_back.txt', i_dont_follow_back)
        save_users_to_json('i_dont_follow_back.json', i_dont_follow_back)
        
        print("✨ Process completed successfully!")
        print(f"📁 All results saved in the '{OUTPUT_DIR}' directory")

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
    except KeyError as e:
        print(f"❌ Data structure error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
