"""
Neralu Farms AI Chatbot - Backend Application
This Flask application powers the AI chatbot for Neralu Farms
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
from datetime import datetime
import json
import re

app = Flask(__name__)
CORS(app)

# Store conversation history (in production, use a database)
conversations = {}
leads = []

# Neralu Farms Knowledge Base
NERALU_KNOWLEDGE = {
    "brand_info": {
        "name": "Neralu Farms / Neralu Managed Farms",
        "tagline": "Nature-based luxury managed farmland",
        "mission": "To provide sustainable managed farmland ownership with long-term returns and lifestyle benefits",
        "values": ["Sustainability", "Transparency", "Trust", "Nature-focused living", "Long-term value creation"],
        "positioning": "Premium managed farmland investment combining lifestyle, returns, and environmental consciousness"
    },
    
    "concept": {
        "managed_farmland": "Neralu offers fully managed farmland where you own the land while we handle plantation, maintenance, and management. It's a hassle-free investment in nature.",
        "ownership_model": "You own the farmland with clear legal titles. Neralu manages the plantation, irrigation, maintenance, and harvesting.",
        "benefits": [
            "Passive income through plantation yields",
            "Land appreciation over time",
            "Weekend getaway and lifestyle amenity",
            "Tax benefits on agricultural land",
            "Sustainable and eco-friendly investment",
            "Professional farm management included"
        ]
    },
    
    "plantations": {
        "mango": "Premium mango varieties with excellent yield potential and market demand",
        "coconut": "High-yielding coconut plantations with consistent returns",
        "timber": "Long-term timber plantations including teak and other hardwoods",
        "sandalwood": "Premium sandalwood plantation with exceptional long-term value"
    },
    
    "projects": {
        "korlaparti": {
            "name": "Korlaparti Project",
            "location": "Korlaparti area with excellent connectivity",
            "features": ["Well-planned layouts", "Water infrastructure", "Road connectivity", "Community spaces"],
            "status": "Available for booking"
        },
        "sandal_valley": {
            "name": "Sandal Valley Project",
            "location": "Premium location for sandalwood plantation",
            "features": ["Sandalwood focus", "Premium amenities", "Gated community", "Luxury farmhouse plots"],
            "status": "Available for booking"
        }
    },
    
    "amenities": {
        "infrastructure": ["Paved internal roads", "Drip irrigation system", "Bore wells and water storage", "Electricity connection", "Security and fencing"],
        "lifestyle": ["Clubhouse", "Children's play area", "Walking trails", "Organic farming zones", "Event spaces"],
        "maintenance": "Professional farm management team handles all plantation care, irrigation, fertilization, and harvesting"
    },
    
    "investment": {
        "returns": "Combination of land appreciation and plantation yields over time",
        "timeline": "Medium to long-term investment (5-15 years) with progressive returns",
        "legal": "Clear legal titles, RERA compliance where applicable, and transparent documentation",
        "payment": "Flexible payment plans available. Contact team for current pricing and offers"
    }
}

# Conversation intents and responses
INTENT_PATTERNS = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening", "namaste"],
    "about_neralu": ["who are you", "about neralu", "tell me about", "what is neralu", "about company"],
    "managed_farmland": ["managed farmland", "what is managed", "how does it work", "ownership model"],
    "plantations": ["plantation", "mango", "coconut", "timber", "sandalwood", "crops", "what can i grow"],
    "projects": ["projects", "locations", "where", "korlaparti", "sandal valley"],
    "benefits": ["benefits", "why invest", "returns", "advantages", "profit"],
    "amenities": ["amenities", "facilities", "infrastructure", "clubhouse"],
    "pricing": ["price", "cost", "how much", "rates", "payment"],
    "site_visit": ["visit", "site visit", "can i visit", "show me", "tour"],
    "booking": ["book", "buy", "purchase", "interested", "want to invest"],
    "legal": ["legal", "documents", "title", "rera", "registration"],
    "contact": ["contact", "phone", "email", "reach you", "talk to someone"]
}

def detect_intent(user_message):
    """Detect user intent from message"""
    message_lower = user_message.lower()
    
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if pattern in message_lower:
                return intent
    
    return "general"

def generate_response(intent, user_message, conversation_history):
    """Generate contextual response based on intent"""
    
    responses = {
        "greeting": f"Hello! 🌿 Welcome to Neralu Farms. I'm here to help you explore our managed farmland opportunities. \n\nHow can I assist you today? You can ask me about:\n• Our managed farmland concept\n• Available projects and plantations\n• Investment benefits and returns\n• Booking a site visit\n\nWhat interests you most?",
        
        "about_neralu": f"Neralu Farms (also called Neralu Managed Farms) offers premium managed farmland where you own beautiful agricultural land while we handle everything else! 🌳\n\n**Our Mission:** {NERALU_KNOWLEDGE['brand_info']['mission']}\n\n**What makes us special:**\n• You own the land with clear legal titles\n• We manage plantation, maintenance & harvesting\n• Enjoy lifestyle amenities + long-term returns\n• Sustainable, nature-focused investment\n\nWould you like to know more about our projects or how managed farmland works?",
        
        "managed_farmland": f"Great question! Let me explain how Neralu's managed farmland works: 🌾\n\n**The Concept:**\n{NERALU_KNOWLEDGE['concept']['managed_farmland']}\n\n**Ownership Model:**\n{NERALU_KNOWLEDGE['concept']['ownership_model']}\n\n**Key Benefits:**\n" + "\n".join([f"✓ {benefit}" for benefit in NERALU_KNOWLEDGE['concept']['benefits']]) + "\n\nIt's perfect for those who want farmland ownership without the hassle of daily management!\n\nWould you like to know about our plantation options or current projects?",
        
        "plantations": f"We offer diverse plantation options at Neralu Farms! 🌱\n\n**Available Plantations:**\n\n🥭 **Mango:** {NERALU_KNOWLEDGE['plantations']['mango']}\n\n🥥 **Coconut:** {NERALU_KNOWLEDGE['plantations']['coconut']}\n\n🌲 **Timber:** {NERALU_KNOWLEDGE['plantations']['timber']}\n\n🪵 **Sandalwood:** {NERALU_KNOWLEDGE['plantations']['sandalwood']}\n\nEach plantation is professionally managed with optimal care for maximum yields. Which plantation interests you most?",
        
        "projects": f"We have two exciting projects available! 🏞️\n\n**1. {NERALU_KNOWLEDGE['projects']['korlaparti']['name']}**\nLocation: {NERALU_KNOWLEDGE['projects']['korlaparti']['location']}\nHighlights: {', '.join(NERALU_KNOWLEDGE['projects']['korlaparti']['features'])}\n\n**2. {NERALU_KNOWLEDGE['projects']['sandal_valley']['name']}**\nLocation: {NERALU_KNOWLEDGE['projects']['sandal_valley']['location']}\nHighlights: {', '.join(NERALU_KNOWLEDGE['projects']['sandal_valley']['features'])}\n\nBoth projects are thoughtfully planned with excellent connectivity and premium amenities. Would you like detailed information about either project?",
        
        "benefits": f"Investing in Neralu Farms offers multiple advantages! 💰🌿\n\n**Financial Benefits:**\n• Passive income from plantation yields\n• Land appreciation over 5-15 years\n• Tax benefits on agricultural land\n• Diversification of investment portfolio\n\n**Lifestyle Benefits:**\n• Your own weekend farmhouse getaway\n• Fresh organic produce\n• Connect with nature\n• Community of like-minded investors\n\n**Peace of Mind:**\n• Professional management included\n• Clear legal documentation\n• Sustainable & eco-friendly\n• Long-term wealth creation\n\n{NERALU_KNOWLEDGE['investment']['returns']}\n\nWould you like to discuss investment timelines or book a site visit?",
        
        "amenities": f"Neralu Farms comes with excellent infrastructure and lifestyle amenities! 🏡\n\n**Infrastructure:**\n" + "\n".join([f"✓ {item}" for item in NERALU_KNOWLEDGE['amenities']['infrastructure']]) + "\n\n**Lifestyle Amenities:**\n" + "\n".join([f"✓ {item}" for item in NERALU_KNOWLEDGE['amenities']['lifestyle']]) + f"\n\n**Maintenance:**\n{NERALU_KNOWLEDGE['amenities']['maintenance']}\n\nEverything is designed for your convenience and comfort. Would you like to see this in person with a site visit?",
        
        "pricing": "I'd be happy to discuss pricing with you! 💼\n\nOur farmland pricing varies based on:\n• Project location (Korlaparti or Sandal Valley)\n• Plot size and layout\n• Plantation type chosen\n• Current offers and payment plans\n\nFor the most accurate and up-to-date pricing, I recommend:\n1. **Booking a site visit** - See the property and get detailed pricing\n2. **Speaking with our sales team** - They can share current rates and special offers\n\nWe also offer flexible payment plans to make your investment easier.\n\nWould you like me to help you schedule a site visit or connect you with our team?",
        
        "site_visit": "Wonderful! A site visit is the best way to experience Neralu Farms! 🚗\n\nDuring your visit, you'll:\n✓ Tour the actual farmland\n✓ See infrastructure and amenities\n✓ Meet our farm management team\n✓ Understand plantation options\n✓ Get detailed pricing and documentation\n✓ See sample farmhouses (if available)\n\n**To book your site visit, I'll need:**\n• Your name\n• Phone number\n• Preferred project (Korlaparti / Sandal Valley / Both)\n• Preferred date/time\n\nWould you like to share these details now so I can arrange your visit?",
        
        "booking": "That's exciting! Thank you for your interest in Neralu Farms! 🎉\n\nHere's how the booking process works:\n\n**Step 1:** Site Visit (if not done already)\n**Step 2:** Select your preferred project and plot\n**Step 3:** Documentation and verification\n**Step 4:** Payment plan discussion\n**Step 5:** Agreement signing and registration\n**Step 6:** Plantation begins!\n\nTo get started, I can:\n1. Schedule a site visit for you\n2. Connect you with our sales team\n3. Share project brochures and details\n\nMay I have your name and phone number to help you proceed?",
        
        "legal": f"Legal clarity is a priority at Neralu! 📄\n\n**Legal Aspects:**\n{NERALU_KNOWLEDGE['investment']['legal']}\n\n**What you get:**\n✓ Clear and marketable title\n✓ Sale deed in your name\n✓ All necessary government approvals\n✓ Transparent documentation\n✓ Legal due diligence support\n\nWe believe in complete transparency and legal compliance. Our team can walk you through all documentation during your site visit.\n\nWould you like to schedule a visit or speak with our legal team?",
        
        "contact": "I'm here to help, but for detailed assistance, here's how you can reach Neralu Farms: 📞\n\n**Contact Options:**\n• I can collect your details and have our team call you\n• You can request a site visit and meet the team in person\n• For immediate queries, share your question and I'll do my best to help\n\nWould you like me to have our team contact you? If yes, please share:\n• Your name\n• Phone number\n• Best time to call",
        
        "general": "I'm here to help you with information about Neralu Farms! 🌿\n\nI can assist you with:\n• Understanding managed farmland concept\n• Details about our projects (Korlaparti & Sandal Valley)\n• Plantation options (Mango, Coconut, Timber, Sandalwood)\n• Investment benefits and returns\n• Amenities and infrastructure\n• Booking site visits\n• Legal and documentation info\n\nWhat would you like to know more about?"
    }
    
    return responses.get(intent, responses["general"])

def extract_lead_info(conversation_history):
    """Extract name and phone number from conversation"""
    lead_info = {"name": None, "phone": None}
    
    for msg in conversation_history:
        if msg["role"] == "user":
            text = msg["content"]
            
            # Extract phone number (Indian format)
            phone_pattern = r'(\+?91[-\s]?)?[6-9]\d{9}'
            phone_match = re.search(phone_pattern, text)
            if phone_match and not lead_info["phone"]:
                lead_info["phone"] = phone_match.group()
            
            # Extract name (simple heuristic)
            if not lead_info["name"]:
                words = text.split()
                if len(words) >= 2 and words[0].lower() in ["my", "name", "i'm", "i", "am"]:
                    potential_name = " ".join(words[1:4])
                    if len(potential_name) > 2 and not any(char.isdigit() for char in potential_name):
                        lead_info["name"] = potential_name.strip(".,!?")
    
    return lead_info

@app.route('/')
def home():
    """Serve chatbot interface"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.json
    user_message = data.get('message', '')
    session_id = data.get('session_id', 'default')
    
    # Initialize conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    # Add user message to history
    conversations[session_id].append({
        "role": "user",
        "content": user_message,
        "timestamp": datetime.now().isoformat()
    })
    
    # Detect intent and generate response
    intent = detect_intent(user_message)
    response = generate_response(intent, user_message, conversations[session_id])
    
    # Add bot response to history
    conversations[session_id].append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now().isoformat(),
        "intent": intent
    })
    
    # Extract lead information if present
    lead_info = extract_lead_info(conversations[session_id])
    
    # Save lead if we have contact info
    if lead_info["phone"] and lead_info not in leads:
        lead_info["session_id"] = session_id
        lead_info["conversation"] = conversations[session_id]
        lead_info["captured_at"] = datetime.now().isoformat()
        leads.append(lead_info)
    
    return jsonify({
        "response": response,
        "intent": intent,
        "lead_captured": bool(lead_info["phone"])
    })

@app.route('/leads', methods=['GET'])
def get_leads():
    """Get captured leads (admin endpoint)"""
    return jsonify({"leads": leads, "total": len(leads)})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "Neralu Farms Chatbot"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
