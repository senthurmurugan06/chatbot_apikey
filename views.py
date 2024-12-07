import openai
from django.shortcuts import render
from .forms import ChatForm
from django.conf import settings
from django.http import JsonResponse
import io
import base64

openai.api_key = settings.OPENAI_API_KEY

def index(request):
    form = ChatForm()
    response_data = None
    
    if request.method == 'POST':
        form = ChatForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            image = request.FILES.get('image')

            if text:
                response_data = get_chatgpt_response(text)
            elif image:
                response_data = analyze_image(image)

    return render(request, 'chatbot/index.html', {'form': form, 'response': response_data})

def get_chatgpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=60
        )
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error in get_chatgpt_response: {e}")
        return None

def convert_image_to_base64(image):
    image_content = image.read()
    return base64.b64encode(image_content).decode('utf-8')

def analyze_image(image):
    base64_image = convert_image_to_base64(image)
    payload = {
        "model": "gpt-4-vision-preview",
        "stream": False,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",  
                        "image_url": f"data:image/png;base64,{base64_image}"
                    }
                ]
            }
        ]
    }

    try:
        response = openai.ChatCompletion.create(**payload)
        return response.choices[0].message['content']
    except Exception as e:
        print(f"Error in analyze_image: {e}")
        return None

