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
        print("Initializing API connection...")  # 表示正在初始化
        # Test if the API is working
        try:
            response = self.client.chat.completions.create(
                model="nvidia/llama-3.1-nemotron-70b-instruct",
                messages=[{"role": "user", "content": "Is the API working?"}],
                temperature=0.5,
                top_p=0.7,
                max_tokens=1024,
                stream=False,
            )

            # # Check if the response is valid
            # if hasattr(response, 'choices') and response.choices:
            #     completion = response.choices[0].message['content']
            #     print("API connection successful! Response:", completion)
            # else:
            #     print("Unexpected response format:", response)

        except Exception as e:
            print("An error occurred when connecting to the API:", str(e))

    def analyze(self, commit_id, record, preliminary_prompt):
        diff_prompt = f"{preliminary_prompt} Commit ID: {str(commit_id)}, Record: {str(record)}"
        print(f"Analyzing commit record for Commit ID: {commit_id}...")  # Print prompt message
        
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
            if chunk.choices[0].delta.content is not None:
                full_reply += chunk.choices[0].delta.content
        
        return full_reply

def analyze_commits(commit_records, args):
    start_time = time.time()  # Record start time
    pre_prompt = "where is a bunch of git diff. you are the absolute expert of the entire project. Please help me analyze it:"
    
    analyzer = OpenAIAnalyzer(args)
    full_reply = "Hello "

    for commit_id, record in commit_records.items():
        full_reply += analyzer.analyze(commit_id, record, pre_prompt)

    print(full_reply)
    end_time = time.time()  # Record end time
    print(f"Analysis completed, took {end_time - start_time:.2f} seconds")  # Print elapsed time
