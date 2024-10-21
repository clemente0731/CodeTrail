#######################################
###  Integrate LLM AI for analysis ####
#######################################
import os
from openai import OpenAI
import time

class OpenAIAnalyzer:
    def __init__(self, args):
        self.args = args
        self.base_url = args.base_url
        self.api_token = args.api_token
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_token)
        self.api_check()

    def api_check(self):
        print("\033[92mInitializing API connection...\033[0m")  # Indicate that initialization is in progress

        # Define the test message
        test_message = {"role": "user", "content": "Is the API working?"}
        
        # Attempt to connect to the API
        try:
            response = self.client.chat.completions.create(
                model=self.args.model,
                messages=[test_message],
                temperature=0.5,
                top_p=0.7,
                max_tokens=1024,
                stream=False,
            )
            
            # Validate the response
            self._check_response(response)

        except Exception as e:
            print("An error occurred when connecting to the API:", str(e))

    def _check_response(self, response):
        """Check the validity of the API response and print the result."""
        if hasattr(response, 'choices') and response.choices:
            completion = response.choices[0].message.content  # 获取响应内容
            print("\033[94mAPI connection successful! This is the testing response for you:\033[0m", completion)  # 蓝色
        else:
            print("\033[91mUnexpected response format:\033[0m", response)  # 红色


    def analyze(self, commit_id, record, preliminary_prompt):
        diff_prompt = f"{preliminary_prompt} Commit ID: {str(commit_id)}, Record: {str(record)}"
        print(f"\033[33mAnalyzing commit record for Commit ID: {commit_id}...\033[0m")  # Print prompt message in yellow
        
        completion = self.client.chat.completions.create(
            model=self.args.model,
            messages=[{"role": "user", "content": diff_prompt}],
            temperature=0.5,
            top_p=0.7,
            max_tokens=1024,
            stream=True,
        )

        full_reply = ""
        for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
                full_reply += chunk.choices[0].delta.content
        print(full_reply)
        return full_reply

def analyze_commits(commit_records, args):
    start_time = time.time()  # Record start time
    pre_prompt = """
You are an expert in the current project. Please analyze the following Git commit message and Git diff information. Specifically, address the following questions:

1. What are the main modifications made in this commit?
2. What issues might these modifications resolve?
3. Extract key information from the following commit message: , and explain how this message describes the code submission
4. analyze the relationship between the submitted code content and its description. Specifically, which code implements the goals stated in the commit message
5. Evaluate the impact of the following commit on the project:. Which files or functionalities were affected
6. please explain the context and significance of this commit. Did it address any issues or implement new features
7. Do not directly quote large amounts of original input information. You need to explain clearly and can appropriately reference key changes.

Based on the above requirements please provide clear insights in a bullet-point format.    
"""
    
    analyzer = OpenAIAnalyzer(args)
    full_reply = "Hello "

    for commit_id, record in commit_records.items():
        full_reply += analyzer.analyze(commit_id, record, pre_prompt)

    print(full_reply)
    end_time = time.time()  # Record end time
    print(f"Analysis completed, took {end_time - start_time:.2f} seconds")  # Print elapsed time
