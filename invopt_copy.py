import ollama

def test_llama():
    print("Testing LLaMA...")
    response = ollama.chat(model='llama3.1:8b', messages=[{'role': 'user', 'content': 'Hi, can you respond?'}])
    print("Response:", response['message']['content'])

if __name__ == "__main__":
    test_llama()