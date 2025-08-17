#!/usr/bin/env python3
"""
Test script for IBM Granite models integration in ClauseWise

This script tests the IBM Granite models to ensure they're working correctly
before deploying to the main application.
"""

import requests
import time
import json

# Hugging Face API configuration
HF_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# IBM Granite Model Configuration (Updated with available models)
GRANITE_MODELS = {
    "summarization": "ibm-granite/granite-3.0-8b-instruct",
    "tts": "microsoft/speecht5_tts",  # Keep original TTS as Granite Speech not available
    "chatbot": "ibm-granite/granite-3.0-8b-instruct",
    "detailed_analysis": "ibm-granite/granite-7b-instruct",
    "voice_processing": "microsoft/speecht5_tts"  # Keep original TTS
}

def test_model_availability(model_name, model_id):
    """Test if a model is available on Hugging Face"""
    print(f"\n🔍 Testing {model_name}: {model_id}")
    
    url = f"https://api-inference.huggingface.co/models/{model_id}"
    
    try:
        # Simple test payload
        payload = {"inputs": "This is a test."}
        
        response = requests.post(url, headers=HF_HEADERS, json=payload, timeout=30)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ {model_name} is available and working!")
            return True
        elif response.status_code == 503:
            print(f"   ⏳ {model_name} is loading (this is normal for first use)")
            return True
        elif response.status_code == 404:
            print(f"   ❌ {model_name} not found - may need to check model ID")
            return False
        elif response.status_code == 401:
            print(f"   ❌ Authentication failed for {model_name}")
            return False
        else:
            print(f"   ⚠️ {model_name} returned unexpected status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing {model_name}: {str(e)}")
        return False

def test_summarization_model():
    """Test the IBM Granite summarization model"""
    print(f"\n📝 Testing Summarization with {GRANITE_MODELS['summarization']}")
    
    test_text = """
    This is a sample legal contract between Party A and Party B. 
    The contract outlines the terms and conditions for the provision of services. 
    Party A agrees to provide consulting services to Party B for a period of 12 months. 
    The total compensation shall be $50,000 payable in monthly installments.
    """
    
    prompt = f"Please provide a concise summary of the following legal document:\n\n{test_text}"
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 150,
            "temperature": 0.3,
            "do_sample": True,
            "top_p": 0.9
        }
    }
    
    url = f"https://api-inference.huggingface.co/models/{GRANITE_MODELS['summarization']}"
    
    try:
        response = requests.post(url, headers=HF_HEADERS, json=payload, timeout=45)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                print(f"   ✅ Summary generated successfully!")
                print(f"   📄 Summary: {generated_text[:200]}...")
                return True
        else:
            print(f"   ❌ Summarization test failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Summarization test error: {str(e)}")
    
    return False

def test_chatbot_model():
    """Test the IBM Granite chatbot model"""
    print(f"\n💬 Testing Chatbot with {GRANITE_MODELS['chatbot']}")
    
    context = "This contract is between ABC Corp and XYZ Ltd for software development services worth $100,000."
    question = "What is the value of this contract?"
    
    prompt = f"""You are a legal document assistant. Based on the following document content, please answer the user's question.

Document Content: {context}

User Question: {question}

Answer:"""
    
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 100,
            "temperature": 0.3,
            "do_sample": True
        }
    }
    
    url = f"https://api-inference.huggingface.co/models/{GRANITE_MODELS['chatbot']}"
    
    try:
        response = requests.post(url, headers=HF_HEADERS, json=payload, timeout=45)
        
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                print(f"   ✅ Chatbot response generated successfully!")
                print(f"   💭 Response: {generated_text[:200]}...")
                return True
        else:
            print(f"   ❌ Chatbot test failed: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Chatbot test error: {str(e)}")
    
    return False

def test_api_connection():
    """Test basic API connection with a known working model"""
    print("\n🔧 Testing API Connection")
    print("=" * 25)

    # Test with a simple, known working model
    test_model = "gpt2"
    url = f"https://api-inference.huggingface.co/models/{test_model}"

    try:
        payload = {"inputs": "Hello, this is a test."}
        response = requests.post(url, headers=HF_HEADERS, json=payload, timeout=30)

        print(f"   Testing with {test_model}")
        print(f"   Status Code: {response.status_code}")

        if response.status_code == 200:
            print("   ✅ API connection working!")
            return True
        elif response.status_code == 503:
            print("   ⏳ API working but model loading")
            return True
        elif response.status_code == 401:
            print("   ❌ Authentication failed - check API key")
            return False
        else:
            print(f"   ⚠️ Unexpected response: {response.status_code}")
            return False

    except Exception as e:
        print(f"   ❌ Connection error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing IBM Granite Models for ClauseWise")
    print("=" * 50)

    # First test basic API connection
    api_working = test_api_connection()

    if not api_working:
        print("\n❌ API connection failed. Please check your API key and internet connection.")
        return

    # Test model availability
    results = {}
    for model_name, model_id in GRANITE_MODELS.items():
        results[model_name] = test_model_availability(model_name, model_id)
    
    # Test specific functionality
    print("\n🧪 Testing Model Functionality")
    print("=" * 30)
    
    summarization_works = test_summarization_model()
    chatbot_works = test_chatbot_model()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 25)
    
    for model_name, available in results.items():
        status = "✅ Available" if available else "❌ Not Available"
        print(f"   {model_name}: {status}")
    
    print(f"\n   Summarization Function: {'✅ Working' if summarization_works else '❌ Failed'}")
    print(f"   Chatbot Function: {'✅ Working' if chatbot_works else '❌ Failed'}")
    
    # Overall status
    all_available = all(results.values())
    functions_working = summarization_works and chatbot_works
    
    if all_available and functions_working:
        print(f"\n🎉 All IBM Granite models are ready for ClauseWise!")
    elif all_available:
        print(f"\n⚠️ Models are available but some functions need adjustment")
    else:
        print(f"\n❌ Some models are not available - check model IDs and API access")

if __name__ == "__main__":
    main()
