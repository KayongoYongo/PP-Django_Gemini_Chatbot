from dotenv import load_dotenv
import google.generativeai as genai
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Load environmental variables from a .env file
load_dotenv()

# Access the Google API key from the loaded environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the generative AI client with the API key
genai.configure(api_key=API_KEY)

# Select the generative AI model to use
model = genai.GenerativeModel('gemini-pro')

# Start a new chat session with an empty history
chat = model.start_chat(history=[])

# Instruction to the model for the style of responses
instruction = "In this chat, respond as if you are explaining to a five-year-old child."

class ChatAPIView(APIView):
    def post(self, request):
        # Get the question from the POST request
        question = request.data.get('question', '')

        # If the question is empty, return an error
        if not question:
            return Response({'error': 'Question is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Send the user's question along with the instruction to the chat model
        response = chat.send_message(instruction + question)

        # Return the response as JSON
        return Response({'response': response.text})