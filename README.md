# Python Instagram Follower Analysis Tool

This Python script helps you analyze your Instagram followers and identify users who:

*   You follow but don't follow you back.
*   Follow you but you don't follow back.

## Prerequisites

*   Python 3.6+
*   `requests` library (install with `pip install requests`)
*   `tqdm` library (install with `pip install tqdm`) - for progress bars

## Setup

1.  **Clone the repository or copy the .py file:**

    ```bash
    git clone https://github.com/romflorod/python_instagram_followers_not_following/
    cd python_instagram_followers_not_following/
    ```

2.  **Install the required libraries:**

    ```bash
    pip install requests tqdm
    ```

3.  **Configure your Instagram session cookie:**

    *   Open your Instagram account in a web browser (e.g., Chrome, Firefox).
    *   Open the browser's developer tools (usually by pressing F12).
    *   Go to the "Network" tab.
    *   Refresh the page.
    *   Find any request to Instagram (e.g., a request to your profile).
    *   Look at the request headers.
    *   Copy the entire value of the `cookie` header.  This is a long string of key-value pairs separated by semicolons.
    *   In the `insta.py` file, replace the cookie value with the one you copied:

        ```python
        COOKIES = {
            'cookie': 'YOUR_INSTAGRAM_COOKIE_HERE'
        }
        ```

        **Important:** This cookie is essential for authenticating with Instagram. It expires periodically, so you'll need to update it regularly (e.g., every few days or weeks) by repeating the process above.

4.  **Set your username:**

    *   In the `insta.py` file, replace `"tazuhslowfi"` with your Instagram username:

        ```python
        username = "your_username"
        ```

## Usage

1.  **Run the script:**

    ```bash
    python insta.py
    ```

2.  **Output:**

    The script will show real-time progress bars while fetching data and will save results to the `results` directory:

    *   `followers.txt/json`:  List of your followers.
    *   `following.txt/json`:  List of accounts you are following.
    *   `dont_follow_me_back.txt/json`: List of accounts you follow that don't follow you back.
    *   `i_dont_follow_back.txt/json`: List of accounts that follow you that you don't follow back.

    Each text file contains the username and full name, separated by a comma:

    ```
    username1,Full Name 1
    username2,Full Name 2
    ...
    ```

## Features

*   Progress bars to track data retrieval in real-time
*   Rate limiting protection with configurable delay between requests
*   Output in both text and JSON formats
*   Efficient user comparison using set operations
*   Comprehensive error handling
*   Automatic creation of output directory

## Important Considerations

*   **Cookie Expiration:** Instagram session cookies expire. You'll need to update the cookie in your script regularly.
*   **Rate Limiting:** Instagram has rate limits. The script implements a 1-second delay between requests to help avoid rate limiting.
*   **Terms of Service:** Scraping Instagram may violate their terms of service. Be careful and respectful of their policies.
*   **Security:** Be careful about exposing your cookie or other sensitive information. Avoid committing it to public repositories.
*   **Disclaimer:** Use this script at your own risk. The author is not responsible for any consequences resulting from its use.
