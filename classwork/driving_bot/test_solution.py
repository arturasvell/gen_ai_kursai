#!/usr/bin/env python3
"""
Comprehensive test script for the driving bot solution.
This script tests the full functionality including validation and querying.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.llm_setup import validate_driving_question, setup_llm
from modules.embedding import embed_driving_rules
from modules.query_system import ask_driving_question

def test_full_solution():
    """Test the complete driving bot solution."""
    
    print("Testing Lithuanian Driving Bot - Full Solution")
    print("=" * 60)
    
    # Test 1: Setup LLM
    print("\n1. Testing LLM Setup...")
    try:
        setup_llm()
        print("   PASS - LLM setup completed")
    except Exception as e:
        print(f"   FAIL - LLM setup failed: {e}")
        return False
    
    # Test 2: Embedding
    print("\n2. Testing Driving Rules Embedding...")
    try:
        client, collection = embed_driving_rules()
        print("   PASS - Driving rules embedded successfully")
        print(f"   Collection name: {collection.name}")
    except Exception as e:
        print(f"   FAIL - Embedding failed: {e}")
        return False
    
    # Test 3: Validation Function
    print("\n3. Testing Question Validation...")
    
    # Test relevant questions
    relevant_questions = [
        "What is the speed limit in urban areas?",
        "Are seatbelts mandatory?",
        "What should I do at a pedestrian crossing?"
    ]
    
    for question in relevant_questions:
        try:
            result = validate_driving_question(question)
            status = "PASS" if result else "FAIL"
            print(f"   {status} - Relevant question: '{question}' -> {result}")
        except Exception as e:
            print(f"   FAIL - Validation error for '{question}': {e}")
    
    # Test irrelevant questions
    irrelevant_questions = [
        "How do I cook pasta?",
        "What's the weather like?",
        "Tell me a joke"
    ]
    
    for question in irrelevant_questions:
        try:
            result = validate_driving_question(question)
            status = "PASS" if not result else "FAIL"
            print(f"   {status} - Irrelevant question: '{question}' -> {result}")
        except Exception as e:
            print(f"   FAIL - Validation error for '{question}': {e}")
    
    # Test 4: Full Query System
    print("\n4. Testing Full Query System...")
    
    test_questions = [
        ("What is the speed limit in urban areas?", True),  # Should be relevant
        ("How do I cook pasta?", False),  # Should be irrelevant
        ("Are seatbelts mandatory?", True),  # Should be relevant
        ("What's the capital of France?", False)  # Should be irrelevant
    ]
    
    for question, should_be_relevant in test_questions:
        try:
            answer = ask_driving_question(question, collection)
            if should_be_relevant:
                if "I'm sorry, but I can only answer questions" in answer:
                    print(f"   FAIL - Relevant question rejected: '{question}'")
                else:
                    print(f"   PASS - Relevant question processed: '{question}'")
            else:
                if "I'm sorry, but I can only answer questions" in answer:
                    print(f"   PASS - Irrelevant question correctly rejected: '{question}'")
                else:
                    print(f"   FAIL - Irrelevant question incorrectly processed: '{question}'")
        except Exception as e:
            print(f"   FAIL - Query error for '{question}': {e}")
    
    print("\n" + "=" * 60)
    print("Full solution test completed!")
    return True

if __name__ == "__main__":
    test_full_solution()
 