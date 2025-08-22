#!/usr/bin/env python3
"""
Analytics AI Agent
Tracks and analyzes marketing campaign performance
"""

import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
import datetime
import os

class Analytics:
    def __init__(self, db_path="leads.db"):
        self.db_path = db_path
    
    def get_daily_signups(self, days=30):
        """Get daily signups for the last N days"""
        conn = sqlite3.connect(self.db_path)
        
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=days)
        
        query = f"""SELECT signup_date, COUNT(*) as count 
                    FROM leads 
                    WHERE signup_date BETWEEN '{start_date}' AND '{end_date}'
                    GROUP BY signup_date
                    ORDER BY signup_date"""
        
        daily_signups = pd.read_sql_query(query, conn)
        conn.close()
        
        return daily_signups
    
    def get_conversion_rate(self):
        """Calculate conversion rate"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT status, COUNT(*) as count FROM leads GROUP BY status"
        status_counts = pd.read_sql_query(query, conn)
        
        conn.close()
        
        total_leads = status_counts['count'].sum()
        converted_leads = status_counts[status_counts['status'] == 'Converted']['count'].sum()
        
        if total_leads > 0:
            conversion_rate = (converted_leads / total_leads) * 100
        else:
            conversion_rate = 0
        
        return conversion_rate
    
    def get_province_breakdown(self):
        """Get breakdown of leads by province"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT province, COUNT(*) as count FROM leads GROUP BY province"
        province_breakdown = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return province_breakdown
    
    def calculate_roi(self, marketing_spend):
        """Calculate ROI based on commissions earned vs marketing spend"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT SUM(commission_earned) as total_commission FROM leads"
        total_commission = pd.read_sql_query(query, conn).iloc[0]['total_commission'] or 0
        
        conn.close()
        
        if marketing_spend > 0:
            roi = ((total_commission - marketing_spend) / marketing_spend) * 100
        else:
            roi = float('inf') if total_commission > 0 else 0
        
        return roi, total_commission
    
    def generate_report(self, marketing_spend=0):
        """Generate a comprehensive analytics report"""
        daily_signups = self.get_daily_signups()
        conversion_rate = self.get_conversion_rate()
        province_breakdown = self.get_province_breakdown()
        roi, total_commission = self.calculate_roi(marketing_spend)
        
        report = {
            "daily_signups": daily_signups,
            "conversion_rate": conversion_rate,
            "province_breakdown": province_breakdown,
            "roi": roi,
            "total_commission": total_commission,
            "marketing_spend": marketing_spend,
            "report_date": datetime.date.today()
        }
        
        return report
    
    def visualize_data(self, report, output_dir="analytics"):
        """Create visualizations from the report data"""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Daily signups chart
        plt.figure(figsize=(10, 6))
        plt.plot(report['daily_signups']['signup_date'], report['daily_signups']['count'])
        plt.title('Daily Signups')
        plt.xlabel('Date')
        plt.ylabel('Number of Signups')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/daily_signups.png")
        plt.close()
        
        # Province breakdown chart
        plt.figure(figsize=(10, 6))
        plt.bar(report['province_breakdown']['province'], report['province_breakdown']['count'])
        plt.title('Leads by Province')
        plt.xlabel('Province')
        plt.ylabel('Number of Leads')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f"{output_dir}/province_breakdown.png")
        plt.close()
        
        return [
            f"{output_dir}/daily_signups.png",
            f"{output_dir}/province_breakdown.png"
        ]

if __name__ == "__main__":
    analytics = Analytics()
    
    # Generate a report
    report = analytics.generate_report(marketing_spend=5000)
    print("Analytics Report:")
    print(f"Conversion Rate: {report['conversion_rate']:.2f}%")
    print(f"Total Commission: R{report['total_commission']:.2f}")
    print(f"ROI: {report['roi']:.2f}%")
    
    # Create visualizations
    charts = analytics.visualize_data(report)
    print(f"Created charts: {charts}")
