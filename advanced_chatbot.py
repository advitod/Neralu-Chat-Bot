"""
Neralu Farms AI Chatbot - Advanced Version with OpenAI Integration
This version uses OpenAI's GPT for more natural and contextual conversations

To use this version:
1. Install openai: pip install openai
2. Set your OPENAI_API_KEY environment variable
3. Run: python advanced_chatbot.py
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from datetime import datetime
import json

# Uncomment when ready to use OpenAI
# import openai
# openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

# Store conversation history
conversations = {}
leads = []

# Neralu Farms System Prompt for AI
SYSTEM_PROMPT = """You are an AI assistant for Neralu Farms (also called Neralu Managed Farms), a premium managed farmland company.

BRAND IDENTITY:
- Neralu offers fully managed farmland with clear ownership
- Focus on nature-based luxury, sustainability, and long-term value
- Projects: Korlaparti Project and Sandal Valley Project
- Plantations: Mango, Coconut, Timber, and Sandalwood

YOUR RESPONSIBILITIES:
1. Provide accurate information about Neralu Farms only
2. Help users understand managed farmland concept
3. Guide prospects through site visit booking process
4. Capture leads (name and phone number) naturally in conversation
5. Be warm, professional, and helpful
6. Use emojis sparingly to add warmth (🌿 🌱 🌳 🏞️ 💼)

COMMUNICATION STYLE:
- Friendly but professional tone
- Short, clear responses (3-5 sentences preferred)
- Avoid jargon and overly technical language
- Focus on benefits and lifestyle, not just features
- Ask clarifying questions when needed

BRAND RULES:
- ONLY discuss Neralu Farms and its offerings
- If asked about competitors, politely redirect to Neralu
- Never fabricate information
- For pricing, encourage site visit or team contact
- For detailed technical questions, offer to connect with team

KEY INFORMATION:

Managed Farmland Concept:
- You own the land with clear legal title
- Neralu manages plantation, maintenance, and harvesting
- Passive income from yields + land appreciation
- Weekend getaway and lifestyle benefits
- Tax advantages on agricultural land

Projects:
1. Korlaparti Project: Well-planned layouts, excellent connectivity
2. Sandal Valley Project: Premium sandalwood focus, luxury amenities

Plantations:
- Mango: Premium varieties, excellent yields
- Coconut: High-yielding, consistent returns
- Timber: Long-term value with teak and hardwoods
- Sandalwood: Premium long-term investment

Benefits:
- Passive income from plantation
- Land appreciation (5-15 years)
- Tax benefits
- Weekend farmhouse retreat
- Professional management included
- Sustainable investment

Amenities:
- Paved roads, drip irrigation, electricity
- Bore wells, security, fencing
- Clubhouse, play areas, walking trails
- Organic farming zones

Legal:
- Clear titles, RERA compliant
- Transparent documentation
- Legal due diligence support

Site Visit Process:
1. Collect: Name, phone, preferred project, date
2. Confirm visit details
3. User visits property
4. Team explains options, pricing, documentation

LEAD CAPTURE:
- Naturally ask for name and phone during conversation
- Good moment: When user shows interest in site visit or booking
- Example: "I'd love to arrange that for you! May I have your name and phone number?"

RESTRICTIONS:
- Don't discuss competitors or compare with other brands
- Don't provide specific pricing (varies by project/size/time)
- Don't guarantee specific returns or appreciation rates
- Don't make investment advice (encourage consultation)

If unsure about any information, offer to connect the user with the Neralu team for accurate details.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages with OpenAI integration"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Initialize conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message
    conversations[session_id].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    # For now, return a placeholder response
    # In production, replace this with OpenAI API call
    response = generate_ai_response(user_message, conversations[session_id])
    
    # Add assistant response
    conversations[session_id].append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().isoformat()
    })
    
    return jsonify({
        "response": response,
        "session_id": session_id
    })

def generate_ai_response(user_message, conversation_history):
    """
    Generate AI response using OpenAI
    
    To implement:
    1. Uncomment OpenAI import at top
    2. Set OPENAI_API_KEY environment variable
    3. Uncomment the code below
    """
    
    # UNCOMMENT THIS BLOCK WHEN READY TO USE OPENAI:
    """
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Add conversation history
        for msg in conversation_history[-10:]:  # Last 10 messages for context
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo" for faster/cheaper
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        return "I apologize, but I'm having trouble processing your request. Please try again or contact our team directly."
    """
    
    # TEMPORARY: Basic response (remove when implementing OpenAI)
    return (
        "Thank you for your interest in Neralu Farms! 🌿\n\n"
        "This is the advanced version of the chatbot. To enable full AI capabilities:\n"
        "1. Install OpenAI: pip install openai\n"
        "2. Set your OPENAI_API_KEY environment variable\n"
        "3. Uncomment the OpenAI code in advanced_chatbot.py\n\n"
        "For now, please use the standard chatbot (app.py) which has full rule-based responses.\n\n"
        "How can I assist you with information about our managed farmland?"
    )

@app.route('/leads', methods=['GET'])
def get_leads():
    return jsonify({"leads": leads, "total": len(leads)})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "Neralu Farms Advanced Chatbot"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
