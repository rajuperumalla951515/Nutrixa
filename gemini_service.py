import google.generativeai as genai

def get_gemini_response(input_prompt, image_data=None):
    model = genai.GenerativeModel('gemini-2.5-flash')

    content = [input_prompt]

    if image_data:
        content.extend(image_data)

    response = model.generate_content(content)
    return response.text
