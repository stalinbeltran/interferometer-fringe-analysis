#python3 imageVerticalCropper.py 0 150 ./videos/fringes_44/framesSoftened/ ./videos/fringes_44/framesLeft/ test

from PIL import Image
import os
import sys
import imageSineFit as isf
import file

x = int(sys.argv[1])
width = int(sys.argv[2])
input_folder = (sys.argv[3])
output_folder = (sys.argv[4])
file.createDirectory(output_folder)

test = False
if len(sys.argv) > 5 and (sys.argv[5].lower() == 'test'): 
    test = True

# Coordenadas del área a recortar
def getVerticalBox(img, x, width):
    w, h = img.size
    return (x, 0, x + width, h)  # Ejemplo: elimina franja central vertical

for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
        path = os.path.join(input_folder, filename)
        img = Image.open(path)
        box = getVerticalBox(img, x, width)
        imgCropped = img.crop(box)
        # new_img = Image.new('RGB', (top.width + bottom.width, img.height))
        # new_img.paste(top, (0, 0))
        # new_img.paste(bottom, (top.width, 0))

        imgCropped.save(os.path.join(output_folder, filename))
        if test:
            break
