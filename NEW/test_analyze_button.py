#!/usr/bin/env python3
"""
Test script to identify the analyze button error

This script simulates the analyze button functionality to identify the exact error.
"""

import sys
import os

# Add the current directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Mock streamlit for testing
class MockStreamlit:
    def __init__(self):
        self.session_state = MockSessionState()
    
    def info(self, msg): print(f"ℹ️ INFO: {msg}")
    def success(self, msg): print(f"✅ SUCCESS: {msg}")
    def warning(self, msg): print(f"⚠️ WARNING: {msg}")
    def error(self, msg): print(f"❌ ERROR: {msg}")
    def spinner(self, msg): return MockSpinner(msg)
    def markdown(self, content, **kwargs): pass
    def columns(self, spec):
        if isinstance(spec, int):
            return [MockColumn() for _ in range(spec)]
        elif isinstance(spec, list):
            return [MockColumn() for _ in range(len(spec))]
        else:
            return [MockColumn(), MockColumn()]
    def expander(self, title, **kwargs): return MockExpander()
    def text_input(self, *args, **kwargs): return ""
    def button(self, *args, **kwargs): return False
    def text_area(self, *args, **kwargs): return ""
    def metric(self, *args, **kwargs): pass
    def plotly_chart(self, *args, **kwargs): pass
    def download_button(self, *args, **kwargs): pass
    def balloons(self): pass

class MockSessionState:
    def __init__(self):
        self.extracted_text = "This is a sample legal contract between Party A and Party B. The contract establishes terms and conditions for services. Payment of $50,000 is due by December 31, 2024. Both parties shall comply with all obligations."
        self.chat_history = []
        self.current_page = "Analysis"
    
    def get(self, key, default=None):
        return getattr(self, key, default)

class MockSpinner:
    def __init__(self, msg):
        print(f"🔄 SPINNER: {msg}")
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

class MockColumn:
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

class MockExpander:
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        pass

def test_analysis_imports():
    """Test importing all required functions"""
    print("🔍 Testing Analysis Page Imports")
    print("=" * 33)
    
    try:
        from utils import (
            generate_summary, generate_detailed_summary, classify_document_type, 
            extract_named_entities, simplify_clauses, extract_key_clauses, 
            chatbot_response, text_to_speech, highlight_entities_in_text, 
            test_tts_connection
        )
        print("✅ All required functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_analysis_functions():
    """Test each analysis function individually"""
    print("\n🔍 Testing Individual Analysis Functions")
    print("=" * 38)
    
    # Mock streamlit
    sys.modules['streamlit'] = MockStreamlit()
    
    try:
        from utils import (
            generate_summary, generate_detailed_summary, classify_document_type, 
            extract_named_entities, simplify_clauses, extract_key_clauses, 
            chatbot_response, text_to_speech, highlight_entities_in_text, 
            test_tts_connection
        )
        
        sample_text = "This is a sample legal contract between Party A and Party B. The contract establishes terms and conditions for services. Payment of $50,000 is due by December 31, 2024."
        
        # Test each function
        functions_to_test = [
            ("generate_summary", lambda: generate_summary(sample_text)),
            ("generate_detailed_summary", lambda: generate_detailed_summary(sample_text)),
            ("classify_document_type", lambda: classify_document_type(sample_text)),
            ("extract_named_entities", lambda: extract_named_entities(sample_text)),
            ("simplify_clauses", lambda: simplify_clauses(sample_text)),
            ("extract_key_clauses", lambda: extract_key_clauses(sample_text)),
            ("chatbot_response", lambda: chatbot_response("What is this contract about?", sample_text)),
            ("test_tts_connection", lambda: test_tts_connection()),
            ("highlight_entities_in_text", lambda: highlight_entities_in_text(sample_text, {}))
        ]
        
        results = {}
        for func_name, func_call in functions_to_test:
            try:
                print(f"Testing {func_name}...")
                result = func_call()
                if result:
                    print(f"✅ {func_name}: Working")
                    results[func_name] = True
                else:
                    print(f"⚠️ {func_name}: Returned None/False")
                    results[func_name] = True  # Still working, just empty result
            except Exception as e:
                print(f"❌ {func_name}: Error - {str(e)}")
                results[func_name] = False
        
        # Test TTS separately (might take longer)
        print("Testing text_to_speech (this may take a moment)...")
        try:
            tts_result = text_to_speech("Short test.")
            if tts_result:
                print("✅ text_to_speech: Working")
                results["text_to_speech"] = True
            else:
                print("⚠️ text_to_speech: No audio generated")
                results["text_to_speech"] = False
        except Exception as e:
            print(f"❌ text_to_speech: Error - {str(e)}")
            results["text_to_speech"] = False
        
        # Summary
        passed = sum(results.values())
        total = len(results)
        print(f"\n📊 Function Test Results: {passed}/{total} passed")
        
        return passed >= total * 0.8  # 80% success rate
        
    except Exception as e:
        print(f"❌ Function testing failed: {e}")
        return False

def test_analysis_page_simulation():
    """Simulate the analysis page loading"""
    print("\n🔍 Testing Analysis Page Simulation")
    print("=" * 35)
    
    # Mock streamlit
    mock_st = MockStreamlit()
    sys.modules['streamlit'] = mock_st
    
    try:
        # Import the analysis page
        from pages import analysis
        
        print("✅ Analysis page imported successfully")
        
        # Try to call the main show function
        print("Testing analysis.show()...")
        analysis.show()
        print("✅ Analysis page show() completed without errors")
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis page simulation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests to identify the analyze button error"""
    print("🚀 Analyzing the 'Analyze Document' Button Error")
    print("=" * 47)
    
    tests = [
        ("Import Test", test_analysis_imports),
        ("Function Test", test_analysis_functions),
        ("Page Simulation", test_analysis_page_simulation)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} crashed: {str(e)}")
            results[test_name] = False
    
    # Final Summary
    print("\n" + "="*50)
    print("📊 ERROR DIAGNOSIS RESULTS")
    print("="*50)
    
    passed = 0
    for test_name, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n🎉 NO ERRORS FOUND! The analyze button should work correctly.")
        print("The issue might be in the Streamlit environment or session state.")
    elif passed >= 2:
        print("\n⚠️ MINOR ISSUES FOUND! Most functionality is working.")
        print("Check the failed tests above for specific issues.")
    else:
        print("\n❌ MAJOR ISSUES FOUND! Multiple components are failing.")
        print("Review the error messages above to fix the issues.")
    
    return passed == len(tests)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
