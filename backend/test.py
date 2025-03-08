import requests
import json
import os

# Replace with your actual DeepSeek API key
api_key = "sk-519079ea9b144723a1c62c2bcb98202c"

# Test HTML content - replace with your own clause content for testing
html_content = """
<div>
  <p>The Security Council,</p>
  <p>Recalling its previous resolutions on the situation in the Middle East,</p>
  <p>1. Calls upon all parties to cease hostilities;</p>
  <p>2. Urges the international community to provide humanitarian assistance;</p>
  <p>3. Decides to establish a monitoring mission with the following mandate:</p>
  <p>a) To observe the implementation of the ceasefire;</p>
  <p>b) To facilitate the delivery of humanitarian aid;</p>
  <p>i) Through coordination with local authorities;</p>
  <p>ii) By ensuring safe passage for aid convoys;</p>
  <p>a) To report regularly to the Security Council;</p>
  <p>4. Decides to remain seized of the matter.</p>
</div>
"""

# DeepSeek API endpoint
deepseek_api_url = "https://api.deepseek.com/v1/chat/completions"

# Format the instruction for DeepSeek
instruction = """
Please reformat the following HTML content to use proper clause styling:
- First level: number (1, 2, 3, ...)
- Second level: small letters (a, b, c, ...)
- Third level: small roman numerals (i, ii, iii, ...)
- Fourth level: small letters again (a, b, c, ...)

Maintain all original content and meaning, but structure it properly with the specified formatting.
Return just the formatted HTML that I can directly use, with no explanations or markdown.
"""

# Prepare the request payload
payload = {
    "model": "deepseek-chat",
    "messages": [
        {"role": "system", "content": "You are an assistant that formats document clauses with proper styling."},
        {"role": "user", "content": f"{instruction}\n\n{html_content}"}
    ],
    "stream": True
}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

try:
    # Make the API call with streaming
    print("Sending request to DeepSeek API...")
    response = requests.post(deepseek_api_url, json=payload, headers=headers, stream=True)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        exit(1)
    
    print("Receiving streaming response:")
    formatted_content = ""
    
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8')
            if line_text.startswith('data: '):
                try:
                    json_str = line_text[6:]  # Remove 'data: ' prefix
                    if json_str.strip() == '[DONE]':
                        print("\n[DONE] Stream completed")
                        break
                        
                    data = json.loads(json_str)
                    
                    # Extract the content chunk from the response
                    if 'choices' in data and len(data['choices']) > 0:
                        choice = data['choices'][0]
                        if 'delta' in choice and 'content' in choice['delta']:
                            chunk = choice['delta']['content']
                            formatted_content += chunk
                            print(chunk, end='', flush=True)
                except json.JSONDecodeError as e:
                    print(f"\nJSON parse error: {str(e)}")
    
    print("\n\nFinal formatted content:")
    print(formatted_content)
    
except Exception as e:
    print(f"Error: {str(e)}")