# AI Research Paper Generator

A beautiful, modern web application that generates comprehensive research papers using Google's Gemini AI. Features an advanced interface with HTML, CSS, JavaScript, and PDF generation capabilities.

## Features

- 🤖 **AI-Powered Research Generation**: Uses Google Gemini AI to create comprehensive research papers
- 🎨 **Modern Web Interface**: Beautiful, responsive design with animations and smooth interactions
- 📄 **PDF Export**: Download generated research papers as professionally formatted PDFs
- 🌍 **Multi-Language Support**: Generate papers in multiple languages
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- ⚡ **Real-time Generation**: Fast and efficient AI-powered content generation
- 💾 **Copy to Clipboard**: Easy text copying functionality
- 🎯 **Customizable Length**: Choose from 2 to 10 pages

## Installation

1. **Clone or download the project files**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your Google API key**:
   - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Create a `.env` file in the project root:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to `http://localhost:5000`

## Usage

1. **Enter Research Details**:
   - Research Topic: Describe what you want to research
   - Language: Choose from English, Arabic, Spanish, French, German, Chinese, or Japanese
   - Number of Pages: Select from 2 to 10 pages

2. **Generate Research Paper**:
   - Click "Generate Research Paper" button
   - Wait for the AI to create your comprehensive research paper

3. **Download or Copy**:
   - Download as PDF for professional formatting
   - Copy text to clipboard for easy sharing

## Project Structure

```
AI Research/
├── app.py                 # Flask backend application
├── templates/
│   └── index.html        # Main HTML template
├── static/
│   ├── css/
│   │   └── style.css     # Beautiful CSS styling
│   └── js/
│       └── script.js     # Interactive JavaScript
├── requirements.txt      # Python dependencies
├── .env                 # Environment variables (create this)
└── README.md           # This file
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **AI**: Google Gemini AI via LangChain
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **PDF Generation**: ReportLab
- **Styling**: Custom CSS with animations and responsive design
- **Icons**: Font Awesome
- **Fonts**: Google Fonts (Inter)

## Features Breakdown

### 🎨 **Modern Interface**
- Gradient backgrounds and glass-morphism effects
- Smooth animations and transitions
- Interactive hover effects
- Responsive grid layouts

### 🤖 **AI Integration**
- Multiple model fallback system
- Error handling and retry logic
- Real-time generation status
- Comprehensive prompt engineering

### 📄 **PDF Generation**
- Professional formatting
- Custom styling and typography
- Automatic page breaks
- Structured sections (Abstract, Introduction, etc.)

### ⚡ **User Experience**
- Toast notifications for feedback
- Loading states and progress indicators
- Keyboard shortcuts (Ctrl+Enter to submit)
- Form validation with visual feedback

## API Endpoints

- `GET /` - Main application page
- `POST /generate` - Generate research paper
- `POST /download_pdf` - Download PDF version

## Customization

### Adding New Languages
Edit the language options in `templates/index.html`:
```html
<option value="YourLanguage">Your Language</option>
```

### Modifying AI Prompts
Edit the prompt template in `app.py`:
```python
prompt = ChatPromptTemplate.from_template(
    "Your custom prompt here: {topic}..."
)
```

### Styling Changes
Modify `static/css/style.css` to customize colors, fonts, and layouts.

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your Google API key is valid and has Gemini API access
2. **Model Not Found**: The app will try multiple model names automatically
3. **PDF Generation Error**: Ensure ReportLab is properly installed
4. **Port Already in Use**: Change the port in `app.py` if needed

### Getting Help

- Check the browser console for JavaScript errors
- Check the Flask console for Python errors
- Verify your `.env` file has the correct API key
- Ensure all dependencies are installed

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this application.

---

**Enjoy generating amazing research papers with AI! 🚀**
