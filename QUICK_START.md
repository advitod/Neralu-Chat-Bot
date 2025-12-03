# Neralu Farms Chatbot - Quick Start Guide

Get your chatbot up and running in 5 minutes!

---

## ⚡ Quick Start (Local Testing)

### 1. Install Python Dependencies
```bash
cd neralu_chatbot
pip install flask flask-cors
```

### 2. Run the Chatbot
```bash
python app.py
```

### 3. Open in Browser
Navigate to: **http://localhost:5000**

That's it! Your chatbot is now running locally. 🎉

---

## 📁 What's Included

```
neralu_chatbot/
├── app.py                      # Main chatbot backend (rule-based)
├── advanced_chatbot.py         # AI-powered version (requires OpenAI)
├── requirements.txt            # Python dependencies
├── templates/
│   └── index.html             # Chatbot UI
├── README.md                   # Complete documentation
├── DEPLOYMENT_GUIDE.md        # Deployment instructions
├── CUSTOMIZATION_GUIDE.md     # How to customize
└── .env.example               # Environment variables template
```

---

## 🚀 Deploy in 5 Minutes

### Option 1: Heroku (Easiest - Free Tier Available)
```bash
# Install Heroku CLI, then:
git init
git add .
git commit -m "Initial commit"
heroku create neralu-chatbot
git push heroku master
heroku open
```

### Option 2: Railway.app (Modern & Easy)
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub"
4. Select this repository
5. Railway auto-deploys! Get your URL

### Option 3: Your Website (Iframe Embed)
Add this to your website:
```html
<iframe 
    src="http://your-chatbot-url.com" 
    width="400" 
    height="600" 
    frameborder="0">
</iframe>
```

---

## 🎨 Quick Customization

### Change Brand Colors
Edit `templates/index.html` - Search for these colors:
- `#2d5016` - Dark green (header)
- `#4a7c2c` - Medium green (buttons)
- `#5d9938` - Light green (accents)

Replace with your brand colors!

### Update Welcome Message
Edit `app.py` line ~128:
```python
"greeting": "Your custom welcome message here!"
```

### Add New Quick Action Buttons
Edit `templates/index.html` around line 211:
```html
<button class="quick-action-btn" onclick="sendQuickMessage('Your Question')">
    Button Text
</button>
```

### Update Knowledge Base
Edit `app.py` starting at line 24 - the `NERALU_KNOWLEDGE` dictionary contains all information.

---

## 🧪 Test Your Chatbot

### Test in Browser
1. Go to http://localhost:5000
2. Try these queries:
   - "Hello"
   - "Tell me about Neralu Farms"
   - "What plantations do you offer?"
   - "I want to book a site visit"

### Test API Directly
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test123"}'
```

### Check Captured Leads
```bash
curl http://localhost:5000/leads
```

---

## 💡 What The Chatbot Can Do

### Current Features (app.py - Rule-Based)
✅ Answer questions about Neralu Farms  
✅ Explain managed farmland concept  
✅ Provide project information  
✅ Discuss plantations (Mango, Coconut, Timber, Sandalwood)  
✅ Share investment benefits  
✅ Guide through site visit booking  
✅ Capture leads (name + phone)  
✅ Beautiful responsive UI  
✅ Works on mobile and desktop  

### Advanced Features (advanced_chatbot.py - AI-Powered)
🤖 Natural conversation with OpenAI GPT  
🤖 Context-aware responses  
🤖 Handles unexpected questions  
🤖 More human-like interactions  

*Note: Advanced version requires OpenAI API key and setup*

---

## 🔧 Common Issues & Solutions

### Issue: "Module not found"
```bash
Solution: pip install flask flask-cors
```

### Issue: "Port 5000 already in use"
```bash
Solution: 
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change port in app.py
app.run(port=5001)
```

### Issue: Chatbot not responding
- Check console for errors
- Ensure Flask server is running
- Check network tab in browser DevTools
- Try restarting the server

---

## 📊 View Captured Leads

### In Browser
Navigate to: **http://localhost:5000/leads**

### In Code
Leads are stored in the `leads` list in `app.py`. To export:

```python
import json

# Add this route to app.py
@app.route('/export-leads', methods=['GET'])
def export_leads():
    return json.dumps(leads, indent=2)
```

Then visit: http://localhost:5000/export-leads

---

## 🌐 Integration Options

### 1. Full Page
Simply link to your chatbot:
```html
<a href="https://your-chatbot-url.com">Chat with us</a>
```

### 2. Iframe Embed
Embed in existing website:
```html
<iframe src="https://your-chatbot-url.com" 
        width="100%" height="600px" 
        frameborder="0">
</iframe>
```

### 3. Floating Widget
See `DEPLOYMENT_GUIDE.md` for widget code

### 4. API Integration
Use the `/chat` endpoint in your own app:
```javascript
fetch('https://your-chatbot-url.com/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        message: 'User message',
        session_id: 'unique-id'
    })
});
```

---

## 🚀 Next Steps

### For Production Use:
1. ✅ Deploy to hosting platform (see DEPLOYMENT_GUIDE.md)
2. ✅ Enable HTTPS (use Let's Encrypt)
3. ✅ Add database for lead storage (PostgreSQL recommended)
4. ✅ Set up email notifications for new leads
5. ✅ Add Google Analytics tracking
6. ✅ Connect to your CRM (Salesforce, HubSpot, etc.)

### For Better AI:
1. Get OpenAI API key from [platform.openai.com](https://platform.openai.com)
2. Install: `pip install openai`
3. Set environment variable: `export OPENAI_API_KEY='your-key'`
4. Use `advanced_chatbot.py` instead of `app.py`
5. Uncomment OpenAI code in `advanced_chatbot.py`

### For More Features:
- Add WhatsApp integration
- Enable voice input/output
- Add multi-language support (Kannada)
- Create admin dashboard
- Add conversation analytics

---

## 📚 Documentation

- **README.md** - Complete overview and features
- **DEPLOYMENT_GUIDE.md** - Detailed deployment instructions
- **CUSTOMIZATION_GUIDE.md** - How to customize everything
- **This file** - Quick start guide

---

## 🆘 Need Help?

### Stuck? Try These:
1. Read the error message carefully
2. Check the relevant documentation file
3. Google the specific error
4. Check Flask documentation: [flask.palletsprojects.com](https://flask.palletsprojects.com)

### Still Stuck?
Contact the Neralu technical team with:
- Error message
- What you were trying to do
- Screenshots if possible

---

## 🎯 Success Checklist

Before considering your chatbot "complete":

- [ ] Tested all intents (greeting, projects, plantations, etc.)
- [ ] Lead capture working (test with name + phone)
- [ ] UI looks good on mobile and desktop
- [ ] Brand colors match your website
- [ ] Welcome message is customized
- [ ] Quick action buttons are relevant
- [ ] Tested in different browsers (Chrome, Firefox, Safari)
- [ ] Deployed to production hosting
- [ ] HTTPS enabled
- [ ] Lead notification set up (email/webhook)
- [ ] Analytics tracking added
- [ ] Team trained on accessing leads

---

## 🎉 Congratulations!

You now have a fully functional AI chatbot for Neralu Farms!

### What Your Chatbot Does:
✨ Educates visitors about managed farmland  
✨ Answers questions 24/7  
✨ Captures qualified leads  
✨ Books site visits  
✨ Provides consistent information  
✨ Improves customer experience  

### Your chatbot will help:
📈 Increase lead generation  
📈 Reduce support workload  
📈 Provide instant responses  
📈 Qualify prospects automatically  
📈 Improve conversion rates  

---

**Ready to go live? Follow the DEPLOYMENT_GUIDE.md to publish your chatbot!**

---

*Built for Neralu Farms with ❤️ and 🌿*
