#!/usr/bin/env python3
"""
Test Google Cloud TTS Authentication
"""
import os
import json
from google.cloud import texttospeech
from google.oauth2 import service_account

def test_tts_authentication():
    """Test Google Cloud TTS authentication and basic functionality"""
    try:
        print("🔍 Testing Google Cloud TTS Authentication...")
        
        # Get credentials from environment
        credentials_json_str = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', '{}')
        print(f"📋 Credentials string length: {len(credentials_json_str)} characters")
        
        if len(credentials_json_str) < 100:
            print("❌ GOOGLE_APPLICATION_CREDENTIALS appears to be empty or invalid")
            return False
            
        # Parse credentials
        credentials_json = json.loads(credentials_json_str)
        print(f"📧 Service account email: {credentials_json.get('client_email', 'Not found')}")
        print(f"🆔 Project ID: {credentials_json.get('project_id', 'Not found')}")
        
        # Create credentials object
        credentials = service_account.Credentials.from_service_account_info(credentials_json)
        print("✅ Credentials object created successfully")
        
        # Create TTS client
        client = texttospeech.TextToSpeechClient(credentials=credentials)
        print("✅ TTS client created successfully")
        
        # Test basic functionality with a simple synthesis request
        print("🎵 Testing text-to-speech synthesis...")
        
        synthesis_input = texttospeech.SynthesisInput(text="Hello, this is a test.")
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US",
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )
        
        # Make the synthesis request
        response = client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )
        
        print(f"✅ TTS synthesis successful! Audio size: {len(response.audio_content)} bytes")
        
        # Test if we can list voices (additional permission check)
        print("🎤 Testing voice listing capability...")
        voices_request = texttospeech.ListVoicesRequest()
        voices = client.list_voices(request=voices_request)
        print(f"✅ Voice listing successful! Found {len(voices.voices)} voices")
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {str(e)}")
        print("The GOOGLE_APPLICATION_CREDENTIALS contains invalid JSON")
        return False
    except Exception as e:
        print(f"❌ TTS Authentication Error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    success = test_tts_authentication()
    print(f"\n{'='*50}")
    if success:
        print("🎉 Google Cloud TTS Authentication: SUCCESS")
    else:
        print("💥 Google Cloud TTS Authentication: FAILED")
    print(f"{'='*50}")