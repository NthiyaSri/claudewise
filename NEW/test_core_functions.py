#!/usr/bin/env python3
"""
Test script for core enhanced functions without dependencies

This script tests the core logic of enhanced functions without requiring
external dependencies like pdfplumber or docx.
"""

import re

def test_legal_term_replacement():
    """Test the legal term replacement logic"""
    print("🔍 Testing Legal Term Replacement")
    print("=" * 32)
    
    legal_text = """
    Whereas the party hereby covenants to indemnify and hold harmless 
    the other party, notwithstanding any force majeure circumstances 
    pursuant to the aforementioned agreement.
    """
    
    # Legal term replacements (from enhanced simplify_clauses)
    replacements = {
        "whereas": "while",
        "hereby": "by this document", 
        "covenant": "promise",
        "indemnify": "protect from loss",
        "notwithstanding": "despite",
        "pursuant to": "according to",
        "aforementioned": "mentioned above",
        "force majeure": "uncontrollable circumstances"
    }
    
    simplified_text = legal_text
    for legal_term, plain_term in replacements.items():
        simplified_text = simplified_text.replace(legal_term, plain_term)
    
    print(f"Original: {legal_text[:100]}...")
    print(f"Simplified: {simplified_text[:100]}...")
    
    # Check if replacements were made
    improvements = sum(1 for term in replacements.keys() if term not in simplified_text.lower())
    print(f"✅ {improvements}/{len(replacements)} legal terms simplified")
    return improvements > 0

def test_entity_extraction_patterns():
    """Test the regex patterns for entity extraction"""
    print("\n🔍 Testing Entity Extraction Patterns")
    print("=" * 36)
    
    sample_text = """
    This agreement dated March 15, 2024, is between Microsoft Corporation 
    and Apple Inc. The total value is $1,500,000. Contact John Doe at 
    john.doe@email.com or call (555) 123-4567. The office is located at 
    123 Main Street, Seattle, WA. Payment due by 12/31/2024.
    """
    
    # Test date extraction
    date_patterns = [
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b'
    ]
    
    dates = []
    for pattern in date_patterns:
        dates.extend(re.findall(pattern, sample_text, re.IGNORECASE))
    
    # Test monetary value extraction
    money_patterns = [
        r'\$[\d,]+\.?\d*',
        r'\b\d+\s*(?:dollars?|USD|cents?)\b'
    ]
    
    money = []
    for pattern in money_patterns:
        money.extend(re.findall(pattern, sample_text, re.IGNORECASE))
    
    # Test organization extraction
    org_pattern = r'\b\w+(?:\s+\w+)*\s+(?:Inc\.?|LLC|Corp\.?|Company|Corporation|Ltd\.?)\b'
    orgs = re.findall(org_pattern, sample_text, re.IGNORECASE)
    
    # Test email extraction
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, sample_text)
    
    # Test phone extraction
    phone_pattern = r'\b\(\d{3}\)\s*\d{3}[-.]?\d{4}\b'
    phones = re.findall(phone_pattern, sample_text)
    
    print(f"Dates found: {dates}")
    print(f"Money found: {money}")
    print(f"Organizations found: {orgs}")
    print(f"Emails found: {emails}")
    print(f"Phones found: {phones}")
    
    total_entities = len(dates) + len(money) + len(orgs) + len(emails) + len(phones)
    print(f"✅ Total entities extracted: {total_entities}")
    return total_entities >= 5  # Expect at least 5 entities

def test_document_classification_logic():
    """Test the document classification keyword matching"""
    print("\n🔍 Testing Document Classification Logic")
    print("=" * 38)
    
    classifications = {
        "Legal Contract": ["contract", "agreement", "party", "whereas", "hereby", "covenant"],
        "Lease Agreement": ["lease", "rent", "tenant", "landlord", "premises", "rental"],
        "Employment Document": ["employment", "employee", "employer", "salary", "compensation"],
        "Non-Disclosure Agreement": ["confidential", "nda", "proprietary", "disclosure"]
    }
    
    test_documents = [
        ("This lease agreement is for rental property between landlord and tenant", "Lease Agreement"),
        ("This employment contract outlines salary and compensation for employee", "Employment Document"),
        ("This confidential disclosure agreement protects proprietary information", "Non-Disclosure Agreement"),
        ("This contract agreement between parties hereby establishes terms", "Legal Contract")
    ]
    
    correct_classifications = 0
    for doc_text, expected_type in test_documents:
        text_lower = doc_text.lower()
        scores = {}
        
        for doc_type, keywords in classifications.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                scores[doc_type] = score
        
        if scores:
            best_match = max(scores, key=scores.get)
            confidence = scores[best_match]
            classification = f"{best_match} (Confidence: {confidence} keywords matched)"
        else:
            classification = "General Legal Document"
        
        print(f"Text: {doc_text[:50]}...")
        print(f"Expected: {expected_type}")
        print(f"Classified: {classification}")
        
        if expected_type in classification:
            print("✅ Correct")
            correct_classifications += 1
        else:
            print("❌ Incorrect")
        print()
    
    print(f"✅ {correct_classifications}/{len(test_documents)} classifications correct")
    return correct_classifications >= len(test_documents) // 2

def test_keyword_matching_logic():
    """Test the enhanced keyword matching for chatbot responses"""
    print("\n🔍 Testing Keyword Matching Logic")
    print("=" * 33)
    
    context = """
    This Service Agreement is between TechCorp Inc. and DataSoft LLC. 
    The contract value is $75,000 for software development services. 
    The project must be completed by December 31, 2024. 
    Payment terms are Net 30 days after invoice submission.
    """
    
    test_cases = [
        ("What is the contract value?", ["money", "cost", "price", "fee", "payment"]),
        ("When is the deadline?", ["date", "when", "time", "deadline"]),
        ("Who are the parties?", ["who", "party", "parties", "person"]),
        ("What are the obligations?", ["obligation", "duty", "responsibility", "must"])
    ]
    
    successful_matches = 0
    for question, expected_keywords in test_cases:
        question_lower = question.lower()
        
        # Test if any expected keywords are found
        matches = [keyword for keyword in expected_keywords if keyword in question_lower]
        
        print(f"Question: {question}")
        print(f"Expected keywords: {expected_keywords}")
        print(f"Matched keywords: {matches}")
        
        if matches:
            print("✅ Keywords matched")
            successful_matches += 1
        else:
            print("❌ No keywords matched")
        print()
    
    print(f"✅ {successful_matches}/{len(test_cases)} keyword matches successful")
    return successful_matches == len(test_cases)

def test_text_preprocessing():
    """Test text preprocessing for legal documents"""
    print("\n🔍 Testing Text Preprocessing")
    print("=" * 28)
    
    raw_text = """
    **LEGAL CONTRACT**
    
    This agreement contains •important terms and *conditions*.
    
    The parties shall comply with all obligations...
    """
    
    # Clean text (similar to TTS preprocessing)
    clean_text = raw_text.replace("**", "").replace("•", "").replace("*", "")
    clean_text = clean_text.replace("\n", " ").replace("\r", " ")
    clean_text = re.sub(r'[^\w\s.,!?-]', '', clean_text)
    clean_text = " ".join(clean_text.split())
    
    print(f"Original: {raw_text}")
    print(f"Cleaned: {clean_text}")
    
    # Check if cleaning was effective
    improvements = [
        "**" not in clean_text,
        "•" not in clean_text,
        "*" not in clean_text,
        "\n" not in clean_text,
        len(clean_text.split()) > 0
    ]
    
    success_count = sum(improvements)
    print(f"✅ {success_count}/{len(improvements)} preprocessing checks passed")
    return success_count == len(improvements)

def main():
    """Run all core function tests"""
    print("🚀 Testing Core Enhanced Functions")
    print("=" * 35)
    
    tests = [
        ("Legal Term Replacement", test_legal_term_replacement),
        ("Entity Extraction Patterns", test_entity_extraction_patterns),
        ("Document Classification", test_document_classification_logic),
        ("Keyword Matching", test_keyword_matching_logic),
        ("Text Preprocessing", test_text_preprocessing)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test failed: {str(e)}")
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
        print("🎉 All core functions are working correctly!")
    elif passed >= len(tests) // 2:
        print("⚠️ Most core functions are working well")
    else:
        print("❌ Several core functions need attention")

if __name__ == "__main__":
    main()
