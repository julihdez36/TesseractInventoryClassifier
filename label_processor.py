import os
from pathlib import Path
import pandas as pd
from tqdm import tqdm
from PIL import Image
import pytesseract
import cv2
import numpy as np

# -------- CONFIGURACIÓN --------

# Ruta al ejecutable de Tesseract en Windows
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Carpeta donde tienes las imágenes:
IMAGES_DIR = Path(r"C:\Users\Julian\Desktop\py_environments\ocr_python\Labels")

# Archivo de salida CSV
OUTPUT_CSV = Path("ocr_inventory.csv")

# Extensiones permitidas
EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"}

# Configuración de Tesseract
TESSERACT_CONFIG = r"--oem 3 --psm 6"
LANG = "spa+eng"

# --------------------------------


def preprocess_image(img_path):
    """Lee imagen con OpenCV, convierte a escala de grises y aplica limpieza para mejorar OCR."""
    img = cv2.imread(str(img_path))

    if img is None:
        raise ValueError(f"No pude abrir la imagen: {img_path}")

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Filtro para reducir ruido
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Binarización adaptativa
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 11
    )

    return thresh


def ocr_file(img_path):
    """Aplica OCR a una imagen con preprocesado."""
    processed = preprocess_image(img_path)

    pil_img = Image.fromarray(processed)

    text = pytesseract.image_to_string(
        pil_img,
        lang=LANG,
        config=TESSERACT_CONFIG
    )

    # Obtener tabla detallada (incluye confianza)
    try:
        df = pytesseract.image_to_data(
            pil_img,
            lang=LANG,
            config=TESSERACT_CONFIG,
            output_type=pytesseract.Output.DATAFRAME
        )
        df = df[df.conf != -1]   # Tesseract usa -1 para elementos no textuales
        avg_conf = df.conf.mean() if not df.empty else None
        n_words = df.shape[0]
    except:
        avg_conf = None
        n_words = None

    # limpiar texto
    clean_text = "\n".join([line.strip() for line in text.splitlines() if line.strip() != ""])

    return clean_text, avg_conf, n_words


def main():
    images = [p for p in IMAGES_DIR.iterdir() if p.suffix.lower() in EXTS]

    if not images:
        print("No se encontraron imágenes en la carpeta.")
        return

    rows = []

    print(f"Procesando {len(images)} imágenes...\n")

    for img_path in tqdm(images):
        try:
            text, avg_conf, n_words = ocr_file(img_path)
        except Exception as e:
            print(f"Error procesando {img_path}: {e}")
            text, avg_conf, n_words = "", None, None

        rows.append({
            "file": img_path.name,
            "text": text,
            "avg_conf": avg_conf,
            "n_words": n_words
        })

    df = pd.DataFrame(rows)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    print("\nOCR completado.")
    print(f"Archivo generado: {OUTPUT_CSV}")
    print("\nPrimeras filas:\n")
    print(df.head().to_string(index=False))


if __name__ == "__main__":
    main()
