# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 12:35:04 2025

@author: Julian
"""

import pandas as pd
import os
import re


# Establecimiento de dirrectorio de trabajo

os.chdir(r'C:\Users\Julian\Desktop\py_environments\ocr_python')
os.getcwd()

os.listdir()

# Normalización del texto

cleaned = []

with open("inventario.txt", "r", encoding="utf-8") as f:
    for line in f:
        l = line.strip().lower()
        
        # reemplaza separadores raros por espacio
        l = re.sub(r"[;,|\-_/]+", " ", l)
        
        # colapsa múltiples espacios en uno
        l = re.sub(r"\s+", " ", l)
        
        cleaned.append(l)

# Guardar archivo limpio
with open("inventario_normalizado.txt", "w", encoding="utf-8") as f:
    for l in cleaned:
        f.write(l + "\n")

# Inventario normalizado 

df = pd.read_csv("inventario_normalizado.txt", header=None, names=["etiqueta"])

df.head()

# Tokenizar

import re

productos = []

with open("inventario_normalizado.txt", encoding="utf-8") as f:
    for linea in f:
        # Línea limpia → tokens
        tokens = re.findall(r"[a-zA-Z0-9\-\"]+", linea.lower())
        productos.append(tokens)


marcas = [
    "apple", "macbook", "imac",
    "dell", "latitude", "inspiron",
    "hp", "lenovo", "ideapad", "thinkpad",
    "asus", "acer", "toshiba", "samsung", "huawei", "lg", "sony",
    "microsoft", "surface"
]


categorias = {
    "motherboard": ["motherboard", "mainboard", "logic board", "board", "motherborad"],
    "keyboard": ["keyboard", "keypad", "palmrest", "backlit", "keybourd", "hitekped"],
    "screen": ["screen", "lcd", "led", "display", "panel"],
    "battery": ["battery", "cell", "powerpack"],
    "cover": ["cover", "case", "housing", "shell", "bezel", "top", "bottom", "i1case"],
    "charger": ["charger", "adapter", "power supply"],
    "speaker": ["speaker", "audio"],
    "camera": ["camera", "webcam"],
    "hinge": ["hinge"],
    "wifi": ["wifi", "wireless card"],
    "trackpad": ["trackpad", "touchpad"],
    "cooling": ["heatsink", "fan", "cooling", "thermal module"]
}


def detectar_marca(tokens):
    for marca in marcas:
        if marca in tokens:
            return marca
    return "unknown"

def detectar_categoria(tokens):
    for categoria, keywords in categorias.items():
        for kw in keywords:
            if kw in tokens:
                return categoria
    return "unknown"


def detectar_modelo(tokens):
    for token in tokens:
        if re.match(r"[a-z0-9]{3,10}", token.lower()):
            return token
    return "unknown"




df = pd.DataFrame({"tokens": productos})

df["brand"] = df["tokens"].apply(detectar_marca)
df["categoria"] = df["tokens"].apply(detectar_categoria)
df["modelo"] = df["tokens"].apply(detectar_modelo)

# df["etiqueta"] = df["tokens"].apply(lambda x: " ".join(x))  # opcional, reconstruye etiqueta


# Revisar qué no se reconoce
unk = df[df["categoria"]=="unknown"]["etiqueta"].head(20)

# Revisar qué marcas hay
df["brand"].value_counts()

# Revisar categorías
df["categoria"].value_counts()


motherboards = df[df["categoria"] == "motherboard"]
