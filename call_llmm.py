import google.generativeai as genai
import base64
from generate_prompt import build_system_message
genai.configure(api_key='AIzaSyAM6HAe_3pDw8ZrZpa0Y_5LPQKcRv3r8VA')
model = genai.GenerativeModel(model_name='gemini-2.0-flash')

def call_llm(user_query: str):
    full_query, image_paths = build_system_message(user_query)
    
    mime_array = []
    for image_path in image_paths:
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        encoded_image = base64.b64encode(image_bytes).decode('utf-8')
        mime_array.append({'mime_type': 'image/png', 'data': encoded_image})
    mime_array.append(full_query)
    response = model.generate_content(mime_array)
    print('model response', response.candidates)
    full_text = ''
    for i in response.candidates:
        for j in i.content.parts:
            full_text += f"{j.text} \n"
    # all_text = "\n".join(candidate.text for candidate in response.candidates)
    print('full text', full_text)
    return full_text