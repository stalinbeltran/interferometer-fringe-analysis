#python imageVerticalCentralCropper.py 800  ./originales ./recortadas
from PIL import Image
import os
import sys
import imageSineFit as isf

pixelesXrecortarCentro = int(sys.argv[1])
input_folder = (sys.argv[2])
output_folder = (sys.argv[3])

pixelesXrecortarPorLado = pixelesXrecortarCentro/2 
os.makedirs(output_folder, exist_ok=True)

# Coordenadas del área a recortar (por ejemplo, zona central de 200x200)
def get_crop_box(img):
    w, h = img.size
    return (0, 0, w/2 - pixelesXrecortarPorLado, h), (w/2 + pixelesXrecortarPorLado, 0 , w, h)  # Ejemplo: elimina franja central vertical

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(input_folder, filename)
        img = Image.open(path)
        if isf.isBlackImage(img):
            continue
        # Recortar porciones superior e inferior y unirlas (saltando zona central)
        # top = img.crop((0, 0, img.width, img.height//2 - pixelesXrecortarPorLado))
        # bottom = img.crop((0, img.height//2 + pixelesXrecortarPorLado, img.width, img.height))
        box = get_crop_box(img)
        top = img.crop(box[0])
        bottom = img.crop(box[1])
        new_img = Image.new('RGB', (top.width + bottom.width, img.height))
        new_img.paste(top, (0, 0))
        new_img.paste(bottom, (top.width, 0))

        new_img.save(os.path.join(output_folder, filename))
