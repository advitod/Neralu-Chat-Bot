# Neralu Farms Chatbot - Customization Guide

This guide will help you customize the chatbot to match your specific requirements and branding.

---

## 1. Updating Knowledge Base

### Add New Information
Edit the `NERALU_KNOWLEDGE` dictionary in `app.py`:

```python
NERALU_KNOWLEDGE = {
    "brand_info": {
        # Update brand information
        "name": "Your Brand Name",
        "tagline": "Your Tagline",
        "mission": "Your Mission Statement",
    },
    
    # Add new sections
    "new_section": {
        "key": "value",
        "description": "Information about new topic"
    }
}
```

### Example: Add New Project
```python
"projects": {
    "existing_project": {...},
    "new_project": {
        "name": "New Project Name",
        "location": "Location details",
        "features": ["Feature 1", "Feature 2"],
        "status": "Coming Soon / Available"
    }
}
```

---

## 2. Adding New Intents

### Step 1: Define Intent Patterns
Add keywords to `INTENT_PATTERNS` in `app.py`:

```python
INTENT_PATTERNS = {
    # ... existing intents
    "new_intent": ["keyword1", "keyword2", "phrase to match"],
}
```

### Step 2: Create Response
Add response in `generate_response()` function:

```python
responses = {
    # ... existing responses
    "new_intent": f"Your response here with {NERALU_KNOWLEDGE['section']['key']}",
}
```

### Example: Add "Testimonials" Intent
```python
# In INTENT_PATTERNS:
"testimonials": ["testimonial", "review", "customer feedback", "what others say"],

# In generate_response():
"testimonials": "Our customers love Neralu Farms! 🌟\n\n" + 
                "Here are some recent testimonials:\n" +
                "• 'Best investment decision!' - Rajesh K.\n" +
                "• 'Professional management team' - Priya S.\n\n" +
                "Would you like to become part of our community?",
```

---

## 3. Customizing UI Colors & Branding

### Change Color Scheme
Edit `templates/index.html`, look for these sections:

#### Header Colors
```css
.chat-header {
    background: linear-gradient(135deg, #2d5016 0%, #4a7c2c 100%);
    /* Change to your brand colors */
}
```

#### Message Bubble Colors
```css
.message.user .message-content {
    background: linear-gradient(135deg, #4a7c2c 0%, #5d9938 100%);
    /* User message color */
}

.message.bot .message-content {
    background: white;
    /* Bot message color */
}
```

#### Send Button Color
```css
.send-button {
    background: linear-gradient(135deg, #4a7c2c 0%, #5d9938 100%);
    /* Button color */
}
```

### Change Logo/Icon
Replace the emoji in multiple places:

```html
<!-- In header -->
<div class="logo">🌿</div>

<!-- In bot messages -->
avatar.textContent = sender === 'bot' ? '🌿' : '👤';
```

You can replace with:
- Another emoji
- Image: `<img src="logo.png" alt="Logo">`
- Text initials: `NF`

---

## 4. Modifying Quick Action Buttons

Edit the quick actions in `templates/index.html`:

```html
<div class="quick-actions" id="quickActions">
    <button class="quick-action-btn" onclick="sendQuickMessage('Your question')">
        Button Text
    </button>
    <!-- Add more buttons -->
</div>
```

### Example: Add Custom Buttons
```html
<button class="quick-action-btn" onclick="sendQuickMessage('Tell me about payment plans')">
    Payment Plans
</button>
<button class="quick-action-btn" onclick="sendQuickMessage('What are the tax benefits?')">
    Tax Benefits
</button>
```

---

## 5. Customizing Welcome Message

Edit the initial bot message in `templates/index.html`:

```html
<div class="message bot">
    <div class="avatar">🌿</div>
    <div class="message-content">
        Your custom welcome message here!<br><br>
        • Point 1<br>
        • Point 2<br>
    </div>
</div>
```

Or modify the greeting response in `app.py`:

```python
"greeting": "Your custom greeting message...",
```

---

## 6. Adding Multi-Language Support

### Step 1: Detect Language
Add language detection in `app.py`:

```python
def detect_language(message):
    # Simple detection based on script
    if any('\u0C80' <= c <= '\u0CFF' for c in message):  # Kannada
        return 'kn'
    return 'en'
```

### Step 2: Create Language-Specific Responses
```python
RESPONSES_KN = {
    "greeting": "ನಮಸ್ಕಾರ! ನೆರಳು ಫಾರ್ಮ್ಸ್‌ಗೆ ಸ್ವಾಗತ...",
    # ... more Kannada responses
}

RESPONSES_EN = {
    "greeting": "Hello! Welcome to Neralu Farms...",
    # ... English responses
}

def generate_response(intent, user_message, conversation_history):
    lang = detect_language(user_message)
    responses = RESPONSES_KN if lang == 'kn' else RESPONSES_EN
    return responses.get(intent, responses["general"])
```

---

## 7. Customizing Lead Capture

### Modify Lead Information Fields
Edit `extract_lead_info()` in `app.py`:

```python
def extract_lead_info(conversation_history):
    lead_info = {
        "name": None,
        "phone": None,
        "email": None,  # Add email
        "location": None,  # Add location
        "budget": None  # Add budget range
    }
    
    # Add extraction logic for new fields
    # Email regex
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        lead_info["email"] = email_match.group()
    
    return lead_info
```

### Customize Lead Capture Prompts
Modify responses to ask for specific information:

```python
"site_visit": "Wonderful! To book your site visit, I'll need:\n" +
              "• Your name\n" +
              "• Phone number\n" +
              "• Email (optional)\n" +
              "• Preferred location: Korlaparti or Sandal Valley\n\n" +
              "Please share these details.",
```

---

## 8. Integrating with CRM/Database

### PostgreSQL Integration Example

```python
import psycopg2

# Add connection function
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )

# Save lead to database
def save_lead(lead_info):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute(
        "INSERT INTO leads (name, phone, email, captured_at) VALUES (%s, %s, %s, %s)",
        (lead_info['name'], lead_info['phone'], lead_info['email'], datetime.now())
    )
    
    conn.commit()
    cur.close()
    conn.close()

# Update the /chat route to use this function
```

### Webhook Integration (Send to Zapier/Make)

```python
import requests

def send_to_webhook(lead_info):
    webhook_url = os.getenv('WEBHOOK_URL')
    
    requests.post(webhook_url, json={
        'name': lead_info['name'],
        'phone': lead_info['phone'],
        'source': 'Neralu Chatbot',
        'timestamp': datetime.now().isoformat()
    })

# Call in /chat route when lead is captured
```

---

## 9. Adding Email Notifications

```python
import smtplib
from email.mime.text import MIMEText

def send_lead_notification(lead_info):
    msg = MIMEText(f"""
    New lead captured from Neralu Chatbot!
    
    Name: {lead_info['name']}
    Phone: {lead_info['phone']}
    Session ID: {lead_info['session_id']}
    Time: {lead_info['captured_at']}
    """)
    
    msg['Subject'] = '🌿 New Lead - Neralu Farms Chatbot'
    msg['From'] = os.getenv('EMAIL_FROM')
    msg['To'] = os.getenv('EMAIL_TO')
    
    with smtplib.SMTP(os.getenv('SMTP_HOST'), os.getenv('SMTP_PORT')) as server:
        server.starttls()
        server.login(os.getenv('EMAIL_FROM'), os.getenv('EMAIL_PASSWORD'))
        server.send_message(msg)

# Call when lead is captured
```

---

## 10. Adding Analytics Events

### Google Analytics Events

Add to `templates/index.html`:

```javascript
function trackEvent(category, action, label) {
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label
        });
    }
}

// Track message sent
function sendMessage() {
    // ... existing code
    trackEvent('Chat', 'message_sent', intent);
}

// Track intent
function addMessage(text, sender) {
    // ... existing code
    if (sender === 'bot' && data.intent) {
        trackEvent('Intent', 'detected', data.intent);
    }
}

// Track lead capture
if (data.lead_captured) {
    trackEvent('Conversion', 'lead_captured', 'chatbot');
}
```

---

## 11. Customizing Response Tone

### Make Responses More Formal
```python
"greeting": "Good day. Welcome to Neralu Farms. I am here to assist you with information about our managed farmland services. How may I help you today?"
```

### Make Responses More Casual
```python
"greeting": "Hey there! 👋 So excited you're checking out Neralu Farms! We've got some amazing farmland opportunities. What brings you here today?"
```

### Remove Emojis
Search and replace all emojis in responses with empty string or appropriate text.

---

## 12. Adding File Upload Support

To allow users to upload documents:

```python
from werkzeug.utils import secure_filename

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file'}), 400
    
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join('uploads', filename))
    
    return jsonify({'success': True, 'filename': filename})
```

Add to frontend:
```html
<input type="file" id="fileUpload" accept=".pdf,.doc,.docx">
<button onclick="uploadFile()">Upload Document</button>

<script>
async function uploadFile() {
    const fileInput = document.getElementById('fileUpload');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });
    
    const data = await response.json();
    addMessage('Document uploaded successfully!', 'bot');
}
</script>
```

---

## 13. Adding Voice Input

```html
<!-- Add to HTML -->
<button id="voiceButton" onclick="startVoiceInput()">🎤</button>

<script>
function startVoiceInput() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-IN';
    
    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        document.getElementById('messageInput').value = transcript;
        sendMessage();
    };
    
    recognition.start();
}
</script>
```

---

## 14. Rate Limiting

Prevent spam by adding rate limiting:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/chat', methods=['POST'])
@limiter.limit("30 per minute")
def chat():
    # ... existing code
```

Install: `pip install Flask-Limiter`

---

## 15. Testing Your Customizations

### Test Locally
```bash
python app.py
# Open http://localhost:5000
```

### Test API Endpoints
```bash
# Test greeting
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "session_id": "test"}'

# Test intent
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about projects", "session_id": "test"}'
```

### Test Lead Capture
```bash
curl -X POST http://localhost:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "My name is John and my phone is 9876543210", "session_id": "test"}'

# Check if lead was captured
curl http://localhost:5000/leads
```

---

## Need Help?

If you need assistance with customization:
1. Check the code comments for guidance
2. Refer to Flask documentation for backend changes
3. Consult CSS/JavaScript references for UI changes
4. Contact the Neralu technical team for complex modifications

---

**Pro Tip**: Always test changes locally before deploying to production!
