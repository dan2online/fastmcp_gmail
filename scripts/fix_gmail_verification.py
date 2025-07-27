#!/usr/bin/env python3
"""
Quick fix script for Gmail API verification issues
"""

import os
import sys
import webbrowser
from urllib.parse import quote


def main():
    print("🚨 Gmail API Access Blocked - Quick Fix Guide")
    print("=" * 50)

    print("\n📋 The 'Access blocked' error occurs because your app needs verification.")
    print("Here are 3 ways to fix this:\n")

    print("1️⃣  **EASIEST FIX** - Add yourself as test user:")
    print("   • Go to Google Cloud Console OAuth consent screen")
    print("   • Add your Gmail address in 'Test users' section")
    print("   • This allows you to use the app without verification")

    print("\n2️⃣  Use 'Internal' app type (Google Workspace only):")
    print("   • Change app type from 'External' to 'Internal'")
    print("   • Bypasses verification requirements completely")

    print("\n3️⃣  Request verification (for production use):")
    print("   • Submit app for Google verification")
    print("   • Takes 1-2 weeks for approval")
    print("   • Required for public/production apps")

    print("\n🔗 Quick Links:")

    # Generate direct links
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID", "YOUR_PROJECT_ID")
    oauth_url = f"https://console.cloud.google.com/apis/credentials/consent?project={project_id}"
    credentials_url = (
        f"https://console.cloud.google.com/apis/credentials?project={project_id}"
    )

    print(f"   • OAuth Consent Screen: {oauth_url}")
    print(f"   • Credentials: {credentials_url}")
    print(
        "   • Gmail API Library: https://console.cloud.google.com/apis/library/gmail.googleapis.com"
    )

    print("\n🎯 Recommended Steps:")
    print("1. Open OAuth consent screen link above")
    print("2. Scroll to 'Test users' section")
    print("3. Click 'Add users'")
    print("4. Add your Gmail address")
    print("5. Save changes")
    print("6. Run 'make auth-setup' again")

    # Ask if user wants to open links
    response = input(
        "\n🌐 Open Google Cloud Console OAuth screen in browser? (y/n): "
    ).lower()
    if response in ["y", "yes"]:
        try:
            webbrowser.open(oauth_url)
            print("✅ Opened OAuth consent screen in browser")
        except Exception as e:
            print(f"❌ Could not open browser: {e}")
            print(f"Please manually visit: {oauth_url}")

    print("\n💡 Once you've added yourself as a test user, run:")
    print("   make auth-setup")
    print("   # OR")
    print("   make test-gmail")


if __name__ == "__main__":
    main()
