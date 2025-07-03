#!/usr/bin/env python3
"""
Test script for the driving bot validation functionality.
This script tests whether the validation correctly identifies
questions related to Lithuanian driving rules.
"""

from modules.llm_setup import validate_driving_question

def test_validation():
    """Test the validation function with various types of questions."""
    
    # Relevant questions (should return True)
    relevant_questions = [
        "What is the speed limit in urban areas in Lithuania?",
        "Can I turn right on red light in Lithuania?",
        "What are the requirements for getting a driving license in Lithuania?",
        "What should I do at a pedestrian crossing?",
        "Are seatbelts mandatory in Lithuania?",
        "What are the rules for parking in Vilnius?",
        "How should I behave when emergency vehicles approach?",
        "What are the penalties for drunk driving in Lithuania?",
        "Can cyclists use the road in Lithuania?",
        "What documents do I need to carry while driving?"
    ]
    
    # Irrelevant questions (should return False)
    irrelevant_questions = [
        "How do I cook pasta?",
        "What's the weather like today?",
        "Tell me a joke",
        "What are the rules for driving in Germany?",
        "How do I fix a flat tire?",
        "What's the capital of France?",
        "Can you help me with my math homework?",
        "What's the best restaurant in town?",
        "How do I apply for a job?",
        "What's the latest news?"
    ]
    
    print("Testing Lithuanian Driving Rules Validation")
    print("=" * 50)
    
    print("\nTesting RELEVANT questions (should return True):")
    print("-" * 40)
    for i, question in enumerate(relevant_questions, 1):
        result = validate_driving_question(question)
        status = "PASS" if result else "FAIL"
        print(f"{i:2d}. {status} - {question}")
    
    print("\nTesting IRRELEVANT questions (should return False):")
    print("-" * 40)
    for i, question in enumerate(irrelevant_questions, 1):
        result = validate_driving_question(question)
        status = "PASS" if not result else "FAIL"
        print(f"{i:2d}. {status} - {question}")
    
    print("\nValidation test completed!")

if __name__ == "__main__":
    test_validation() 