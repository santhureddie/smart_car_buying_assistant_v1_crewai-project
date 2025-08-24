#!/usr/bin/env python
"""
Simple status checker for the Smart Car Buying Assistant website
"""

import requests
import json
import time

def check_website_status():
    """Check if the website is running and healthy"""
    try:
        # Check health endpoint
        response = requests.get('http://localhost:5000/health', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("🌐 Website Status:")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Environment: {data.get('environment', 'unknown')}")
            print(f"   Crew Available: {data.get('crew_available', 'unknown')}")
            return True
        else:
            print(f"❌ Website returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Website is not running or not accessible")
        print("💡 Start the website with: python run_website.py")
        return False
    except Exception as e:
        print(f"❌ Error checking website status: {e}")
        return False

def check_session_status(session_id):
    """Check the status of a specific session"""
    try:
        response = requests.get(f'http://localhost:5000/status/{session_id}', timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📊 Session {session_id} Status:")
            print(f"   Status: {data.get('status', 'unknown')}")
            print(f"   Progress: {data.get('progress', 0)}%")
            print(f"   Current Task: {data.get('current_task', 'unknown')}")
            if data.get('error'):
                print(f"   Error: {data.get('error')}")
            return True
        else:
            print(f"❌ Session not found or error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error checking session status: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Smart Car Buying Assistant - Status Checker")
    print("=" * 50)
    
    # Check website status
    if check_website_status():
        print("\n✅ Website is running and healthy!")
        
        # Ask if user wants to check a specific session
        session_id = input("\n📝 Enter session ID to check (or press Enter to skip): ").strip()
        if session_id:
            check_session_status(session_id)
    else:
        print("\n❌ Website is not running properly")
        print("\n💡 Troubleshooting steps:")
        print("1. Make sure you have set your OpenAI API key")
        print("2. Run: python debug_website.py")
        print("3. Start the website: python run_website.py")

if __name__ == "__main__":
    main()
