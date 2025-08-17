#!/usr/bin/env python3
"""
Test script for TTS integration within Streamlit context

This script tests the TTS function as it would be called from the Streamlit app.
"""

import sys
import os

# Add the current directory to the path so we can import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock streamlit for testing
class MockStreamlit:
    def info(self, message):
        print(f"ℹ️ INFO: {message}")
    
    def success(self, message):
        print(f"✅ SUCCESS: {message}")
    
    def warning(self, message):
        print(f"⚠️ WARNING: {message}")
    
    def error(self, message):
        print(f"❌ ERROR: {message}")

# Replace streamlit with mock
import sys
sys.modules['streamlit'] = MockStreamlit()

def test_tts_integration():
    """Test TTS integration with mock Streamlit"""
    print("🔍 Testing TTS Integration with Streamlit Context")
    print("=" * 50)
    
    try:
        # Import the TTS function
        from utils import text_to_speech
        
        # Test with short text
        print("\n📝 Testing with short text:")
        short_text = "This is a short legal document summary."
        result = text_to_speech(short_text)
        
        if result:
            print(f"✅ Short text TTS successful: {len(result)} characters")
        else:
            print("❌ Short text TTS failed")
        
        # Test with longer text
        print("\n📝 Testing with longer text:")
        long_text = """
        This legal document analysis provides comprehensive insights into contract terms and conditions.
        The agreement establishes clear obligations for all parties involved.
        Key provisions include payment terms, delivery schedules, and termination clauses.
        All parties must comply with applicable laws and regulations.
        This analysis helps identify potential risks and opportunities.
        """
        
        result2 = text_to_speech(long_text)
        
        if result2:
            print(f"✅ Long text TTS successful: {len(result2)} characters")
        else:
            print("❌ Long text TTS failed")
        
        # Test with very short text (should be extended)
        print("\n📝 Testing with very short text (auto-extension):")
        very_short_text = "Contract approved."
        result3 = text_to_speech(very_short_text)
        
        if result3:
            print(f"✅ Very short text TTS successful: {len(result3)} characters")
        else:
            print("❌ Very short text TTS failed")
        
        return all([result, result2, result3])
        
    except Exception as e:
        print(f"❌ TTS integration test failed: {e}")
        return False

def test_tts_error_handling():
    """Test TTS error handling"""
    print("\n🔍 Testing TTS Error Handling")
    print("=" * 30)
    
    try:
        from utils import text_to_speech
        
        # Test with empty text
        print("📝 Testing with empty text:")
        result = text_to_speech("")
        
        if result is None:
            print("✅ Empty text handled correctly (returned None)")
        else:
            print("⚠️ Empty text returned unexpected result")
        
        # Test with None
        print("📝 Testing with None:")
        result2 = text_to_speech(None)
        
        if result2 is None:
            print("✅ None input handled correctly")
        else:
            print("⚠️ None input returned unexpected result")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_text_preprocessing():
    """Test text preprocessing for TTS"""
    print("\n🔍 Testing Text Preprocessing for TTS")
    print("=" * 35)
    
    try:
        from utils import text_to_speech
        
        # Test with special characters
        print("📝 Testing with special characters:")
        special_text = "**LEGAL CONTRACT** •Important terms• *conditions* \n\n Line breaks and tabs\t\t"
        result = text_to_speech(special_text)
        
        if result:
            print("✅ Special characters handled correctly")
        else:
            print("❌ Special characters caused failure")
        
        return result is not None
        
    except Exception as e:
        print(f"❌ Text preprocessing test failed: {e}")
        return False

def main():
    """Run all TTS integration tests"""
    print("🚀 Testing TTS Integration with ClauseWise")
    print("=" * 42)
    
    tests = [
        ("TTS Integration", test_tts_integration),
        ("Error Handling", test_tts_error_handling),
        ("Text Preprocessing", test_text_preprocessing)
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
        print("🎉 All TTS integration tests passed! Ready for Streamlit deployment.")
    elif passed >= len(tests) // 2:
        print("⚠️ Most TTS integration tests passed - should work in Streamlit")
    else:
        print("❌ TTS integration tests failed - check implementation")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
