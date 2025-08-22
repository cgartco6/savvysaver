#!/usr/bin/env python3
"""
Lead Tracker AI Agent
Tracks new signups and leads for commission purposes
"""

import pandas as pd
import sqlite3
import datetime
import os

class LeadTracker:
    def __init__(self, db_path="leads.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize the database if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Create leads table
        c.execute('''CREATE TABLE IF NOT EXISTS leads
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      company_name TEXT,
                      contact_name TEXT,
                      phone TEXT,
                      email TEXT,
                      province TEXT,
                      city TEXT,
                      signup_date DATE,
                      status TEXT,
                      commission_earned REAL)''')
        
        conn.commit()
        conn.close()
    
    def add_lead(self, company_name, contact_name, phone, email, province, city):
        """Add a new lead to the database"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''INSERT INTO leads 
                     (company_name, contact_name, phone, email, province, city, signup_date, status, commission_earned)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                     (company_name, contact_name, phone, email, province, city, 
                      datetime.date.today(), 'New', 0.0))
        
        conn.commit()
        lead_id = c.lastrowid
        conn.close()
        
        return lead_id
    
    def update_lead_status(self, lead_id, status, commission_earned=0.0):
        """Update the status of a lead"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''UPDATE leads 
                     SET status = ?, commission_earned = ?
                     WHERE id = ?''',
                     (status, commission_earned, lead_id))
        
        conn.commit()
        conn.close()
    
    def get_new_leads(self):
        """Get all new leads that haven't been processed yet"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM leads WHERE status = 'New'"
        new_leads = pd.read_sql_query(query, conn)
        
        conn.close()
        return new_leads
    
    def get_leads_by_province(self):
        """Get leads grouped by province"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT province, COUNT(*) as count FROM leads GROUP BY province"
        leads_by_province = pd.read_sql_query(query, conn)
        
        conn.close()
        return leads_by_province
    
    def get_commission_report(self):
        """Generate a commission report"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT SUM(commission_earned) as total_commission FROM leads"
        total_commission = pd.read_sql_query(query, conn)
        
        query = "SELECT province, SUM(commission_earned) as commission FROM leads GROUP BY province"
        commission_by_province = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return {
            "total_commission": total_commission.iloc[0]['total_commission'],
            "by_province": commission_by_province
        }
    
    def export_to_excel(self, filename="leads_export.xlsx"):
        """Export all leads to an Excel file"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM leads"
        all_leads = pd.read_sql_query(query, conn)
        
        conn.close()
        
        # Export to Excel
        all_leads.to_excel(filename, index=False)
        return filename

if __name__ == "__main__":
    tracker = LeadTracker()
    
    # Add some test leads
    tracker.add_lead("Test Company", "John Doe", "123456789", "test@example.com", "Gauteng", "Johannesburg")
    tracker.add_lead("Another Company", "Jane Smith", "987654321", "jane@example.com", "Western Cape", "Cape Town")
    
    # Get new leads
    new_leads = tracker.get_new_leads()
    print("New leads:", new_leads)
    
    # Update a lead status
    if not new_leads.empty:
        tracker.update_lead_status(new_leads.iloc[0]['id'], 'Converted', 1000.0)
    
    # Export to Excel
    export_file = tracker.export_to_excel()
    print(f"Exported to {export_file}")
