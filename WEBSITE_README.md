# Smart Car Buying Assistant - Web Interface

A beautiful, modern web interface for the Smart Car Buying Assistant powered by CrewAI. This web application provides an intuitive user experience for interacting with the AI-powered car buying analysis system.

## 🌟 Features

- **Modern, Responsive Design**: Beautiful UI that works on desktop, tablet, and mobile devices
- **Real-time Progress Tracking**: See live updates as the AI crew analyzes your requirements
- **Comprehensive Form**: Collect all necessary information for car buying analysis
- **Detailed Results Display**: View organized, easy-to-read analysis results
- **Download Functionality**: Save your analysis as a text file
- **Error Handling**: Graceful error handling with user-friendly messages

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher (but less than 3.14)
- OpenAI API key configured in your environment

### Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your OpenAI API Key**:
   ```bash
   # On Windows
   set OPENAI_API_KEY=your_api_key_here
   
   # On macOS/Linux
   export OPENAI_API_KEY=your_api_key_here
   ```

3. **Run the Website**:
   ```bash
   python run_website.py
   ```

4. **Open your browser** and go to: `http://localhost:5000`

## 📱 How to Use

### 1. Fill Out the Form
- **Your Requirements**: Describe what you're looking for in a car
- **Car Type**: Select from sedan, SUV, truck, hybrid, electric, etc.
- **Budget Range**: Specify your budget (e.g., "$15,000 - $25,000")
- **Current State**: Select your state of residence

### 2. Submit and Wait
- Click "Get Smart Car Recommendations"
- Watch the real-time progress as our AI experts work
- The system will analyze your requirements through multiple specialized agents

### 3. Review Results
- View comprehensive analysis including:
  - Market research and vehicle recommendations
  - Legal requirements for out-of-state purchases
  - Vehicle valuations and pricing analysis
  - Negotiation strategies
  - Inspection checklists
- Download the full report as a text file

## 🏗️ Architecture

### Backend (Flask)
- **app.py**: Main Flask application with API endpoints
- **Background Processing**: CrewAI runs in background threads
- **Session Management**: Tracks user sessions and results
- **API Endpoints**:
  - `POST /submit_requirements`: Submit car buying requirements
  - `GET /status/<session_id>`: Get processing status
  - `GET /results/<session_id>`: Get analysis results
  - `GET /results/<session_id>/page`: Display results page

### Frontend (HTML/CSS/JavaScript)
- **templates/index.html**: Main form page with modern UI
- **templates/results.html**: Results display page
- **Responsive Design**: Works on all device sizes
- **Real-time Updates**: JavaScript polling for status updates
- **Modern Styling**: Gradient backgrounds, smooth animations

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `FLASK_ENV`: Set to 'development' for debug mode

### Customization
You can customize the website by modifying:
- **Styling**: Edit CSS in the HTML templates
- **Form Fields**: Add/remove fields in `templates/index.html`
- **Results Display**: Modify `templates/results.html` for different result formats
- **API Endpoints**: Extend `app.py` with additional functionality

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install -r requirements.txt
   ```

2. **OpenAI API Key Not Set**:
   ```bash
   export OPENAI_API_KEY=your_key_here
   ```

3. **Port Already in Use**:
   - Change the port in `app.py` or `run_website.py`
   - Kill the process using the port

4. **CrewAI Errors**:
   - Check your internet connection
   - Verify your OpenAI API key is valid
   - Check the CrewAI documentation for troubleshooting

### Debug Mode
Run with debug mode for detailed error messages:
```bash
export FLASK_ENV=development
python run_website.py
```

## 📁 Project Structure

```
smart_car_buying_assistant_v1_crewai-project/
├── app.py                          # Main Flask application
├── run_website.py                  # Startup script
├── requirements.txt                # Python dependencies
├── templates/                      # HTML templates
│   ├── index.html                 # Main form page
│   └── results.html               # Results display page
├── src/                           # Original CrewAI project
│   └── smart_car_buying_assistant/
├── WEBSITE_README.md              # This file
└── README.md                      # Original project README
```

## 🎨 Design Features

- **Gradient Backgrounds**: Modern purple-blue gradients
- **Card-based Layout**: Clean, organized information display
- **Smooth Animations**: Hover effects and transitions
- **Icon Integration**: Font Awesome icons throughout
- **Mobile Responsive**: Optimized for all screen sizes
- **Progress Indicators**: Real-time progress bars and status updates

## 🔒 Security Notes

- Change the Flask secret key in production
- Use HTTPS in production environments
- Implement proper session management for production
- Add rate limiting for API endpoints
- Validate and sanitize all user inputs

## 🚀 Deployment

### Local Development
```bash
python run_website.py
```

### Production Deployment
For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a reverse proxy (Nginx)
- Using environment variables for configuration
- Implementing proper logging
- Setting up monitoring and health checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Smart Car Buying Assistant CrewAI project.

## 🆘 Support

For issues related to:
- **Website/UI**: Check this README and the code comments
- **CrewAI Integration**: Refer to the original project README
- **General Issues**: Check the CrewAI documentation

---

**Happy Car Shopping! 🚗✨**
