# Neralu Farms Chatbot - Deployment Guide

## Quick Start (Local Testing)

### Step 1: Install Dependencies
```bash
cd neralu_chatbot
pip install -r requirements.txt
```

### Step 2: Run the Chatbot
```bash
python app.py
```

### Step 3: Open in Browser
Navigate to: `http://localhost:5000`

---

## Production Deployment Options

### Option 1: Deploy to Heroku (Easiest)

#### Prerequisites
- Heroku account (free tier available)
- Heroku CLI installed

#### Steps
1. **Create Procfile**
   ```bash
   echo "web: gunicorn app:app" > Procfile
   ```

2. **Initialize Git**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   ```

3. **Create Heroku App**
   ```bash
   heroku create neralu-chatbot
   ```

4. **Deploy**
   ```bash
   git push heroku master
   ```

5. **Open Your App**
   ```bash
   heroku open
   ```

**Cost**: Free tier available (may sleep after 30 mins inactivity)

---

### Option 2: Deploy to AWS EC2

#### Steps
1. **Launch EC2 Instance**
   - Choose Ubuntu Server 20.04 LTS
   - t2.micro (free tier eligible)
   - Configure security group: Allow HTTP (80), HTTPS (443), SSH (22)

2. **Connect via SSH**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip nginx -y
   ```

4. **Upload Your Code**
   ```bash
   # On your local machine
   scp -i your-key.pem -r neralu_chatbot ubuntu@your-ec2-ip:~/
   ```

5. **Install Python Packages**
   ```bash
   cd neralu_chatbot
   pip3 install -r requirements.txt
   ```

6. **Configure Nginx**
   ```bash
   sudo nano /etc/nginx/sites-available/neralu
   ```
   
   Add:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

7. **Enable Site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/neralu /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

8. **Run with Gunicorn**
   ```bash
   gunicorn --bind 0.0.0.0:5000 app:app --daemon
   ```

**Cost**: ~$10-15/month for t2.micro instance

---

### Option 3: Deploy to Google Cloud Run (Recommended for Scalability)

#### Steps
1. **Install Google Cloud SDK**

2. **Create Dockerfile** (already provided)

3. **Build and Push Container**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/neralu-chatbot
   ```

4. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy neralu-chatbot \
     --image gcr.io/YOUR-PROJECT-ID/neralu-chatbot \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

**Cost**: Pay per use, free tier includes 2 million requests/month

---

### Option 4: Deploy to Railway.app (Easiest Modern Option)

#### Steps
1. Go to [Railway.app](https://railway.app)
2. Sign up with GitHub
3. Create new project → Deploy from GitHub repo
4. Select your chatbot repository
5. Railway auto-detects Flask and deploys
6. Get your public URL

**Cost**: Free tier with $5/month credit, then pay as you go

---

### Option 5: Deploy to Your Own Server (cPanel/VPS)

#### For cPanel Hosting
1. **Upload Files**
   - Use File Manager or FTP to upload all files

2. **Create Python App**
   - In cPanel, go to "Setup Python App"
   - Select Python version (3.8+)
   - Set application root to `/neralu_chatbot`
   - Set application URL to `/chat` or subdomain

3. **Install Requirements**
   - Use terminal in cPanel or SSH
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure & Start**
   - cPanel will provide a URL
   - Access your chatbot at that URL

#### For Traditional VPS (DigitalOcean, Linode, etc.)
Similar to AWS EC2 steps above.

**Cost**: Varies, typically $5-20/month

---

## Website Integration

### Method 1: Full Page Integration
Simply link to your deployed chatbot URL:
```html
<a href="https://your-chatbot-url.com">Chat with us</a>
```

### Method 2: Iframe Embed
Embed chatbot in your existing website:
```html
<iframe 
    src="https://your-chatbot-url.com" 
    width="100%" 
    height="600px" 
    frameborder="0"
    style="border: none; border-radius: 10px;">
</iframe>
```

### Method 3: Floating Widget (Recommended)
Add this to your website's HTML (before `</body>`):

```html
<!-- Neralu Chatbot Widget -->
<div id="neralu-chat-widget" style="display: none; position: fixed; bottom: 20px; right: 20px; width: 400px; height: 600px; z-index: 9999; box-shadow: 0 5px 40px rgba(0,0,0,0.3); border-radius: 10px; overflow: hidden;">
    <iframe 
        src="https://your-chatbot-url.com" 
        width="100%" 
        height="100%" 
        frameborder="0">
    </iframe>
</div>

<button 
    id="neralu-chat-button" 
    onclick="toggleChat()"
    style="position: fixed; bottom: 20px; right: 20px; width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #4a7c2c 0%, #5d9938 100%); border: none; color: white; font-size: 30px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.3); z-index: 9998;">
    🌿
</button>

<script>
function toggleChat() {
    const widget = document.getElementById('neralu-chat-widget');
    const button = document.getElementById('neralu-chat-button');
    
    if (widget.style.display === 'none') {
        widget.style.display = 'block';
        button.style.display = 'none';
    } else {
        widget.style.display = 'none';
        button.style.display = 'block';
    }
}
</script>
```

### Method 4: API Integration
Use the `/chat` endpoint for custom integration:

```javascript
async function sendMessage(message) {
    const response = await fetch('https://your-chatbot-url.com/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            message: message,
            session_id: 'unique_user_id'
        })
    });
    
    const data = await response.json();
    return data.response;
}
```

---

## Advanced: AI-Powered Version Setup

### Using OpenAI GPT-4

1. **Get OpenAI API Key**
   - Sign up at [OpenAI](https://platform.openai.com)
   - Get API key from API settings

2. **Install OpenAI Package**
   ```bash
   pip install openai
   ```

3. **Set Environment Variable**
   ```bash
   export OPENAI_API_KEY='your-api-key-here'
   ```

4. **Use Advanced Version**
   ```bash
   python advanced_chatbot.py
   ```

5. **Uncomment OpenAI Code**
   - Open `advanced_chatbot.py`
   - Uncomment the OpenAI integration code
   - Test with real conversations

**Benefits of AI Version:**
- More natural conversations
- Better context understanding
- Handles unexpected questions
- Learns from conversation flow
- More human-like responses

**Cost**: 
- GPT-4: ~$0.03 per 1K tokens (1 conversation ≈ $0.05-0.10)
- GPT-3.5-turbo: ~$0.002 per 1K tokens (1 conversation ≈ $0.01)

---

## Database Setup (Optional but Recommended for Production)

### Using PostgreSQL

1. **Install PostgreSQL** (or use managed service like AWS RDS)

2. **Create Database**
   ```sql
   CREATE DATABASE neralu_chatbot;
   ```

3. **Update Code** to use database instead of in-memory storage:
   ```python
   import psycopg2
   
   conn = psycopg2.connect(
       dbname="neralu_chatbot",
       user="your_user",
       password="your_password",
       host="localhost"
   )
   ```

4. **Create Tables**
   ```sql
   CREATE TABLE conversations (
       id SERIAL PRIMARY KEY,
       session_id VARCHAR(255),
       role VARCHAR(50),
       content TEXT,
       timestamp TIMESTAMP
   );
   
   CREATE TABLE leads (
       id SERIAL PRIMARY KEY,
       name VARCHAR(255),
       phone VARCHAR(20),
       session_id VARCHAR(255),
       captured_at TIMESTAMP
   );
   ```

---

## Monitoring & Analytics

### Add Google Analytics
Add this to `templates/index.html` before `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=YOUR-GA-ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'YOUR-GA-ID');
</script>
```

### Custom Event Tracking
Track important events:
```javascript
// Track message sent
gtag('event', 'chat_message_sent', {
    'event_category': 'engagement',
    'event_label': 'user_query'
});

// Track lead captured
gtag('event', 'lead_captured', {
    'event_category': 'conversion',
    'value': 1
});
```

---

## Security Checklist for Production

- [ ] Enable HTTPS (use Let's Encrypt for free SSL)
- [ ] Add rate limiting (Flask-Limiter)
- [ ] Implement authentication for admin endpoints
- [ ] Sanitize user inputs
- [ ] Use environment variables for secrets
- [ ] Enable CORS only for your domain
- [ ] Add logging and monitoring
- [ ] Regular security updates
- [ ] Backup database regularly
- [ ] Use strong session keys

---

## Troubleshooting

### Common Issues

**Issue**: Port already in use
```bash
# Solution: Change port or kill existing process
lsof -i :5000
kill -9 <PID>
```

**Issue**: Module not found
```bash
# Solution: Install missing package
pip install package-name
```

**Issue**: Permission denied
```bash
# Solution: Run with sudo or fix permissions
sudo chown -R $USER:$USER /path/to/project
```

---

## Support & Maintenance

### Regular Tasks
- Monitor lead capture rate
- Update knowledge base monthly
- Review conversation logs for improvement
- Test on different devices/browsers
- Update dependencies quarterly
- Backup data weekly

### Performance Optimization
- Use CDN for static files
- Enable gzip compression
- Minimize CSS/JS
- Use caching for static responses
- Consider Redis for session management

---

## Next Steps After Deployment

1. **Test Thoroughly**: Try various user queries
2. **Monitor Logs**: Check for errors or issues
3. **Gather Feedback**: Ask team and early users
4. **Iterate**: Improve responses based on real usage
5. **Scale**: Add AI capabilities when ready
6. **Integrate**: Connect with CRM, email, WhatsApp

---

**Need Help?** 
Contact the Neralu technical team for assistance with deployment or customization.
