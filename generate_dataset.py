import os
import shutil
from PIL import Image, ImageDraw, ImageFont
import cv2
import numpy as np
import common

def draw_text_with_custom_font(text, font_path, font_size, padding):
    font = ImageFont.truetype(font_path, font_size)

    temp_image = Image.new('RGB', (1, 1), color=(255, 255, 255))
    draw = ImageDraw.Draw(temp_image)

    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    image_width = text_width + 2 * padding
    image_height = text_height + 2 * padding

    image = Image.new('RGB', (image_width, image_height), color=(255, 255, 255))

    draw = ImageDraw.Draw(image)
    text_x = padding
    text_y = padding
    draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))

    open_cv_image = np.array(image)
    open_cv_image = open_cv_image[:, :, ::-1].copy()  # Convert RGB to BGR

    return open_cv_image


if __name__ == "__main__":

    shutil.rmtree('./data/dataset')
    os.makedirs('./data/dataset')

    i = 0
    total = 20000

    with open("./it.txt") as f:
        for line in f:
            
            if not line.strip() or len(line) > 75:
                continue

            try:
                image = draw_text_with_custom_font(line, './data/fonts/Adobe Garamond Pro Bold Italic.ttf', 110, 10)
                image = common.process(image, perspective=41)

                cv2.imwrite(f'./data/dataset/{i}.png', image)

                with open(f'./data/dataset/{i}.gt.txt', 'w') as f1:
                    f1.write(line)

                i += 1

                image = draw_text_with_custom_font(line, './data/fonts/Linotype Humanistika W01.ttf', 72, 10)
                image = common.process(image, threshold=200)

                cv2.imwrite(f'./data/dataset/{i}.png', image)

                with open(f'./data/dataset/{i}.gt.txt', 'w') as f1:
                    f1.write(line)

                i += 1

                if (i > total):
                    break
            except:
                print('ERROR:', line)

