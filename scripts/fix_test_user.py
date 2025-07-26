#!/usr/bin/env python3
"""
Step-by-step Gmail verification fix with detailed instructions
"""

import webbrowser
import sys

def main():
    print("🚨 FIXING: Gmail API Access Blocked Error")
    print("=" * 60)
    
    print("\n🎯 You need to add yourself as a TEST USER in Google Cloud Console")
    print("This is REQUIRED for external OAuth apps in testing mode.\n")
    
    print("📋 EXACT STEPS TO FIX:")
    print("-" * 30)
    
    print("1. Open Google Cloud Console OAuth Consent Screen:")
    print("   https://console.cloud.google.com/apis/credentials/consent")
    
    print("\n2. Make sure you're in the correct project:")
    print("   - Check project name at top of page")
    print("   - Should be your FastMCP Gmail project")
    
    print("\n3. Find the 'Test users' section:")
    print("   - Scroll down on the OAuth consent screen page")
    print("   - Look for 'Test users' section")
    
    print("\n4. Add your Gmail address:")
    print("   - Click '+ ADD USERS' button")
    print("   - Enter: 8888dhe@gmail.com")
    print("   - Click 'Save'")
    
    print("\n5. Verify it's added:")
    print("   - You should see '8888dhe@gmail.com' in the test users list")
    print("   - Status should show as 'Added'")
    
    print("\n6. Wait and retry:")
    print("   - Wait 1-2 minutes for changes to take effect")
    print("   - Delete any existing token: rm token.json")
    print("   - Run: make auth-setup")
    
    print("\n" + "=" * 60)
    print("🔍 TROUBLESHOOTING CHECKLIST:")
    print("=" * 60)
    
    print("❓ Can't find 'Test users' section?")
    print("   → Make sure OAuth consent screen is configured as 'External'")
    print("   → If it's 'Internal', you don't need test users")
    
    print("\n❓ Still getting access_denied after adding test user?")
    print("   → Clear browser cache and cookies")
    print("   → Try incognito/private browsing mode")
    print("   → Make sure you're signing in with 8888dhe@gmail.com")
    
    print("\n❓ Don't see the project or can't access Cloud Console?")
    print("   → Make sure you're signed in with the correct Google account")
    print("   → Check that you have owner/editor permissions on the project")
    
    # Ask to open browser
    try:
        response = input("\n🌐 Open Google Cloud Console OAuth screen now? (y/n): ").lower().strip()
        if response in ['y', 'yes']:
            oauth_url = "https://console.cloud.google.com/apis/credentials/consent"
            webbrowser.open(oauth_url)
            print("✅ Opened OAuth consent screen in browser")
            print("\nLook for 'Test users' section and add: 8888dhe@gmail.com")
        else:
            print("🔗 Manual link: https://console.cloud.google.com/apis/credentials/consent")
    except KeyboardInterrupt:
        print("\n\n🔗 Manual link: https://console.cloud.google.com/apis/credentials/consent")
    
    print("\n💡 After adding yourself as test user, run:")
    print("   rm token.json        # Clear any existing token")
    print("   make auth-setup      # Start fresh authentication")

if __name__ == "__main__":
    main()
