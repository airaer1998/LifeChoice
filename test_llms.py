import json
import os
import argparse
from typing import Dict, List, Optional
import openai
from anthropic import Anthropic
import google.generativeai as genai

class LLMTester:
    def __init__(self, data_path: str):
        # Load data
        with open(data_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        # Initialize API keys (need to be set when using)
        self.openai_api_key = ""  # GPT-3.5 and GPT-4
        self.anthropic_api_key = ""  # Claude
        self.google_api_key = ""  # Gemini
        
        # Initialize API clients
        if self.openai_api_key:
            openai.api_key = self.openai_api_key
        if self.anthropic_api_key:
            self.anthropic = Anthropic(api_key=self.anthropic_api_key)
        if self.google_api_key:
            genai.configure(api_key=self.google_api_key)

    def create_prompt(self, character_data: Dict) -> str:
        """Create structured prompt"""
        prompt = f"""Please play the role of {character_data['character_name']} based on the Profile and make your life choice under the Scenario regarding Question. Return the option letter (A, B, C, or D) that your character should most appropriately choose in the current scenario. The Profile consists of Description and Memory, where Description is an overall description of the character, and Memory consists of specific events the character has experienced.

# Inputs:
1. Profile:
1.1. Description
{character_data['character_name']}

1.2. Memory
{character_data['input_text']}

2. Scenario:
{character_data['Multiple Choice Question']['Scenario']}

3. Question:
{character_data['Multiple Choice Question']['Question']}

4. Options:
A. {character_data['Multiple Choice Question']['Options'][0]}
B. {character_data['Multiple Choice Question']['Options'][1]}
C. {character_data['Multiple Choice Question']['Options'][2]}
D. {character_data['Multiple Choice Question']['Options'][3]}

# Outputs:
Your choice(A, B, C, or D):"""
        return prompt

    def test_gpt35(self, character_data: Dict) -> Optional[str]:
        """Test GPT-3.5"""
        try:
            if not self.openai_api_key:
                return None
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": self.create_prompt(character_data)}],
                temperature=0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"GPT-3.5 error: {e}")
            return None

    def test_gpt4(self, character_data: Dict) -> Optional[str]:
        """Test GPT-4"""
        try:
            if not self.openai_api_key:
                return None
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": self.create_prompt(character_data)}],
                temperature=0
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"GPT-4 error: {e}")
            return None

    def test_claude(self, character_data: Dict) -> Optional[str]:
        """Test Claude-3"""
        try:
            if not self.anthropic_api_key:
                return None
            
            response = self.anthropic.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{"role": "user", "content": self.create_prompt(character_data)}],
                temperature=0
            )
            return response.content[0].text.strip()
        except Exception as e:
            print(f"Claude error: {e}")
            return None

    def test_gemini(self, character_data: Dict) -> Optional[str]:
        """Test Gemini"""
        try:
            if not self.google_api_key:
                return None
            
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(self.create_prompt(character_data))
            return response.text.strip()
        except Exception as e:
            print(f"Gemini error: {e}")
            return None

    def evaluate_model(self, model_name: str, test_func) -> float:
        """Evaluate model performance"""
        correct = 0
        total = 0
        
        for book_data in self.data:
            for character_data in book_data:
                result = test_func(character_data)
                if result:
                    correct_answer = character_data['Multiple Choice Question']['Correct Answer']
                    if result.upper() == correct_answer:
                        correct += 1
                    total += 1
        
        accuracy = correct / total if total > 0 else 0
        print(f"{model_name} Accuracy: {accuracy:.2%} ({correct}/{total})")
        return accuracy

    def run_selected_tests(self, models: List[str]):
        """Run selected model tests"""
        print("Starting selected model tests...")
        
        model_map = {
            "gpt35": ("GPT-3.5", self.test_gpt35),
            "gpt4": ("GPT-4", self.test_gpt4),
            "claude": ("Claude-3", self.test_claude),
            "gemini": ("Gemini-2", self.test_gemini)
        }
        
        for model in models:
            if model in model_map:
                model_name, test_func = model_map[model]
                self.evaluate_model(model_name, test_func)
            else:
                print(f"Unknown model: {model}")

def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description='Test different LLMs\' role-playing capabilities')
    parser.add_argument('--models', nargs='+', choices=['gpt35', 'gpt4', 'claude', 'gemini'], 
                        default=['gpt35', 'gpt4', 'claude', 'gemini'],
                        help='List of models to test (options: gpt35, gpt4, claude, gemini)')
    
    # Parse command line arguments
    args = parser.parse_args()
    
    # Get current file directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Build data.json path
    data_path = os.path.join(current_dir, 'data', 'data.json')
    
    # Create tester instance and run selected tests
    tester = LLMTester(data_path)
    tester.run_selected_tests(args.models)

if __name__ == "__main__":
    main() 