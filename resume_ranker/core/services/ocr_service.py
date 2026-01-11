import os
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import fitz  # PyMuPDF
from pdf2image import convert_from_path


# --------------------------------------------------
# Configure Tesseract path (Windows)
# --------------------------------------------------
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

# --------------------------------------------------
# Tesseract OCR configuration
# --------------------------------------------------
TESSERACT_CONFIG = r"--oem 3 --psm 6"


# --------------------------------------------------
# IMAGE PREPROCESSING (KEY FOR ACCURACY)
# --------------------------------------------------
def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Improve image quality before OCR:
    - Convert to grayscale
    - Increase contrast
    - Sharpen
    """

    # Convert to grayscale
    image = image.convert("L")

    # Increase contrast
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)

    # Sharpen image
    image = image.filter(ImageFilter.SHARPEN)

    return image


# --------------------------------------------------
# OCR FOR IMAGE FILES
# --------------------------------------------------
def extract_text_from_image(image_path: str) -> str:
    try:
        image = Image.open(image_path)
        image = preprocess_image(image)
        text = pytesseract.image_to_string(
            image,
            config=TESSERACT_CONFIG
        )
        return text
    except Exception as e:
        print(f"OCR image error ({image_path}):", e)
        return ""


# --------------------------------------------------
# OCR FOR PDF FILES
# --------------------------------------------------
def extract_text_from_pdf(pdf_path: str) -> str:
    extracted_text = ""

    try:
        # -----------------------------
        # 1. Try direct text extraction
        # -----------------------------
        doc = fitz.open(pdf_path)
        for page in doc:
            extracted_text += page.get_text()

        # If sufficient text found, return
        if len(extracted_text.strip()) > 200:
            return extracted_text

        # -----------------------------
        # 2. OCR fallback (scanned PDF)
        # -----------------------------
        images = convert_from_path(
            pdf_path,
            dpi=300,          # Higher DPI = better OCR
            fmt="png"
        )

        for img in images:
            img = preprocess_image(img)
            extracted_text += pytesseract.image_to_string(
                img,
                config=TESSERACT_CONFIG
            )

        return extracted_text

    except Exception as e:
        print(f"OCR PDF error ({pdf_path}):", e)
        return ""


# --------------------------------------------------
# MAIN ENTRY FUNCTION
# --------------------------------------------------
def extract_text_from_file(file_path: str) -> str:
    """
    Extract text from resume files (PDF / Image).
    Automatically selects best method.
    """

    if not file_path or not os.path.exists(file_path):
        return ""

    ext = os.path.splitext(file_path)[1].lower()

    if ext in [".jpg", ".jpeg", ".png"]:
        return extract_text_from_image(file_path)

    if ext == ".pdf":
        return extract_text_from_pdf(file_path)

    return ""
