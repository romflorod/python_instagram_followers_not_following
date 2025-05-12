# Python Instagram Follower Analysis Tool

This Python script helps you analyze your Instagram followers and identify users who:

*   You follow but don't follow you back.
*   Follow you but you don't follow back.

## Prerequisites

*   Python 3.6+
*   `requests` library (install with `pip install requests`)

## Setup

1.  **Clone the repository or copy the .py file:**

    ```bash
    git clone https://github.com/romflorod/python_instagram_followers_not_following/
    cd https://github.com/romflorod/python_instagram_followers_not_following/
    ```

2.  **Install the `requests` library:**

    ```bash
    pip install requests
    ```

3.  **Configure your Instagram session cookie:**

    *   Open your Instagram account in a web browser (e.g., Chrome, Firefox).
    *   Open the browser's developer tools (usually by pressing F12).
    *   Go to the "Network" tab.
    *   Refresh the page.
    *   Find any request to Instagram (e.g., a request to your profile).
    *   Look at the request headers.
    *   Copy the entire value of the `cookie` header.  This is a long string of key-value pairs separated by semicolons.
    *   In the `insta.py` file, replace `"YOUR_INSTAGRAM_COOKIE_HERE"` with the cookie you copied:

        ```python
        COOKIES = {
            'cookie': 'YOUR_INSTAGRAM_COOKIE_HERE'
        }
        ```

        **Important:** This cookie is essential for authenticating with Instagram. It expires periodically, so you'll need to update it regularly (e.g., every few days or weeks) by repeating the process above.

4.  **Set your username:**

    *   In the `insta.py` file, replace `"YOUR:USER"` with your Instagram username:

        ```python
        username = "your_username"
        ```

## Usage

1.  **Run the script:**

    ```bash
    python insta.py
    ```

2.  **Output:**

    The script will print the lists of followers, following, those who don't follow you back, and those you don't follow back to the console.  It will also save these lists to separate text files in the same directory as the script:

    *   `followers.txt`:  List of your followers.
    *   `following.txt`:  List of accounts you are following.
    *   `dont_follow_me_back.txt`: List of accounts you follow that don't follow you back.
    *   `i_dont_follow_back.txt`: List of accounts that follow you that you don't follow back.

    Each line in these files contains the username and full name, separated by a comma:

    ```
    username1,Full Name 1
    username2,Full Name 2
    ...
    ```

## Important Considerations

*   **Cookie Expiration:** Instagram session cookies expire. You'll need to update the cookie in your script regularly.
*   **Rate Limiting:** Instagram has rate limits. If you make too many requests too quickly, Instagram may block your IP address.  This script does not currently implement delays, so use it with caution.
*   **Terms of Service:** Scraping Instagram may violate their terms of service. Be careful and respectful of their policies. Consider using the official Instagram API if possible, although it has its own limitations.
*   **Security:** Be careful about exposing your cookie or other sensitive information. Avoid committing it to public repositories.
*   **Disclaimer:** Use this script at your own risk. The author is not responsible for any consequences resulting from its use.
