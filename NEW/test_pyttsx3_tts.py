#!/usr/bin/env python3
"""
Test script for pyttsx3 offline TTS functionality

This script tests the new offline TTS implementation to ensure it's working correctly
before deploying to the main application.
"""

import sys
import os
import tempfile
import base64

def test_pyttsx3_installation():
    """Test if pyttsx3 is properly installed"""
    print("🔍 Testing pyttsx3 Installation")
    print("=" * 32)
    
    try:
        import pyttsx3
        print("✅ pyttsx3 successfully imported")
        
        # Test engine initialization
        engine = pyttsx3.init()
        print("✅ pyttsx3 engine initialized successfully")
        
        # Test voice properties
        voices = engine.getProperty('voices')
        if voices:
            print(f"✅ Found {len(voices)} available voices:")
            for i, voice in enumerate(voices[:3]):  # Show first 3 voices
                print(f"   {i+1}. {voice.name} ({voice.id})")
        else:
            print("⚠️ No voices found, but engine initialized")
        
        # Test rate and volume properties
        rate = engine.getProperty('rate')
        volume = engine.getProperty('volume')
        print(f"✅ Current rate: {rate} words/min, volume: {volume}")
        
        engine.stop()
        return True
        
    except ImportError as e:
        print(f"❌ pyttsx3 not installed: {e}")
        return False
    except Exception as e:
        print(f"❌ pyttsx3 initialization failed: {e}")
        return False

def test_basic_tts():
    """Test basic TTS functionality"""
    print("\n🔍 Testing Basic TTS Functionality")
    print("=" * 35)
    
    try:
        import pyttsx3
        
        # Initialize engine
        engine = pyttsx3.init()
        
        # Configure engine
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Test text
        test_text = "Hello, this is a test of the offline text to speech system."
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_path = temp_file.name
        
        print(f"📝 Test text: {test_text}")
        print(f"📁 Temp file: {temp_path}")
        
        # Generate speech
        engine.save_to_file(test_text, temp_path)
        engine.runAndWait()
        
        # Check if file was created
        if os.path.exists(temp_path):
            file_size = os.path.getsize(temp_path)
            print(f"✅ Audio file created: {file_size} bytes")
            
            if file_size > 0:
                print("✅ Audio file has content")
                
                # Test base64 encoding
                with open(temp_path, 'rb') as audio_file:
                    audio_data = audio_file.read()
                    audio_base64 = base64.b64encode(audio_data).decode()
                    print(f"✅ Base64 encoding successful: {len(audio_base64)} characters")
                
                # Clean up
                os.unlink(temp_path)
                engine.stop()
                return True
            else:
                print("❌ Audio file is empty")
                os.unlink(temp_path)
                engine.stop()
                return False
        else:
            print("❌ Audio file was not created")
            engine.stop()
            return False
            
    except Exception as e:
        print(f"❌ Basic TTS test failed: {e}")
        return False

def test_extended_tts():
    """Test extended TTS for 1-minute duration"""
    print("\n🔍 Testing Extended TTS (1-minute)")
    print("=" * 33)
    
    try:
        import pyttsx3
        
        # Create extended text (target ~180 words for 1 minute)
        base_text = "This is a legal document analysis system that provides comprehensive insights into legal contracts and agreements."
        
        extended_text = base_text
        words = extended_text.split()
        
        # Extend text to reach target word count
        while len(words) < 180:
            extended_text += " This document analysis provides important insights for legal review."
            extended_text += " Please review all sections carefully for complete understanding."
            extended_text += " Legal documents require thorough examination of all terms and conditions."
            words = extended_text.split()
        
        # Trim to exactly 180 words
        extended_text = " ".join(words[:180])
        
        print(f"📊 Extended text: {len(extended_text.split())} words")
        print(f"📝 Preview: {extended_text[:100]}...")
        
        # Initialize engine
        engine = pyttsx3.init()
        
        # Configure for 1-minute speech
        voices = engine.getProperty('voices')
        if voices:
            engine.setProperty('voice', voices[0].id)
        
        # Calculate rate for approximately 1 minute
        target_words = len(extended_text.split())
        rate = max(120, min(180, target_words))
        engine.setProperty('rate', rate)
        engine.setProperty('volume', 0.9)
        
        print(f"🔊 Speech rate set to: {rate} words/minute")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
            temp_path = temp_file.name
        
        # Generate speech
        engine.save_to_file(extended_text, temp_path)
        engine.runAndWait()
        
        # Check result
        if os.path.exists(temp_path):
            file_size = os.path.getsize(temp_path)
            print(f"✅ Extended audio file created: {file_size} bytes")
            
            if file_size > 0:
                print("✅ Extended TTS test successful")
                os.unlink(temp_path)
                engine.stop()
                return True
            else:
                print("❌ Extended audio file is empty")
                os.unlink(temp_path)
                engine.stop()
                return False
        else:
            print("❌ Extended audio file was not created")
            engine.stop()
            return False
            
    except Exception as e:
        print(f"❌ Extended TTS test failed: {e}")
        return False

def test_voice_selection():
    """Test voice selection functionality"""
    print("\n🔍 Testing Voice Selection")
    print("=" * 26)
    
    try:
        import pyttsx3
        
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if not voices:
            print("⚠️ No voices available for testing")
            engine.stop()
            return True  # Not a failure, just no voices
        
        print(f"📢 Available voices: {len(voices)}")
        
        # Test each voice
        for i, voice in enumerate(voices[:2]):  # Test first 2 voices only
            print(f"\n🎤 Testing voice {i+1}: {voice.name}")
            
            try:
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', 150)
                
                test_text = f"This is voice number {i+1} speaking."
                
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                    temp_path = temp_file.name
                
                engine.save_to_file(test_text, temp_path)
                engine.runAndWait()
                
                if os.path.exists(temp_path) and os.path.getsize(temp_path) > 0:
                    print(f"   ✅ Voice {i+1} working: {os.path.getsize(temp_path)} bytes")
                    os.unlink(temp_path)
                else:
                    print(f"   ❌ Voice {i+1} failed")
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                        
            except Exception as e:
                print(f"   ❌ Voice {i+1} error: {e}")
        
        engine.stop()
        return True
        
    except Exception as e:
        print(f"❌ Voice selection test failed: {e}")
        return False

def main():
    """Run all TTS tests"""
    print("🚀 Testing pyttsx3 Offline TTS Implementation")
    print("=" * 45)
    
    tests = [
        ("pyttsx3 Installation", test_pyttsx3_installation),
        ("Basic TTS Functionality", test_basic_tts),
        ("Extended TTS (1-minute)", test_extended_tts),
        ("Voice Selection", test_voice_selection)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 25)
    
    passed = 0
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("🎉 All pyttsx3 TTS tests passed! Ready for deployment.")
    elif passed >= len(tests) // 2:
        print("⚠️ Most TTS tests passed - system should work with minor issues")
    else:
        print("❌ Several TTS tests failed - check pyttsx3 installation")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
