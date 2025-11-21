import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
from data import orders_db, policy_db  # Import our synthetic data

# Load API Key from .env file
load_dotenv()
MY_API_KEY = "AIzaSyCDT5OWdO-tryvTQOZ224haI8H8kH9jSVY"

genai.configure(api_key=MY_API_KEY)

app = Flask(__name__)

# Configure the Model
model = genai.GenerativeModel('gemini-2.5-flash')
chat = model.start_chat(history=[])

def build_system_prompt(user_input):
    """
    This function checks if the user provided an Order ID and injects
    that specific order's data into the context for Gemini.
    """
    context_data = ""

    # 1. Basic Policy Context (Always available to the bot)
    context_data += f"\n\nCOMPANY POLICIES:\n{policy_db}"

    # 2. Dynamic Order Lookup (Simulating a DB query)
    # A simple check to see if any known Order ID is in the user's message
    found_order = False
    for order_id, details in orders_db.items():
        if order_id in user_input.upper():
            context_data += f"\n\nUSER ORDER DATA found for {order_id}: {str(details)}"
            found_order = True
            break

    # 3. Construct the final prompt
    system_instruction = f"""
    You are a helpful customer support chatbot for "TechStore".
    Use the data below to answer the user's question.
    If the user asks about an order, check the ORDER DATA section.
    If the user asks about returns/shipping, check the COMPANY POLICIES.
    If you don't know the answer, strictly say "I cannot find that information."
    
    DATA CONTEXT:
    {context_data}
    """
    return system_instruction

@app.route("/")
def home():
    return "working"

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.form["msg"]

    # Create the context-aware prompt
    system_context = build_system_prompt(user_message)
    full_prompt = f"{system_context}\n\nUser Question: {user_message}"

    try:
        # Send to Gemini
        response = chat.send_message(full_prompt)
        return jsonify({"response": response.text})
    except Exception as e:
        print(f"\n🛑 ERROR DETAILS: {e}\n")
        return jsonify({"response": "Sorry, I encountered an error processing your request."})

if __name__ == "__main__":
    app.run(debug=True)