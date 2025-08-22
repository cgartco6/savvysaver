#!/usr/bin/env python3
"""
Content Creator AI Agent
Generates marketing content for SavvySaver
"""

import openai
import requests
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

class ContentCreator:
    def __init__(self):
        # Initialize OpenAI API (you would need to set up your API key)
        openai.api_key = os.getenv("OPENAI_API_KEY")
        
    def generate_text_content(self, topic):
        """Generate marketing text using GPT-3"""
        prompt = f"Create a engaging social media post about {topic} for SavvySaver, an app that helps businesses save money by scanning receipts and comparing prices from different food distributors. The post should be compelling and encourage restaurants, hotels, and shop owners to sign up."
        
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7
            )
            
            return response.choices[0].text.strip()
        except Exception as e:
            print(f"Error generating text: {e}")
            return f"Discover how SavvySaver can help your business save money on food supplies! Scan receipts and compare prices to maximize your profits. Download now! #SavvySaver #BusinessTips #CostSaving"
    
    def create_image(self, text, filename):
        """Create a marketing image with text"""
        # Create a blank image with a background
        img = Image.new('RGB', (1080, 1080), color=(47, 49, 54))
        d = ImageDraw.Draw(img)
        
        # Load a font
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Wrap text
        lines = textwrap.wrap(text, width=30)
        
        # Draw text on image
        y_text = 400
        for line in lines:
            width, height = font.getsize(line)
            d.text(((1080 - width) / 2, y_text), line, font=font, fill=(255, 255, 255))
            y_text += height + 10
        
        # Add logo
        try:
            logo = Image.open("logo.png")
            logo.thumbnail((200, 200))
            img.paste(logo, (440, 150), logo)
        except:
            pass
        
        # Save image
        img.save(f"content/{filename}")
        return f"content/{filename}"
    
    def create_daily_content(self):
        """Create all content for the day"""
        topics = [
            "saving money on food supplies",
            "maximizing restaurant profits",
            "comparing prices between distributors",
            "business cost reduction strategies"
        ]
        
        content = []
        
        for i, topic in enumerate(topics):
            # Generate text
            text = self.generate_text_content(topic)
            
            # Create image
            image_path = self.create_image(text, f"daily_content_{i}.jpg")
            
            content.append({
                "text": text,
                "image_path": image_path,
                "topic": topic
            })
        
        return content

if __name__ == "__main__":
    creator = ContentCreator()
    content = creator.create_daily_content()
    print("Created content:", content)
