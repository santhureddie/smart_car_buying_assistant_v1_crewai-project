#!/usr/bin/env python
"""
Test script to verify the website components are working correctly
"""

import os
import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from smart_car_buying_assistant.crew import SmartCarBuyingAssistantCrew
        print("✅ CrewAI module imported successfully")
    except ImportError as e:
        print(f"❌ CrewAI import failed: {e}")
        return False
    
    return True

def test_templates():
    """Test if template files exist"""
    print("\n📄 Testing template files...")
    
    templates_dir = "templates"
    required_files = ["index.html", "results.html"]
    
    if not os.path.exists(templates_dir):
        print(f"❌ Templates directory '{templates_dir}' not found")
        return False
    
    for file in required_files:
        file_path = os.path.join(templates_dir, file)
        if os.path.exists(file_path):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            return False
    
    return True

def test_app_creation():
    """Test if the Flask app can be created"""
    print("\n🚀 Testing Flask app creation...")
    
    try:
        # Add src to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        # Import the app
        from app import app
        print("✅ Flask app created successfully")
        
        # Test basic app properties
        if hasattr(app, 'routes'):
            print("✅ App has routes configured")
        else:
            print("⚠️  App routes not verified")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app.py",
        "run_website.py", 
        "requirements.txt",
        "WEBSITE_README.md"
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} found")
        else:
            print(f"❌ {file} not found")
            return False
    
    return True

def main():
    """Run all tests"""
    print("🧪 Testing Smart Car Buying Assistant Website")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Template Files", test_templates),
        ("Module Imports", test_imports),
        ("Flask App Creation", test_app_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔧 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The website should work correctly.")
        print("\n🚀 To start the website, run:")
        print("   python run_website.py")
        print("\n🌐 Then open your browser to: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
