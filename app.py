from flask import Flask, render_template, request, jsonify, session
import os
import sys
import json
from datetime import datetime
import threading
import time

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Loaded environment variables from .env file")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables")
except Exception as e:
    print(f"⚠️  Could not load .env file: {e}")

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Global variable to store crew results
crew_results = {}
crew_status = {}

def make_json_serializable(obj):
    """Convert an object to JSON serializable format"""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, (list, tuple)):
        return [make_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: make_json_serializable(value) for key, value in obj.items()}
    else:
        return str(obj)

def check_environment():
    """Check if required environment variables are set"""
    missing_vars = []
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        missing_vars.append('OPENAI_API_KEY')
    
    # Check for optional API keys (these are optional but recommended)
    optional_vars = ['SERPER_API_KEY', 'BRAVE_API_KEY']
    for var in optional_vars:
        if not os.getenv(var):
            print(f"⚠️  Warning: {var} not set. Some features may be limited.")
    
    if missing_vars:
        error_msg = f"Missing required environment variables: {', '.join(missing_vars)}"
        print(f"❌ {error_msg}")
        return False, error_msg
    
    return True, "Environment check passed"

@app.route('/')
def index():
    """Main page with the car buying assistant form"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint"""
    env_ok, env_msg = check_environment()
    
    return jsonify({
        'status': 'healthy' if env_ok else 'unhealthy',
        'environment': env_msg,
        'crew_available': env_ok
    })

@app.route('/submit_requirements', methods=['POST'])
def submit_requirements():
    """Handle form submission and start the crew process"""
    try:
        # Check environment first
        env_ok, env_msg = check_environment()
        if not env_ok:
            return jsonify({'error': env_msg}), 400
        
        data = request.get_json()
        
        # Extract form data
        user_requirements = data.get('user_requirements', '')
        car_type = data.get('car_type', '')
        budget_range = data.get('budget_range', '')
        current_state = data.get('current_state', '')
        
        # Validate required fields
        if not all([user_requirements, car_type, budget_range, current_state]):
            return jsonify({'error': 'All fields are required'}), 400
        
        # Create a unique session ID
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Initialize crew status
        crew_status[session_id] = {
            'status': 'starting',
            'progress': 0,
            'current_task': 'Initializing...',
            'results': None,
            'error': None
        }
        
        # Start the crew process in a background thread
        thread = threading.Thread(
            target=run_crew_background,
            args=(session_id, user_requirements, car_type, budget_range, current_state)
        )
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'session_id': session_id,
            'message': 'Crew process started successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def run_crew_background(session_id, user_requirements, car_type, budget_range, current_state):
    """Run the crew process in the background"""
    try:
        # Update status
        crew_status[session_id]['status'] = 'running'
        crew_status[session_id]['progress'] = 10
        crew_status[session_id]['current_task'] = 'Analyzing requirements...'
        
        # Import the crew here to avoid import errors at startup
        # Try to use the robust crew first (handles missing API keys gracefully)
        try:
            from smart_car_buying_assistant.crew_robust import SmartCarBuyingAssistantCrewRobust
            crew_class = SmartCarBuyingAssistantCrewRobust
            print("✅ Using robust crew (handles missing API keys gracefully)")
        except ImportError as e:
            print(f"⚠️  Could not import robust crew: {e}")
            
            # Check if optional API keys are available
            serper_key = os.getenv('SERPER_API_KEY')
            brave_key = os.getenv('BRAVE_API_KEY')
            
            # Use simplified crew if search API keys are missing
            if not serper_key or not brave_key:
                print("⚠️  Search API keys not available, using simplified crew")
                try:
                    from smart_car_buying_assistant.crew_simple import SmartCarBuyingAssistantCrewSimple
                    crew_class = SmartCarBuyingAssistantCrewSimple
                    print("✅ Using simplified crew (no external API dependencies)")
                except ImportError as e2:
                    print(f"⚠️  Could not import simplified crew: {e2}")
                    # Fallback to main crew
                    try:
                        from smart_car_buying_assistant.crew import SmartCarBuyingAssistantCrew
                        crew_class = SmartCarBuyingAssistantCrew
                        print("⚠️  Using main crew (some features may fail)")
                    except ImportError as e3:
                        raise Exception(f"Failed to import any CrewAI module: {e3}")
            else:
                # Use main crew if all API keys are available
                try:
                    from smart_car_buying_assistant.crew import SmartCarBuyingAssistantCrew
                    crew_class = SmartCarBuyingAssistantCrew
                    print("✅ Using main crew with full search capabilities")
                except ImportError as e2:
                    print(f"⚠️  Could not import main crew: {e2}")
                    # Fallback to simplified crew
                    try:
                        from smart_car_buying_assistant.crew_simple import SmartCarBuyingAssistantCrewSimple
                        crew_class = SmartCarBuyingAssistantCrewSimple
                        print("✅ Using simplified crew as fallback")
                    except ImportError as e3:
                        raise Exception(f"Failed to import any CrewAI module: {e3}")
        
        # Prepare inputs for the crew
        inputs = {
            'user_requirements': user_requirements,
            'car_type': car_type,
            'budget_range': budget_range,
            'current_state': current_state
        }
        
        # Update progress
        crew_status[session_id]['progress'] = 20
        crew_status[session_id]['current_task'] = 'Creating AI crew...'
        
        # Create the crew
        try:
            crew = crew_class().crew()
        except Exception as e:
            raise Exception(f"Failed to create crew: {e}")
        
        # Update progress
        crew_status[session_id]['progress'] = 30
        crew_status[session_id]['current_task'] = 'Researching vehicle market...'
        
        # Run the crew
        try:
            result = crew.kickoff(inputs=inputs)
            print(f"✅ Crew execution completed successfully")
        except Exception as e:
            print(f"❌ Crew execution failed: {e}")
            raise Exception(f"Crew execution failed: {e}")
        
        # Format the results according to the specified output format
        try:
            formatted_result = format_crew_results(result, user_requirements, car_type, budget_range, current_state)
            crew_results[session_id] = formatted_result
            crew_status[session_id]['status'] = 'completed'
            crew_status[session_id]['progress'] = 100
            crew_status[session_id]['current_task'] = 'Analysis complete!'
            crew_status[session_id]['results'] = formatted_result
            print(f"✅ Results formatted and stored successfully for session {session_id}")
        except Exception as e:
            print(f"❌ Error formatting results: {e}")
            # Fallback to raw results if formatting fails
            result_str = str(result) if result else "No results generated"
            crew_results[session_id] = result_str
            crew_status[session_id]['status'] = 'completed'
            crew_status[session_id]['progress'] = 100
            crew_status[session_id]['current_task'] = 'Analysis complete!'
            crew_status[session_id]['results'] = result_str
        
    except Exception as e:
        crew_status[session_id]['status'] = 'error'
        crew_status[session_id]['error'] = str(e)
        crew_status[session_id]['current_task'] = f'Error: {str(e)}'
        print(f"❌ Error in crew execution: {e}")

def format_crew_results(result, user_requirements, car_type, budget_range, current_state):
    """Format the crew results according to the specified output format"""
    try:
        # Get current date
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Extract additional details from user requirements
        # This is a simplified extraction - you may need to enhance this based on your actual input format
        requirements_parts = user_requirements.split(',') if user_requirements else []
        
        # Default values
        color = "Not specified"
        mileage = "Not specified"
        must_have_features = "Not specified"
        nice_to_have_features = "Not specified"
        payment_method = "Not specified"
        intended_use = "Not specified"
        purchase_date = "Not specified"
        special_considerations = "Not specified"
        
        # Try to extract information from requirements
        for part in requirements_parts:
            part = part.strip().lower()
            if 'color' in part or 'black' in part or 'white' in part or 'red' in part or 'blue' in part:
                color = part.split(':')[-1].strip() if ':' in part else part
            elif 'mileage' in part or 'miles' in part:
                mileage = part.split(':')[-1].strip() if ':' in part else part
            elif 'sunroof' in part or 'camera' in part or 'bluetooth' in part:
                if 'must' in part or 'required' in part:
                    must_have_features = part
                else:
                    nice_to_have_features = part
            elif 'cash' in part or 'loan' in part or 'finance' in part:
                payment_method = part
            elif 'commute' in part or 'work' in part or 'family' in part:
                intended_use = part
            elif 'week' in part or 'month' in part or 'day' in part:
                purchase_date = part
            elif 'title' in part or 'clean' in part:
                special_considerations = part
        
        # Start building the formatted output
        formatted_output = f"""Comprehensive Car Buying Report
Current Date: {current_date}

Customer Profile
State: {current_state}
Vehicle Type: {car_type}
Color: {color}
Mileage: {mileage}
Budget: {budget_range}
Must-Have Features: {must_have_features}
Nice-to-Have Features: {nice_to_have_features}
Method of Payment: {payment_method}
Intended Use: {intended_use}
Desired Purchase Date: {purchase_date}
Special Consideration: {special_considerations}

"""
        
        # Add the crew results
        if result:
            result_str = str(result)
            
            # Try to extract and format specific sections
            if "Top" in result_str and "Recommended" in result_str:
                # Extract the top recommendations section
                formatted_output += "Top 10 Recommended Vehicles\n"
                # Add the table format
                formatted_output += "| Rank | Vehicle Model | Price | Mileage | Location | Seller Type | Link |\n"
                formatted_output += "|------|-----------------------------|--------|---------|------------------|------------------|------------------------------------------------|\n"
                
                # Try to extract vehicle information from the result
                # This is a simplified approach - you may need to enhance this
                lines = result_str.split('\n')
                rank = 1
                for line in lines:
                    if any(keyword in line.lower() for keyword in ['nissan', 'toyota', 'honda', 'hyundai', 'mazda', 'subaru', 'ford', 'chevrolet', 'volkswagen', 'kia']):
                        # Extract vehicle info (simplified)
                        parts = line.split('|')
                        if len(parts) >= 6:
                            formatted_output += f"| {rank} | {parts[0].strip()} | {parts[1].strip()} | {parts[2].strip()} | {parts[3].strip()} | {parts[4].strip()} | {parts[5].strip()} |\n"
                        else:
                            formatted_output += f"| {rank} | {line.strip()} | $TBD | TBD | TBD | TBD | TBD |\n"
                        rank += 1
                        if rank > 10:
                            break
                
                formatted_output += "\n"
            
            # Add the rest of the result content
            formatted_output += result_str
            
            # Add standard sections if not present
            if "Detailed Reasons" not in result_str:
                formatted_output += "\n\nDetailed Reasons to Buy Each Vehicle\n"
                formatted_output += "Detailed analysis of each recommended vehicle will be provided based on the research.\n"
            
            if "Out-of-State Registration" not in result_str:
                formatted_output += "\n\nOut-of-State Registration Requirements\n"
                formatted_output += "For vehicles purchased outside " + current_state + ", the following requirements must be met:\n"
                formatted_output += "Documentation: Bill of sale, title transfer documentation, and any loan agreements if applicable.\n"
                formatted_output += "Fees: Expect to pay registration fees and sales tax based on the purchase price.\n"
                formatted_output += "Inspection: Some vehicles may require a smog check before registration.\n"
                formatted_output += "Timeline: Registration should occur within 10 days of purchase to avoid penalties.\n"
                formatted_output += "Process: Visit the " + current_state + " DMV website for step-by-step instructions.\n"
            
            if "Negotiation Strategies" not in result_str:
                formatted_output += "\n\nNegotiation Strategies\n"
                formatted_output += "| Vehicle Model | Negotiation Range | Suggested Offer Price |\n"
                formatted_output += "|---------------------------|---------------------|-----------------------|\n"
                formatted_output += "| [Vehicle] | [Range] | [Suggested Price] |\n"
                formatted_output += "\nTips for Negotiation:\n"
                formatted_output += "Research market values and be prepared to justify your offer.\n"
                formatted_output += "Highlight any issues found during inspections as leverage.\n"
                formatted_output += "Be ready to walk away if the deal doesn't meet your budget.\n"
            
            if "Inspection Checklists" not in result_str:
                formatted_output += "\n\nInspection Checklists\n"
                formatted_output += "Exterior Inspection\n"
                formatted_output += "Body condition (dents, scratches)\n"
                formatted_output += "Paint consistency\n"
                formatted_output += "Tire tread and wear\n"
                formatted_output += "Functional lights and signals\n"
                formatted_output += "\nInterior Inspection\n"
                formatted_output += "Seat condition\n"
                formatted_output += "Dashboard functionality\n"
                formatted_output += "Air conditioning and heating\n"
                formatted_output += "Infotainment system operation\n"
                formatted_output += "\nEngine and Mechanical Components\n"
                formatted_output += "Fluid levels\n"
                formatted_output += "Signs of leaks\n"
                formatted_output += "Battery condition\n"
                formatted_output += "Brake responsiveness\n"
            
            if "Final Recommendations" not in result_str:
                formatted_output += "\n\nFinal Recommendations\n"
                formatted_output += "Next Steps:\n"
                formatted_output += "Research and contact sellers for preferred vehicles.\n"
                formatted_output += "Schedule inspections and test drives.\n"
                formatted_output += "Prepare negotiation strategies based on research.\n"
                formatted_output += "Complete necessary paperwork for out-of-state registration if applicable.\n"
                formatted_output += "Finalize purchase before the desired purchase date.\n"
                formatted_output += "\nBy following this structured approach, you can confidently navigate the car buying process and select a vehicle that meets your needs and budget.\n"
        else:
            formatted_output += "No results generated from the crew analysis.\n"
        
        return formatted_output
        
    except Exception as e:
        print(f"❌ Error formatting results: {e}")
        # Return the raw result if formatting fails
        return str(result) if result else "No results generated"

@app.route('/status/<session_id>')
def get_status(session_id):
    """Get the current status of a crew process"""
    if session_id not in crew_status:
        return jsonify({'error': 'Session not found'}), 404
    
    try:
        # Ensure all values are JSON serializable
        status_data = make_json_serializable(crew_status[session_id])
        return jsonify(status_data)
    except Exception as e:
        print(f"❌ Error serializing status for session {session_id}: {e}")
        return jsonify({
            'error': 'Error retrieving status',
            'session_id': session_id,
            'status': 'error'
        }), 500

@app.route('/results/<session_id>')
def get_results(session_id):
    """Get the results of a completed crew process"""
    if session_id not in crew_results:
        return jsonify({'error': 'Results not found'}), 404
    
    try:
        # Ensure all values are JSON serializable
        status_data = make_json_serializable(crew_status.get(session_id, {}))
        
        return jsonify({
            'results': crew_results[session_id],
            'status': status_data
        })
    except Exception as e:
        print(f"❌ Error serializing results for session {session_id}: {e}")
        return jsonify({
            'error': 'Error retrieving results',
            'session_id': session_id,
            'results': str(crew_results.get(session_id, "Error retrieving results"))
        }), 500

@app.route('/results/<session_id>/page')
def results_page(session_id):
    """Display results page"""
    if session_id not in crew_results:
        return "Results not found", 404
    
    return render_template('results.html', session_id=session_id)

if __name__ == '__main__':
    # Check environment on startup
    env_ok, env_msg = check_environment()
    if not env_ok:
        print(f"❌ {env_msg}")
        print("💡 Please set the required environment variables before starting the server.")
        print("   Example: set OPENAI_API_KEY=your_api_key_here")
        sys.exit(1)
    
    print("✅ Environment check passed!")
    print("🚀 Starting Smart Car Buying Assistant Web Application...")
    print("📱 The website will be available at: http://localhost:5000")
    print("🔄 Press Ctrl+C to stop the server")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
