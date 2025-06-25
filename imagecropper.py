from PIL import Image
import os

input_folder = 'originales'
output_folder = 'recortadas'
os.makedirs(output_folder, exist_ok=True)

recortar = 140
recortarPorLado = recortar/2
# Coordenadas del área a recortar (por ejemplo, zona central de 200px en la vertical)
def get_crop_box(img):
    w, h = img.size
    return (0, 0, w, h//2 - recortarPorLado) + (w, h//2 + recortarPorLado, w, h)  # Ejemplo: elimina franja central vertical

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(input_folder, filename)
        img = Image.open(path)

        # Recortar porciones superior e inferior y unirlas (saltando zona central)
        top = img.crop((0, 0, img.width, img.height//2 - recortarPorLado))
        bottom = img.crop((0, img.height//2 + recortarPorLado, img.width, img.height))
        new_img = Image.new('RGB', (img.width, top.height + bottom.height))
        new_img.paste(top, (0, 0))
        new_img.paste(bottom, (0, top.height))

        new_img.save(os.path.join(output_folder, filename))
        
