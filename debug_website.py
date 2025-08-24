#!/usr/bin/env python
"""
Debug script to identify issues with the Smart Car Buying Assistant website
"""

import os
import sys
import traceback

def check_python_version():
    """Check Python version"""
    print("🐍 Python Version Check")
    print(f"   Python version: {sys.version}")
    if sys.version_info >= (3, 10) and sys.version_info < (3, 14):
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python version should be >= 3.10 and < 3.14")
        return False

def check_environment_variables():
    """Check environment variables"""
    print("\n🔑 Environment Variables Check")
    
    required_vars = ['OPENAI_API_KEY']
    optional_vars = ['SERPER_API_KEY', 'BRAVE_API_KEY']
    
    all_good = True
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {'*' * min(len(value), 8)}...")
        else:
            print(f"   ❌ {var}: Not set")
            all_good = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"   ✅ {var}: {'*' * min(len(value), 8)}...")
        else:
            print(f"   ⚠️  {var}: Not set (optional)")
    
    return all_good

def check_imports():
    """Check if all required modules can be imported"""
    print("\n📦 Import Check")
    
    imports_to_test = [
        ('flask', 'Flask'),
        ('crewai', 'CrewAI'),
        ('openai', 'OpenAI'),
    ]
    
    all_good = True
    
    for module, name in imports_to_test:
        try:
            __import__(module)
            print(f"   ✅ {name} imported successfully")
        except ImportError as e:
            print(f"   ❌ {name} import failed: {e}")
            all_good = False
    
    return all_good

def check_crew_import():
    """Check if the crew module can be imported"""
    print("\n🤖 Crew Import Check")
    
    # Add src to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from smart_car_buying_assistant.crew import SmartCarBuyingAssistantCrew
        print("   ✅ Main crew imported successfully")
        return True
    except ImportError as e:
        print(f"   ⚠️  Main crew import failed: {e}")
        
        try:
            from smart_car_buying_assistant.crew_simple import SmartCarBuyingAssistantCrewSimple
            print("   ✅ Simplified crew imported successfully")
            return True
        except ImportError as e2:
            print(f"   ❌ Simplified crew import failed: {e2}")
            return False

def check_flask_app():
    """Check if Flask app can be created"""
    print("\n🌐 Flask App Check")
    
    try:
        from app import app
        print("   ✅ Flask app created successfully")
        
        # Check if app has routes
        if hasattr(app, 'url_map'):
            routes = [str(rule) for rule in app.url_map.iter_rules()]
            print(f"   ✅ App has {len(routes)} routes configured")
            for route in routes:
                print(f"      - {route}")
        else:
            print("   ⚠️  App routes not verified")
        
        return True
    except Exception as e:
        print(f"   ❌ Flask app creation failed: {e}")
        traceback.print_exc()
        return False

def check_templates():
    """Check if template files exist"""
    print("\n📄 Template Files Check")
    
    templates_dir = "templates"
    required_files = ["index.html", "results.html"]
    
    if not os.path.exists(templates_dir):
        print(f"   ❌ Templates directory '{templates_dir}' not found")
        return False
    
    all_good = True
    for file in required_files:
        file_path = os.path.join(templates_dir, file)
        if os.path.exists(file_path):
            size = os.path.getsize(file_path)
            print(f"   ✅ {file} found ({size} bytes)")
        else:
            print(f"   ❌ {file} not found")
            all_good = False
    
    return all_good

def check_file_structure():
    """Check if all required files exist"""
    print("\n📁 File Structure Check")
    
    required_files = [
        "app.py",
        "run_website.py", 
        "requirements.txt",
        "WEBSITE_README.md"
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} found ({size} bytes)")
        else:
            print(f"   ❌ {file} not found")
            all_good = False
    
    return all_good

def main():
    """Run all checks"""
    print("🔍 Smart Car Buying Assistant - Debug Check")
    print("=" * 60)
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment Variables", check_environment_variables),
        ("Module Imports", check_imports),
        ("Crew Import", check_crew_import),
        ("Flask App", check_flask_app),
        ("Template Files", check_templates),
        ("File Structure", check_file_structure),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"   ❌ {check_name} check failed with exception: {e}")
            results.append((check_name, False))
    
    print("\n" + "=" * 60)
    print("📊 Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {check_name}")
        if result:
            passed += 1
    
    print(f"\n📈 Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! The website should work correctly.")
        print("\n🚀 To start the website, run:")
        print("   python run_website.py")
        print("\n🌐 Then open your browser to: http://localhost:5000")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above before running the website.")
        
        # Provide specific guidance
        if not check_environment_variables():
            print("\n💡 To fix environment variable issues:")
            print("   set OPENAI_API_KEY=your_api_key_here")
        
        if not check_imports():
            print("\n💡 To fix import issues:")
            print("   pip install -r requirements.txt")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
