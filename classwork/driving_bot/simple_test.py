#!/usr/bin/env python3
"""
Simple test for the validation functionality.
"""

from modules.llm_setup import validate_driving_question

def main():
    print("Testing validation function...")
    
    # Test a relevant question
    question1 = "What is the speed limit in Lithuania?"
    print(f"Testing: {question1}")
    result1 = validate_driving_question(question1)
    print(f"Result: {result1}")
    
    # Test an irrelevant question
    question2 = "How do I cook pasta?"
    print(f"Testing: {question2}")
    result2 = validate_driving_question(question2)
    print(f"Result: {result2}")
    
    print("Test completed!")

if __name__ == "__main__":
    main() 