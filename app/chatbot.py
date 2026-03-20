def ask_chatbot(message, disease=None):

    message = message.strip().lower()

    # Greeting
    if message in ["hi", "hello", "hey"]:
        return {
            "reply": "👋 Hello! I can help you find nearby dermatologists.\nPlease enter your 6-digit pincode."
        }

    # Check pincode
    if message.isdigit() and len(message) == 6:

        if not disease:
            return {
                "reply": "⚠️ Please complete prediction first before searching doctors."
            }

        return {
            "action": "FETCH_DOCTORS",
            "pincode": message,
            "disease": disease
        }

    return {
        "reply": "❗ Please enter a valid 6-digit pincode."
    }