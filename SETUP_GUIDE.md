# 🚗 Smart Car Buying Assistant - Setup Guide

## 🔧 **Quick Fix for the Current Error**

The main issue is that your **OpenAI API key is not set**. Here's how to fix it:

### **Step 1: Get Your OpenAI API Key**

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the API key (it starts with `sk-`)

### **Step 2: Set the API Key**

**Option A: Create a .env file (Recommended)**
1. Create a file named `.env` in your project folder
2. Add this line to the file:
   ```
   OPENAI_API_KEY=sk-your_actual_api_key_here
   ```
3. Replace `sk-your_actual_api_key_here` with your real API key

**Option B: Set environment variable (Windows)**
```bash
set OPENAI_API_KEY=sk-your_actual_api_key_here
```

**Option C: Set environment variable (PowerShell)**
```powershell
$env:OPENAI_API_KEY="sk-your_actual_api_key_here"
```

### **Step 3: Test the Setup**

Run the debug script to verify everything is working:
```bash
python debug_website.py
```

You should see:
- ✅ Environment Variables
- ✅ All other checks passing

### **Step 4: Start the Website**

Once the debug script shows all checks passing:
```bash
python run_website.py
```

Then open your browser to: `http://localhost:5000`

## 🔍 **What Was Wrong**

The debug script identified these issues:
- ❌ **OPENAI_API_KEY: Not set** - This is required for CrewAI to work
- ⚠️ **SERPER_API_KEY: Not set** - Optional, for enhanced search
- ⚠️ **BRAVE_API_KEY: Not set** - Optional, for enhanced search

## 🎯 **What I Fixed**

1. **Added better error handling** in `app.py`
2. **Created a simplified crew** (`crew_simple.py`) that doesn't require external API keys
3. **Added .env file support** for easier configuration
4. **Created a debug script** (`debug_website.py`) to identify issues
5. **Added health check endpoint** at `/health`

## 🚀 **Next Steps**

1. **Set your OpenAI API key** (see Step 2 above)
2. **Run the debug script** to verify everything works
3. **Start the website** and enjoy your Smart Car Buying Assistant!

## 💡 **Optional Enhancements**

If you want enhanced search capabilities, you can also get:
- **Serper API key** from [serper.dev](https://serper.dev)
- **Brave API key** from [brave.com](https://brave.com)

These are optional and the system will work without them.

---

**Need help?** Run `python debug_website.py` anytime to check your setup!
