# 🤖 PbjAI - Personal AI Assistant

An AI-powered chatbot that acts as a personal assistant for Prabanjan R. Built with Gradio and Google's Gemini API, this AI assistant can answer questions about projects, skills, and experience based on LinkedIn profile data and personal summary.

## ✨ Features

- **Personal AI Chatbot**: Acts as Prabanjan R with personality and knowledge from real data
- **Web Interface**: Clean, modern chat interface powered by Gradio
- **Smart Responses**: Uses Google Gemini 2.5 Flash Lite for intelligent conversations
- **Lead Capture**: Records user interest and contact information for follow-up
- **Question Tracking**: Logs unanswered questions for improvement
- **Push Notifications**: Real-time notifications via Pushover when users show interest

## 🛠️ Tech Stack

- **Backend**: Python
- **AI Model**: Google Gemini 2.5 Flash Lite
- **Web Interface**: Gradio
- **API Client**: OpenAI Python SDK (for Gemini compatibility)
- **PDF Processing**: pypdf
- **Notifications**: Pushover API
- **Environment**: python-dotenv

## 📋 Prerequisites

- Python 3.8+
- Google Gemini API key
- Pushover account (for notifications)

## 🚀 Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd PbjAI
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   PUSHOVER_USER=your_pushover_user_key
   PUSHOVER_TOKEN=your_pushover_api_token
   ```

5. **Prepare personal data**
   - Place your LinkedIn profile PDF as `me/linkedin.pdf`
   - Create a personal summary in `me/summary.txt`

## 🏃‍♂️ Running the Application

Start the web interface:
```bash
python app.py
```

The application will launch on `http://localhost:7860` by default.

## 📁 Project Structure

```
PbjAI/
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not tracked)
├── .gitignore         # Git ignore rules
└── me/                # Personal data directory
    ├── linkedin.pdf   # LinkedIn profile data
    └── summary.txt    # Personal summary
```

## 🔧 Configuration

### AI Behavior
The AI assistant follows strict rules:
- Only uses provided data from LinkedIn profile and summary
- Does not hallucinate information
- Records unknown questions for improvement
- Captures user interest when appropriate

### Tools Integration
- **record_user_details**: Captures email and contact information
- **record_unknown_question**: Logs unanswered questions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔒 Privacy & Security

- Environment variables are not tracked in version control
- Personal data is stored locally in the `me/` directory
- User interactions are processed through secure APIs
- No personal data is stored permanently unless explicitly captured

## 🆘 Troubleshooting

### Common Issues

1. **Gemini API Error**: Ensure your API key is valid and has sufficient quota
2. **Pushover Notifications**: Verify your Pushover user key and token are correct
3. **PDF Reading**: Ensure the LinkedIn PDF is accessible and readable
4. **Port Conflict**: Gradio will automatically find an available port if 7860 is occupied

### Debug Mode
For debugging, the application prints push notifications and errors to the console.

## 📞 Support

For questions or support, please reach out through the AI assistant or create an issue in the repository.
