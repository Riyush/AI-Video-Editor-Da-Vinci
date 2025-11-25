from django.contrib import admin
from django.urls import path
from .views import transcribe_audio, transcribe_audio_groq

urlpatterns = [
    path('transcribe_audio', transcribe_audio),
    path('transcribe_audio_groq', transcribe_audio_groq),
]
