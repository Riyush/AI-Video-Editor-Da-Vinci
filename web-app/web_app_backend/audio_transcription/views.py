from django.shortcuts import render
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.conf import settings
import json
import requests
import openai
from groq import Groq
import tempfile

# Create the OpenAI client
client = openai.OpenAI(
    api_key=settings.OPENAI_API_KEY
)

# Create the GROQ client for precise transcription
groq_client = Groq(api_key=settings.GROQ_API_KEY, )

@api_view(['POST'])
@parser_classes([MultiPartParser])
def transcribe_audio(request):
    audio_file = request.FILES.get('file')

    if not audio_file:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Handle TemporaryUploadedFile vs InMemoryUploadedFile
        # convert memory based file to a temp file for transmission to API
        if hasattr(audio_file, "temporary_file_path"):
            file_path = audio_file.temporary_file_path()
        else:
            # Create a temporary file on disk for in-memory uploads
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                for chunk in audio_file.chunks():
                    tmp.write(chunk)
                file_path = tmp.name

        with open(file_path, "rb") as wav_file:
            transcript_response = client.audio.transcriptions.create(
                model="gpt-4o-mini-transcribe",
                file=wav_file,
                response_format="json"
            )
        
        # ✅ Force conversion to a pure Python dict
        transcript_dict = transcript_response.model_dump() if hasattr(transcript_response, "model_dump") else dict(transcript_response)

        return Response({"transcript": transcript_dict}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@parser_classes([MultiPartParser])
def transcribe_audio_groq(request):

    audio_file = request.FILES.get('file')

    if not audio_file:
        return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Handle TemporaryUploadedFile vs InMemoryUploadedFile
        # convert memory based file to a temp file for transmission to API
        if hasattr(audio_file, "temporary_file_path"):
            file_path = audio_file.temporary_file_path()
        else:
            # Create a temporary file on disk for in-memory uploads
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
                for chunk in audio_file.chunks():
                    tmp.write(chunk)
                file_path = tmp.name

        with open(file_path, "rb") as wav_file:
            transcript_response = groq_client.audio.transcriptions.create(
                model="whisper-large-v3-turbo", # Required model to use for transcription
                file=wav_file,
                response_format="verbose_json",
                timestamp_granularities=["word"]
            )
        
        # ✅ Force conversion to a pure Python dict
        # Remember that we are returning a transcript object which contains additional metadata
        # in addition to the transcript
        transcript_dict = transcript_response.model_dump() if hasattr(transcript_response, "model_dump") else dict(transcript_response)

        return Response({"transcript": transcript_dict}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)