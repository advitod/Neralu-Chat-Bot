# Neralu Farms AI Chatbot

An intelligent chatbot designed to assist visitors, prospects, and customers of Neralu Farms with information about managed farmland ownership, projects, plantations, and investment opportunities.

## Features

### Core Capabilities
- **Natural Language Understanding**: Detects user intent and provides contextual responses
- **Brand-Focused Conversations**: Exclusively discusses Neralu Farms and its offerings
- **Intent Detection**: Recognizes various user intents including:
  - Greeting and general inquiries
  - Managed farmland concept questions
  - Project information (Korlaparti & Sandal Valley)
  - Plantation options (Mango, Coconut, Timber, Sandalwood)
  - Investment benefits and returns
  - Amenities and infrastructure
  - Legal and documentation queries
  - Site visit booking
  - Pricing information

### Lead Management
- **Automatic Lead Capture**: Extracts name and phone number from conversations
- **Lead Storage**: Saves captured leads with conversation history
- **Lead Retrieval**: Admin endpoint to view all captured leads

### User Experience
- **Quick Action Buttons**: One-click access to common queries
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Beautiful UI**: Nature-inspired color scheme matching Neralu's brand
- **Typing Indicators**: Shows when the bot is processing
- **Smooth Animations**: Professional fade-in effects for messages

## Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **API**: RESTful endpoints
- **Deployment Ready**: Gunicorn WSGI server included

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
cd neralu_chatbot
pip install -r requirements.txt
```

### Step 2: Run the Application

**For Development:**
```bash
python app.py
```

**For Production:**
```bash
gunicorn --bind 0.0.0.0:5000 app:app
```

### Step 3: Access the Chatbot
Open your browser and navigate to:
```
http://localhost:5000
```

## API Endpoints

### Chat Endpoint
**POST** `/chat`

Request body:
```json
{
  "message": "Tell me about Neralu Farms",
  "session_id": "unique_session_id"
}
```

Response:
```json
{
  "response": "Bot response text",
  "intent": "detected_intent",
  "lead_captured": false
}
```

### Leads Endpoint (Admin)
**GET** `/leads`

Returns all captured leads with conversation history.

### Health Check
**GET** `/health`

Returns service status.

## Knowledge Base

The chatbot includes comprehensive information about:

### Brand Information
- Neralu Farms mission and values
- Brand positioning and unique selling points
- Core value propositions

### Managed Farmland Concept
- Ownership model explanation
- Management approach
- Key benefits and advantages

### Projects
- **Korlaparti Project**: Features, location, status
- **Sandal Valley Project**: Features, location, status

### Plantations
- Mango plantations
- Coconut plantations
- Timber plantations
- Sandalwood plantations

### Investment Details
- Return expectations
- Investment timeline
- Legal compliance
- Payment options

### Amenities & Infrastructure
- Physical infrastructure
- Lifestyle amenities
- Maintenance services

## Customization

### Adding New Intents
Edit the `INTENT_PATTERNS` dictionary in `app.py`:
```python
INTENT_PATTERNS = {
    "new_intent": ["keyword1", "keyword2", "phrase"],
    # ... existing intents
}
```

### Updating Responses
Modify the `generate_response()` function to add new response templates.

### Expanding Knowledge Base
Update the `NERALU_KNOWLEDGE` dictionary with additional information:
```python
NERALU_KNOWLEDGE = {
    "new_category": {
        "key": "value",
        # ... more data
    }
}
```

## Integration Options

### Website Integration (Iframe)
```html
<iframe 
    src="http://your-domain.com" 
    width="400" 
    height="600" 
    frameborder="0"
    style="border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
</iframe>
```

### Widget Integration
The chatbot can be converted into a floating widget by adding a trigger button and showing/hiding the chat container.

### API Integration
Use the `/chat` endpoint to integrate with existing applications or custom interfaces.

## Deployment

### Option 1: Cloud Platforms (Heroku, AWS, Google Cloud)
1. Create `Procfile`:
```
web: gunicorn app:app
```

2. Deploy using platform-specific commands

### Option 2: Docker
Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t neralu-chatbot .
docker run -p 5000:5000 neralu-chatbot
```

### Option 3: Traditional Server
1. Install dependencies
2. Set up Nginx as reverse proxy
3. Run with Gunicorn or uWSGI
4. Use systemd for process management

## Future Enhancements

### Recommended Additions
1. **Database Integration**: Replace in-memory storage with PostgreSQL/MongoDB
2. **AI Integration**: Connect to OpenAI GPT-4 or Anthropic Claude for more natural conversations
3. **Multi-language Support**: Add Kannada language support
4. **Admin Dashboard**: Build a web interface for managing leads and conversations
5. **Analytics**: Track conversation metrics and user engagement
6. **CRM Integration**: Connect with Salesforce, HubSpot, or custom CRM
7. **WhatsApp Integration**: Enable chatbot on WhatsApp Business API
8. **Voice Support**: Add speech-to-text for voice queries
9. **Rich Media**: Support image and video sharing
10. **Appointment Scheduling**: Integrate with calendar for site visits

## Security Considerations

### For Production Deployment
1. **Add Authentication**: Protect admin endpoints with authentication
2. **Rate Limiting**: Implement rate limiting to prevent abuse
3. **Input Validation**: Add comprehensive input sanitization
4. **HTTPS**: Always use SSL/TLS in production
5. **Environment Variables**: Store sensitive configuration in environment variables
6. **CORS Configuration**: Restrict CORS to specific domains
7. **Database Security**: Use parameterized queries and proper access controls

## Support & Maintenance

### Regular Updates Needed
- Update knowledge base with new projects and offers
- Refine intent detection based on user queries
- Add new FAQs based on common questions
- Update pricing guidance as needed
- Refresh seasonal offers and promotions

## License

Proprietary - Neralu Farms

## Contact

For technical support or customization requests, contact the Neralu Farms technical team.

---

**Note**: This chatbot is designed to be a starting point. For production use, consider integrating with advanced AI services (OpenAI GPT-4, Anthropic Claude) for more sophisticated natural language understanding and contextual responses.
