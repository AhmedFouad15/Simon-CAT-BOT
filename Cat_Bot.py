import tweepy 
import time
from telegram import Bot 
 
API_KEY = "My API KEY" 
API_SECRET = "My API Secret Key" 
ACCESS_TOKEN = "My Access Token" 
ACCESS_TOKEN_SECRET = "My Access token S" 

# Users ID
specific_users = ['user1', 'user2'] 

# Keywords to filter
keywords = ['$CAT', 'Memecoin', '$Cat', 'Simon cat', 'memes', 'memecoins', 'cat', 'Cat', 'CAT', 'meme'] 
Simon_CAT_keywords = ['$CAT', '#Simon_Cat_Token', '$Cat', 'Simon cat'] 

def fetch_and_filter_posts(api, users, keywords,Simon_CAT_keywords, min_followers=10000): 
    posts = [] 
    # Fetch from specific Influencers 
    for user in users: 
        user_posts = api.user_timeline(screen_name=user)
        for post in user_posts: 
            if any(keyword in post.text for keyword in keywords): 
                posts.append(post) 

    # Search for general posts 
    search_posts = api.search_tweets(q=" ".join(Simon_CAT_keywords), result_type="recent") 

    for post in search_posts['statuses']: 
        if post.user.followers_count > min_followers: 
           posts.append(post) 

    return posts 
        
#Function to send Telegram message 
def send_telegram_message(message): 
    bot = Bot(token=TELEGRAM_TOKEN) 
    bot.send_message(chat_id=CHAT_ID, text=message) 

# Telegram Bot Data
TELEGRAM_TOKEN = "MY Telegram Token" 
CHAT_ID = "My Chat ID" 

def main():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET) 
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET) 
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)  # Wait on rate limit to avoid hitting limits too quickly

    while True:
        try:
            filtered_posts = fetch_and_filter_posts(api, specific_users, keywords, Simon_CAT_keywords)
            for post in filtered_posts:
                message = f"New post from {post.user.screen_name}: {post.text[:50]}... Read more at: {post.full_text}" 
                send_telegram_message(message)
            time.sleep(300)  # Wait for 5 minutes before checking again

        except tweepy.TweepError as e:
            print(f"An error occurred: {e}")
            time.sleep(600)  # Wait longer if an error occurs, e.g., 10 minutes

        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(600)  # General error handling

if __name__ == "__main__":
    main()
