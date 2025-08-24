#!/usr/bin/env python
"""
API Key Format Validator for Smart Car Buying Assistant
"""

import os
import re
from dotenv import load_dotenv

def load_environment():
    """Load environment variables from .env file"""
    try:
        load_dotenv()
        print("✅ Loaded environment variables from .env file")
        return True
    except Exception as e:
        print(f"⚠️  Could not load .env file: {e}")
        return False

def validate_openai_key(api_key):
    """Validate OpenAI API key format"""
    if not api_key:
        return False, "API key is empty"
    
    # OpenAI API keys start with 'sk-' and can vary in length
    # Older keys: ~51 characters, newer project keys: up to 164 characters
    if not api_key.startswith('sk-'):
        return False, "OpenAI API key should start with 'sk-'"
    
    # Check length - should be reasonable (between 40 and 200 characters)
    if len(api_key) < 40:
        return False, f"OpenAI API key seems too short (current: {len(api_key)} characters)"
    elif len(api_key) > 200:
        return False, f"OpenAI API key seems too long (current: {len(api_key)} characters)"
    
    # Check for valid characters (alphanumeric, hyphens, and underscores)
    if not re.match(r'^sk-[a-zA-Z0-9-_]+$', api_key):
        return False, "OpenAI API key contains invalid characters"
    
    return True, "Valid OpenAI API key format"

def validate_serper_key(api_key):
    """Validate Serper API key format"""
    if not api_key:
        return False, "API key is empty"
    
    # Serper API keys are typically alphanumeric and 32+ characters
    if len(api_key) < 32:
        return False, f"Serper API key seems too short (current: {len(api_key)} characters)"
    
    # Check for valid characters (alphanumeric)
    if not re.match(r'^[a-zA-Z0-9]+$', api_key):
        return False, "Serper API key contains invalid characters"
    
    return True, "Valid Serper API key format"

def validate_brave_key(api_key):
    """Validate Brave API key format"""
    if not api_key:
        return False, "API key is empty"
    
    # Brave API keys are typically alphanumeric and 32+ characters
    if len(api_key) < 32:
        return False, f"Brave API key seems too short (current: {len(api_key)} characters)"
    
    # Check for valid characters (alphanumeric)
    if not re.match(r'^[a-zA-Z0-9]+$', api_key):
        return False, "Brave API key contains invalid characters"
    
    return True, "Valid Brave API key format"

def check_api_keys():
    """Check all API keys for proper formatting"""
    print("🔑 API Key Format Validator")
    print("=" * 50)
    
    # Load environment variables
    if not load_environment():
        print("❌ Could not load environment variables")
        return
    
    print("\n📋 Checking API Key Formats:")
    print("-" * 30)
    
    # Check OpenAI API Key
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        is_valid, message = validate_openai_key(openai_key)
        if is_valid:
            print(f"✅ OPENAI_API_KEY: {message}")
            print(f"   Key: {openai_key[:7]}...{openai_key[-4:]}")
        else:
            print(f"❌ OPENAI_API_KEY: {message}")
            print(f"   Key: {openai_key[:10]}...{openai_key[-10:] if len(openai_key) > 20 else ''}")
    else:
        print("❌ OPENAI_API_KEY: Not set")
    
    # Check Serper API Key
    serper_key = os.getenv('SERPER_API_KEY')
    if serper_key:
        is_valid, message = validate_serper_key(serper_key)
        if is_valid:
            print(f"✅ SERPER_API_KEY: {message}")
            print(f"   Key: {serper_key[:8]}...{serper_key[-8:]}")
        else:
            print(f"❌ SERPER_API_KEY: {message}")
            print(f"   Key: {serper_key[:10]}...{serper_key[-10:] if len(serper_key) > 20 else ''}")
    else:
        print("⚠️  SERPER_API_KEY: Not set (optional)")
    
    # Check Brave API Key
    brave_key = os.getenv('BRAVE_API_KEY')
    if brave_key:
        is_valid, message = validate_brave_key(brave_key)
        if is_valid:
            print(f"✅ BRAVE_API_KEY: {message}")
            print(f"   Key: {brave_key[:8]}...{brave_key[-8:]}")
        else:
            print(f"❌ BRAVE_API_KEY: {message}")
            print(f"   Key: {brave_key[:10]}...{brave_key[-10:] if len(brave_key) > 20 else ''}")
    else:
        print("⚠️  BRAVE_API_KEY: Not set (optional)")
    
    print("\n📊 Summary:")
    print("-" * 15)
    
    # Count valid keys
    valid_count = 0
    total_count = 0
    
    if openai_key:
        total_count += 1
        if validate_openai_key(openai_key)[0]:
            valid_count += 1
    
    if serper_key:
        total_count += 1
        if validate_serper_key(serper_key)[0]:
            valid_count += 1
    
    if brave_key:
        total_count += 1
        if validate_brave_key(brave_key)[0]:
            valid_count += 1
    
    print(f"Valid keys: {valid_count}/{total_count}")
    
    if valid_count == total_count and total_count > 0:
        print("🎉 All API keys have valid formats!")
    elif valid_count > 0:
        print("⚠️  Some API keys have format issues")
    else:
        print("❌ No valid API keys found")
    
    print("\n💡 Tips:")
    print("- OpenAI API keys should start with 'sk-' and can be 40-200 characters long")
    print("- Newer OpenAI project keys can be up to 164 characters")
    print("- Serper and Brave API keys should be alphanumeric and at least 32 characters")
    print("- Make sure there are no extra spaces or special characters")
    print("- Check your .env file for proper formatting")

def check_env_file():
    """Check the .env file format"""
    print("\n📄 Checking .env file format:")
    print("-" * 30)
    
    env_file = '.env'
    if os.path.exists(env_file):
        print(f"✅ .env file found")
        try:
            with open(env_file, 'r') as f:
                lines = f.readlines()
            
            print(f"   Total lines: {len(lines)}")
            
            for i, line in enumerate(lines, 1):
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if (value.startswith('"') and value.endswith('"')) or \
                           (value.startswith("'") and value.endswith("'")):
                            value = value[1:-1]
                        
                        print(f"   Line {i}: {key} = {value[:10]}...{value[-10:] if len(value) > 20 else ''}")
                    else:
                        print(f"   Line {i}: Invalid format (no '=' found)")
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    else:
        print(f"❌ .env file not found")
        print("💡 Create a .env file with your API keys")

if __name__ == "__main__":
    check_api_keys()
    check_env_file()
