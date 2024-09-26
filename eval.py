import os
import cv2
import pytesseract
import string
import pandas
import common
import tempfile
import glob
import re
import multiprocessing
import shutil
from pdf2image import convert_from_path


def full_name(excel_data, excel_filename, index):
    first_name = str(excel_data[excel_filename]["NOME"][index]).strip()
    if first_name.isupper():
        first_name = string.capwords(first_name)

    last_name = str(excel_data[excel_filename]["COGNOME"][index]).strip()
    if last_name.isupper():
        last_name = string.capwords(last_name)

    return first_name + " " + last_name


def birth_date(excel_data, excel_filename, index):
    return (
        str(excel_data[excel_filename]["DATA_NASC_1"][index])
        .strip()
        .lower()
        .lstrip("0")
    )


def birth_place(excel_data, excel_filename, index):
    birth_place = str(excel_data[excel_filename]["LUOGO_NASC"][index]).strip()
    if birth_place.isupper():
        birth_place = birth_place.capitalize()

    return birth_place


def course(excel_data, excel_filename, index):
    return (
        str(excel_data[excel_filename]["DESCRIZ"][index])
        .replace("Laurea in", "")
        .replace("Laurea Magistrale in", "")
        .replace("A'", "à")
        .strip()
        .lower()
    )


def read_text(model_name, page, box, padding = 0, perspective = 0, threshold = 0):
    image = page[box[1] : box[1] + box[3], box[0] : box[0] + box[2]]
    image = common.process(
        image, padding=padding, perspective=perspective, threshold=threshold
    )

    data = pytesseract.image_to_data(
        image, lang=model_name, output_type=pytesseract.Output.DICT
    )

    # print([c for c in data["conf"] if c != -1])

    text = pytesseract.image_to_string(image, lang=model_name).strip()

    return data, text


def eval(excel_folder, pdf_folder):

    model_name = "ita_perg_psm13_dual_20000"
    config = (
        # "--psm 13 "
    )

    # x, y, w, h
    full_name_box = (800, 1133, 1898, 134)
    birth_box = (811, 1267, 1874, 73)
    course_box = (782, 1391, 1930, 98)

    progress = 0

    yield 0, "Lettura dei file PDF e dei file Excel in corso...\n\n"

    # Split PDFs
    temp_dir = tempfile.gettempdir()
    temp_images_dir = os.path.join(temp_dir, "PergaTess", "images")

    if not os.path.exists(temp_images_dir):
        os.makedirs(temp_images_dir)

    pdf_files = glob.glob(os.path.join(pdf_folder, '*.pdf'))
    for f in pdf_files:
        filename = os.path.splitext(os.path.basename(f))[0]

        pages = convert_from_path(f, thread_count=multiprocessing.cpu_count())
        for j, page in enumerate(pages):
            page.save(os.path.join(temp_images_dir, f'{filename}_{j}.png'), 'PNG')
            
            yield progress + j * (25 / len(pdf_files)) / len(pages), ""

        progress += 25 / len(pdf_files)

    # Load Excel data
    excel_data = {}
    excel_files = glob.glob(os.path.join(excel_folder, "*.xls*"))
    for i, f in enumerate(excel_files):
        filename = os.path.splitext(os.path.basename(f))[0]
        excel_data[filename] = pandas.read_excel(f)

        yield progress + i * 5 / len(excel_files), ""

    progress += 5

    # Process images
    image_files = os.listdir(temp_images_dir)

    total = len(image_files)
    total_texts = total * 4
    error_count = 0

    yield progress, (
        f"Trovate {total} pergamene.\n\n"
        # f"Rilevamento errori in corso per {total_texts} dati...\n\n"
    )

    for i, f in enumerate(image_files):
        image_filename = os.path.splitext(f)[0]
        excel_filename = image_filename[: image_filename.rindex("_")]
        image_index = int(image_filename[image_filename.rindex("_") + 1 :])

        page = cv2.imread(f"{temp_images_dir}/{f}")

        result = ""
        error_found = False

        try:

            # Name
            _, text = read_text(
                model_name=model_name,
                page=page,
                box=full_name_box,
                padding=10,
                perspective=41,
                threshold=30,
            )
            correct_text = full_name(excel_data, excel_filename, image_index)

            if text != correct_text:
                error_found = True
                result += (
                    f"Nome rilevato: {text}\nNome corretto: {correct_text}\n"
                )

            # Birth
            _, text = read_text(
                model_name=model_name,
                page=page,
                box=birth_box,
                padding=10,
                threshold=200,
            )

            correct_text = birth_date(excel_data, excel_filename, image_index)
            if correct_text not in text:
                error_found = True
                result += f"Data di nascita rilevata: {text[text.rindex('giorno') + 7:]}\nData di nascita corretta: {correct_text}\n"

            correct_text = birth_place(excel_data, excel_filename, image_index)
            if correct_text not in text:
                error_found = True
                match = re.search(r'nat[oa]\s+a\s+([A-Za-z\s]+?)\s*(\(.*?\))?\s+il', text, re.IGNORECASE)
                result += f"Luogo di nascita rilevato: {text if match is None else match.group(1).strip()}\nLuogo di nascita corretto: {correct_text}\n"

            # Course
            _, text = read_text(
                model_name=model_name,
                page=page,
                box=course_box,
                padding=10,
                perspective=25,
                threshold=30,
            )
            text = text.lower()

            correct_text = course(excel_data, excel_filename, image_index)
            if correct_text not in text:
                error_found = True
                result += f"Corso di laurea rilevato: {text}\nCorso di laurea corretto: {correct_text}\n"

            if error_found:
                error_count += 1
                result = f"Errori rilevati nella pergamena numero {image_index + 1} del file \"{excel_filename}\":\n{result}\n"

        except Exception as error:
            print(error)
            result += f'Errore nel processare la pergamena numero {image_index + 1} del file "{excel_filename}".\nÈ necessario controllarla manualmente.\n\n'

        yield progress + i * 70 / total, result

    progress += 70

    shutil.rmtree(temp_images_dir)

    yield progress, f"Trovate {error_count} pergamene sbagliate su {total}!\n\n"
