import pandas as pd
import json

def test_text_parsing():
    print("--- Testing Text Parsing with Separator Detection ---")
    
    test_cases = [
        "Maria Clara | JHS | 6 | 7,8 | No | Mon-Fri | English",
        "John Doe,SHS,8,11,Yes,TTH,Math",
        "Jane Doe\tSHS\t4\t12\tNo\tMon-Fri\tScience"
    ]
    
    for text_data in test_cases:
        lines = [l.strip() for l in text_data.strip().split('\n') if l.strip()]
        if not lines: continue
        
        sample = lines[0]
        separator = '|'
        for s in ['\t', '|', ',', ';']:
            if s in sample:
                separator = s
                break
        
        print(f"Input: {text_data!r}")
        print(f"Detected separator: {separator!r}")
        
        for line in lines:
            parts = [p.strip() for p in line.split(separator)]
            print(f"Parts: {parts}")
        print("-" * 20)

if __name__ == "__main__":
    test_text_parsing()
