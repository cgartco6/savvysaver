#!/usr/bin/env python3
"""
Social Poster AI Agent
Automatically posts content to social media platforms
"""

import tweepy
import facebook
import requests
import time
import os

class SocialPoster:
    def __init__(self):
        # Initialize API keys (you would need to set these up for each platform)
        self.twitter_api_key = os.getenv("TWITTER_API_KEY")
        self.twitter_api_secret = os.getenv("TWITTER_API_SECRET")
        self.twitter_access_token = os.getenv("TWITTER_ACCESS_TOKEN")
        self.twitter_access_secret = os.getenv("TWITTER_ACCESS_SECRET")
        
        self.facebook_access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
        self.facebook_page_id = os.getenv("FACEBOOK_PAGE_ID")
        
        # Initialize APIs
        self.twitter_auth = tweepy.OAuthHandler(self.twitter_api_key, self.twitter_api_secret)
        self.twitter_auth.set_access_token(self.twitter_access_token, self.twitter_access_secret)
        self.twitter_api = tweepy.API(self.twitter_auth)
        
        self.facebook_graph = facebook.GraphAPI(self.facebook_access_token)
    
    def post_to_twitter(self, text, image_path=None):
        """Post content to Twitter"""
        try:
            if image_path:
                media = self.twitter_api.media_upload(image_path)
                self.twitter_api.update_status(status=text, media_ids=[media.media_id])
            else:
                self.twitter_api.update_status(status=text)
            print("Posted to Twitter successfully")
            return True
        except Exception as e:
            print(f"Error posting to Twitter: {e}")
            return False
    
    def post_to_facebook(self, text, image_path=None):
        """Post content to Facebook"""
        try:
            if image_path:
                self.facebook_graph.put_photo(
                    image=open(image_path, 'rb'),
                    message=text,
                    album_id=self.facebook_page_id
                )
            else:
                self.facebook_graph.put_object(
                    self.facebook_page_id,
                    "feed",
                    message=text
                )
            print("Posted to Facebook successfully")
            return True
        except Exception as e:
            print(f"Error posting to Facebook: {e}")
            return False
    
    def post_to_instagram(self, text, image_path):
        """Post content to Instagram"""
        # Note: Instagram API has stricter requirements
        # This is a simplified version
        try:
            # In a real implementation, you would use the Instagram Graph API
            print(f"Would post to Instagram: {text} with image {image_path}")
            return True
        except Exception as e:
            print(f"Error posting to Instagram: {e}")
            return False
    
    def post_content(self, content):
        """Post all content to social media platforms"""
        results = []
        
        for item in content:
            text = item['text']
            image_path = item['image_path']
            
            # Space out posts to avoid rate limiting
            time.sleep(10)
            
            # Post to Twitter
            twitter_result = self.post_to_twitter(text, image_path)
            
            # Post to Facebook
            time.sleep(10)
            facebook_result = self.post_to_facebook(text, image_path)
            
            # Post to Instagram
            time.sleep(10)
            instagram_result = self.post_to_instagram(text, image_path)
            
            results.append({
                'content': item,
                'twitter': twitter_result,
                'facebook': facebook_result,
                'instagram': instagram_result
            })
        
        return results

if __name__ == "__main__":
    poster = SocialPoster()
    
    # Test with sample content
    sample_content = [{
        'text': 'Test post from SavvySaver AI Agent!',
        'image_path': 'test_image.jpg',
        'topic': 'test'
    }]
    
    results = poster.post_content(sample_content)
    print("Posting results:", results)
