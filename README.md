# TesseractInventoryClassifier

# Smart Inventory Classification using OCR and Text Mining

## Project Overview

This project addresses the digitalization and classification of legacy hardware inventory for **Techsavers**, a technical support company located on Adelaide Street, Brisbane. Over several years of operation, a large number of electronic components and spare parts were accumulated and labeled manually using arbitrary textual tags. However, the inventory management process was never digitized, resulting in a lack of structured information about the available stock.

The company required a solution to automatically extract, organize, and classify the information contained in these physical labels in order to build a searchable digital inventory.

![tech_icon](https://github.com/julihdez36/TesseractInventoryClassifier/blob/main/Labels/techsavers.jpg)

## Objective

The objective of this project is to:

1. Digitize product labels using Optical Character Recognition (OCR).
2. Extract textual information from images captured via camera.
3. Apply text mining and machine learning techniques to classify components.
4. Generate a structured and searchable inventory database.

## Methodology and Workflow

### 1. Image Acquisition  
High-resolution images of product labels are captured using a camera under controlled lighting conditions.

![Label example](https://github.com/julihdez36/TesseractInventoryClassifier/blob/main/Labels/IMG_1646.JPG)


### 2. Optical Character Recognition (OCR)  
The [Tesseract OCR engine](https://github.com/tesseract-ocr/tesseract) is used to extract raw text from each label image. Preprocessing steps such as grayscale conversion, noise reduction, and thresholding are applied to improve recognition accuracy.

### 3. Text Cleaning and Normalization  
The extracted text is processed to remove noise, normalize formats, and standardize terminology (e.g., part numbers, brands, component types).

### 4. Text Mining and Feature Extraction  
Natural Language Processing (NLP) techniques are applied to:
- Tokenize descriptions  
- Extract relevant keywords  
- Build numerical representations (TF-IDF / embeddings)

### 5. Inventory Structuring  
The classified results are stored in a structured format (CSV / database), enabling:
- Search by component type  
- Stock aggregation  
- Future integration with inventory management systems

## Data Availability

Sample images of the labels and extracted datasets are provided for reproducibility and further experimentation.  
A public dataset and example images are available at:

[Google Drive link will be placed [here](https://drive.google.com/drive/folders/1iISWzjhfgtsIIDmZ8iNBjKj0G3HUm0zB?usp=drive_link)

