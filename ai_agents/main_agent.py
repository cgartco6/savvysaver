#!/usr/bin/env python3
"""
SavvySaver Main AI Agent
Coordinates all other AI agents for marketing and analytics
"""

import schedule
import time
from content_creator import ContentCreator
from social_poster import SocialPoster
from lead_tracker import LeadTracker
from analytics import Analytics

class MainAgent:
    def __init__(self):
        self.content_creator = ContentCreator()
        self.social_poster = SocialPoster()
        self.lead_tracker = LeadTracker()
        self.analytics = Analytics()
        
    def run_daily_tasks(self):
        """Execute all daily marketing tasks"""
        print("Starting daily marketing tasks...")
        
        # Create content
        content = self.content_creator.create_daily_content()
        
        # Post to social media
        self.social_poster.post_content(content)
        
        # Track leads and update analytics
        new_leads = self.lead_tracker.get_new_leads()
        self.analytics.update_analytics(new_leads)
        
        print("Daily marketing tasks completed!")
    
    def run_hourly_check(self):
        """Check for new leads hourly"""
        print("Checking for new leads...")
        new_leads = self.lead_tracker.get_new_leads()
        if new_leads:
            print(f"Found {len(new_leads)} new leads")
            self.analytics.update_analytics(new_leads)
    
    def schedule_tasks(self):
        """Schedule all recurring tasks"""
        # Daily marketing tasks at 9 AM
        schedule.every().day.at("09:00").do(self.run_daily_tasks)
        
        # Hourly lead checks
        schedule.every().hour.do(self.run_hourly_check)
        
        print("Scheduled tasks:")
        for job in schedule.jobs:
            print(f" - {job}")
    
    def start(self):
        """Start the main agent"""
        print("SavvySaver Main AI Agent starting...")
        self.schedule_tasks()
        
        # Run initial tasks
        self.run_daily_tasks()
        
        # Keep the agent running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    agent = MainAgent()
    agent.start()
