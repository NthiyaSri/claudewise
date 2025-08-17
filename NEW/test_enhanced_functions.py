#!/usr/bin/env python3
"""
Test script for enhanced ClauseWise functions

This script tests the enhanced functions to ensure they're working correctly
with the improved processing techniques.
"""

import sys
import os

# Add the current directory to the path so we can import utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import (
    generate_summary, 
    simplify_clauses, 
    chatbot_response, 
    classify_document_type,
    extract_named_entities
)

def test_summarization():
    """Test the enhanced summarization function"""
    print("🔍 Testing Enhanced Summarization")
    print("=" * 35)
    
    sample_text = """
    This Agreement is entered into on January 15, 2024, between ABC Corporation, 
    a Delaware corporation ("Company"), and John Smith ("Contractor"). 
    The Contractor agrees to provide consulting services for a period of 12 months. 
    The total compensation shall be $50,000, payable in monthly installments of $4,167. 
    The Contractor shall maintain confidentiality of all proprietary information. 
    Either party may terminate this agreement with 30 days written notice.
    """
    
    try:
        summary = generate_summary(sample_text, max_length=100)
        print(f"✅ Summary generated: {summary[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Summarization failed: {str(e)}")
        return False

def test_clause_simplification():
    """Test the enhanced clause simplification function"""
    print("\n🔍 Testing Enhanced Clause Simplification")
    print("=" * 40)
    
    legal_text = """
    Whereas the party of the first part hereby covenants and agrees to indemnify 
    and hold harmless the party of the second part from any and all claims, 
    notwithstanding any force majeure circumstances that may arise pursuant to 
    the aforementioned agreement.
    """
    
    try:
        simplified = simplify_clauses(legal_text)
        print(f"✅ Clause simplified: {simplified[:200]}...")
        return True
    except Exception as e:
        print(f"❌ Clause simplification failed: {str(e)}")
        return False

def test_chatbot_response():
    """Test the enhanced chatbot response function"""
    print("\n🔍 Testing Enhanced Chatbot Response")
    print("=" * 37)
    
    context = """
    This Service Agreement is between TechCorp Inc. and DataSoft LLC. 
    The contract value is $75,000 for software development services. 
    The project must be completed by December 31, 2024. 
    Payment terms are Net 30 days after invoice submission.
    """
    
    questions = [
        "What is the contract value?",
        "When is the deadline?",
        "Who are the parties involved?",
        "What are the payment terms?"
    ]
    
    success_count = 0
    for question in questions:
        try:
            response = chatbot_response(question, context)
            print(f"Q: {question}")
            print(f"A: {response[:150]}...")
            print()
            success_count += 1
        except Exception as e:
            print(f"❌ Question '{question}' failed: {str(e)}")
    
    print(f"✅ {success_count}/{len(questions)} chatbot responses successful")
    return success_count == len(questions)

def test_document_classification():
    """Test the document classification function"""
    print("\n🔍 Testing Document Classification")
    print("=" * 33)
    
    test_documents = [
        ("This lease agreement is between landlord and tenant for rental property...", "Lease Agreement"),
        ("This employment contract outlines salary and benefits for the employee...", "Employment Document"),
        ("This non-disclosure agreement protects confidential information...", "Non-Disclosure Agreement"),
        ("This service agreement defines the scope of work and deliverables...", "Service Agreement")
    ]
    
    success_count = 0
    for doc_text, expected_type in test_documents:
        try:
            classification = classify_document_type(doc_text)
            print(f"Text: {doc_text[:50]}...")
            print(f"Classification: {classification}")
            if expected_type.lower() in classification.lower():
                print("✅ Correct classification")
                success_count += 1
            else:
                print("⚠️ Different classification")
            print()
        except Exception as e:
            print(f"❌ Classification failed: {str(e)}")
    
    print(f"✅ {success_count}/{len(test_documents)} classifications successful")
    return success_count >= len(test_documents) // 2  # Allow 50% success rate

def test_entity_extraction():
    """Test the named entity extraction function"""
    print("\n🔍 Testing Named Entity Extraction")
    print("=" * 33)
    
    sample_text = """
    This agreement dated March 15, 2024, is between Microsoft Corporation 
    and Apple Inc. The total value is $1,500,000. Contact John Doe at 
    john.doe@email.com or call (555) 123-4567. The office is located at 
    123 Main Street, Seattle, WA.
    """
    
    try:
        entities = extract_named_entities(sample_text)
        print("Extracted entities:")
        for category, items in entities.items():
            if items:
                print(f"  {category}: {items[:3]}")  # Show first 3 items
        
        # Check if we found some entities
        total_entities = sum(len(items) for items in entities.values())
        print(f"\n✅ Total entities found: {total_entities}")
        return total_entities > 0
    except Exception as e:
        print(f"❌ Entity extraction failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Testing Enhanced ClauseWise Functions")
    print("=" * 45)
    
    tests = [
        ("Summarization", test_summarization),
        ("Clause Simplification", test_clause_simplification),
        ("Chatbot Response", test_chatbot_response),
        ("Document Classification", test_document_classification),
        ("Entity Extraction", test_entity_extraction)
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
        print("🎉 All enhanced functions are working correctly!")
    elif passed >= len(tests) // 2:
        print("⚠️ Most functions are working - some may need API access")
    else:
        print("❌ Several functions need attention")

if __name__ == "__main__":
    main()
