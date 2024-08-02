import json
import time
import requests
import base64

class KandinskyAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024, style=None, negative_prompt=None):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": prompt
            }
        }
        
        if style:
            params["style"] = style
        if negative_prompt:
            params["negativePromptUnclip"] = negative_prompt

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def get_styles(self):
        styles = [
            {
                "имя": "КАНДИНСКИЙ",
                "title": "Кандинский",
                "titleEn": "Кандинский",
                "изображение": "https://cdn.fusionbrain.ai/static/download/img-style-kandinsky.png"
            },
            {
                "имя": "UHD",
                "title": "Детальное фото",
                "titleEn": "Детальное фото",
                "изображение": "https://cdn.fusionbrain.ai/static/download/img-style-detail-photo.png"
            },
            {
                "имя": "АНИМЭ",
                "title": "Аниме",
                "titleEn": "Аниме",
                "изображение": "https://cdn.fusionbrain.ai/static/download/img-style-anime.png"
            },
            {
                "имя": "ПО УМОЛЧАНИЮ",
                "title": "Свой стиль",
                "titleEn": "Нет стиль",
                "изображение": "https://cdn.fusionbrain.ai/static/download/img-style-personal.png"
            }
        ]
        return styles

    def decode_image(self, image_data, output_file):
        try:
            image_bytes = base64.b64decode(image_data)
            with open(output_file, 'wb') as file:
                file.write(image_bytes)
        except Exception as e:
            print(f"ошибка {e}")
