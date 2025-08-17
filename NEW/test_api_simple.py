#!/usr/bin/env python3
"""
Simple API test to check Hugging Face connection
"""

import requests
import json

# API configuration
HF_API_KEY = "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"
HF_HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

def test_simple_api():
    """Test with a very basic model"""
    print("Testing Hugging Face API connection...")
    
    # Try the simplest possible request
    url = "https://api-inference.huggingface.co/models/gpt2"
    payload = {"inputs": "The quick brown fox"}
    
    try:
        print(f"Making request to: {url}")
        print(f"Headers: {HF_HEADERS}")
        print(f"Payload: {payload}")
        
        response = requests.post(url, headers=HF_HEADERS, json=payload, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Content Length: {len(response.content)}")
        
        if response.text:
            print(f"Response Text (first 500 chars): {response.text[:500]}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"JSON Response: {result}")
                return True
            except:
                print("Response is not valid JSON")
                return False
        else:
            print(f"Request failed with status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        return False

def test_without_auth():
    """Test without authentication"""
    print("\nTesting without authentication...")
    
    url = "https://api-inference.huggingface.co/models/gpt2"
    payload = {"inputs": "The quick brown fox"}
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        
        print(f"Status Code (no auth): {response.status_code}")
        print(f"Response Text (first 200 chars): {response.text[:200]}")
        
        return response.status_code in [200, 503]  # 503 means model loading
        
    except Exception as e:
        print(f"Exception (no auth): {str(e)}")
        return False

def test_granite_model():
    """Test IBM Granite model specifically"""
    print("\nTesting IBM Granite model...")
    
    url = "https://api-inference.huggingface.co/models/ibm-granite/granite-3.0-8b-instruct"
    payload = {"inputs": "Hello, how are you?"}
    
    try:
        response = requests.post(url, headers=HF_HEADERS, json=payload, timeout=30)
        
        print(f"Granite Status Code: {response.status_code}")
        print(f"Granite Response Text (first 200 chars): {response.text[:200]}")
        
        return response.status_code in [200, 503]
        
    except Exception as e:
        print(f"Granite Exception: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔍 Simple API Connection Test")
    print("=" * 30)
    
    # Test basic API
    basic_works = test_simple_api()
    
    # Test without auth
    no_auth_works = test_without_auth()
    
    # Test Granite model
    granite_works = test_granite_model()
    
    print("\n📊 Results:")
    print(f"Basic API (with auth): {'✅' if basic_works else '❌'}")
    print(f"API without auth: {'✅' if no_auth_works else '❌'}")
    print(f"IBM Granite model: {'✅' if granite_works else '❌'}")
    
    if basic_works or no_auth_works:
        print("\n✅ API connection is working!")
    else:
        print("\n❌ API connection failed - check network and API key")
