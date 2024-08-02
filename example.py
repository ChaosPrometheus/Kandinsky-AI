from kandinsky import create_kandinsky_api

def main():
    api = create_kandinsky_api('https://api-key.fusionbrain.ai/', 'YOUR_API_KEY', 'YOUR_SECRET_KEY')
    model_id = api.get_model()
    styles = api.get_styles()
    
    # Пример генерации изображения с использованием стиля "АНИМЭ"
    uuid = api.generate("Пушистый кот в очках", model_id, width=512, height=512, style="АНИМЭ")
    images = api.check_generation(uuid)
    
    if images:
        # Декодирование и сохранение изображения в формате JPG
        api.decode_image(images[0], 'output.jpg')
        print("Изображение сохранено как output.jpg")

if __name__ == '__main__':
    main()
