# Railway Deployment Guide

## 🚀 Deploy AI Research Paper Generator to Railway

### Prerequisites
1. GitHub account
2. Railway account (free at railway.app)
3. Google API key for Gemini

### Step 1: Prepare Your Code
1. Upload all files to a GitHub repository
2. Make sure all files are in the root directory:
   - `flask_app.py` (main Flask application)
   - `AImodel.py` (AI model)
   - `requirements.txt` (dependencies)
   - `Procfile` (startup command)
   - `railway.json` (Railway configuration)
   - `templates/` folder with `index.html`
   - `static/` folder with CSS and JS files

### Step 2: Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will automatically detect it's a Python project

### Step 3: Configure Environment Variables
1. In Railway dashboard, go to your project
2. Click on "Variables" tab
3. Add the following environment variable:
   ```
   GOOGLE_API_KEY=your_actual_google_api_key_here
   ```
4. Get your API key from: https://aistudio.google.com/app/apikey

### Step 4: Deploy
1. Railway will automatically build and deploy your app
2. Wait for deployment to complete
3. Your app will be available at the provided Railway URL

### Step 5: Test Your Deployment
1. Open the Railway URL in your browser
2. Test generating a research paper
3. Test downloading PDF in Arabic and English

## 📁 Required Files for Railway

```
your-repo/
├── flask_app.py          # Main Flask application
├── AImodel.py            # AI model class
├── requirements.txt      # Python dependencies
├── Procfile             # Railway startup command
├── railway.json         # Railway configuration
├── templates/
│   └── index.html       # HTML template
├── static/
│   ├── css/
│   │   └── style.css    # CSS styling
│   └── js/
│       └── script.js    # JavaScript functionality
└── README.md            # Documentation
```

## 🔧 Environment Variables

Add these in Railway dashboard:

| Variable | Value | Description |
|----------|-------|-------------|
| `GOOGLE_API_KEY` | `your_api_key` | Google Gemini API key |
| `FLASK_ENV` | `production` | Flask environment |
| `PORT` | `auto` | Railway sets this automatically |

## 🎯 Features After Deployment

- ✅ Professional web interface
- ✅ AI-powered research paper generation
- ✅ Arabic language support
- ✅ Professional PDF generation with cover page
- ✅ Table of contents and appendix
- ✅ Multi-language support
- ✅ Responsive design

## 🚨 Troubleshooting

### Common Issues:

1. **API Key Error**: Make sure `GOOGLE_API_KEY` is set correctly
2. **Build Fails**: Check `requirements.txt` has all dependencies
3. **App Won't Start**: Verify `Procfile` is correct
4. **PDF Generation Fails**: Ensure all ReportLab dependencies are installed

### Logs:
- Check Railway logs in the dashboard
- Look for error messages during deployment
- Verify all environment variables are set

## 📞 Support

If you encounter issues:
1. Check Railway logs
2. Verify all files are uploaded correctly
3. Ensure environment variables are set
4. Test locally first with `python3 flask_app.py`

---

**Your AI Research Paper Generator is now live on Railway! 🎉**
