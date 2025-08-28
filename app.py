
##-------- one invoice at a time ----------------##

# from flask import Flask, render_template, request, send_file, flash
# import pytesseract
# import cv2
# import os
# import re
# from werkzeug.utils import secure_filename
# import pandas as pd
# from pdf2image import convert_from_path

# # -------------------- Setup --------------------
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# app = Flask(__name__)
# app.secret_key = "secretkey123"

# UPLOAD_FOLDER = 'static/uploads'
# ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # -------------------- Utils --------------------
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def pdf_to_images(pdf_path):
#     """Convert PDF pages to images"""
#     images = convert_from_path(pdf_path)
#     image_paths = []
#     for i, image in enumerate(images):
#         image_path = f"{pdf_path}_page_{i+1}.png"
#         image.save(image_path, "PNG")
#         image_paths.append(image_path)
#     return image_paths

# # -------------------- OCR & Extraction --------------------
# def extract_fields(image_path):
#     img = cv2.imread(image_path)
#     if img is None:
#         return {}

#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     text = pytesseract.image_to_string(gray)

#     fields = {}

#     # Invoice Number
#     invoice_no = re.search(r"Invoice\s*(?:No\.?|Number)[:\-\s]*([A-Za-z0-9\-]+)", text, re.IGNORECASE)
#     if invoice_no:
#         fields["Invoice Number"] = invoice_no.group(1)

#     # Date
#     date_patterns = [
#         r"(?:Date[:\-\s]*)?([A-Z][a-z]+\.*\s*\d{1,2},\s*\d{4})",
#         r"(\d{1,2}/\d{1,2}/\d{2,4})",
#         r"(\d{4}-\d{1,2}-\d{1,2})"
#     ]
#     for pattern in date_patterns:
#         m = re.search(pattern, text)
#         if m:
#             fields["Date"] = m.group(1)
#             break

#     # Line Items
#     items = []
#     for line in text.splitlines():
#         match = re.search(r"(.*?)(?:\$|₹)\s?([0-9,]+(?:\.\d{2})?)", line)
#         if match:
#             desc = match.group(1).strip()
#             amt = match.group(2).strip()
#             if desc.lower().startswith(("total", "subtotal", "tax", "paid")):
#                 continue
#             if desc and amt:
#                 items.append({"Description": desc, "Amount": amt})
#     fields["Items"] = items

#     # Total


#     return fields

# # -------------------- Save to Excel --------------------
# def save_to_excel(fields, filename="invoice_output.xlsx"):
#     rows = []

#     if "Items" in fields and fields["Items"]:
#         for item in fields["Items"]:
#             rows.append({
#                 "Invoice Number": fields.get("Invoice Number", "Not Found"),
#                 "Date": fields.get("Date", "Not Found"),
#                 "Description": item["Description"],
#                 "Amount": item["Amount"]
#             })
#     else:
#         rows.append({
#             "Invoice Number": fields.get("Invoice Number", "Not Found"),
#             "Date": fields.get("Date", "Not Found"),
#             "Description": "",
#             "Amount": ""
#         })

#     df = pd.DataFrame(rows)

#     # Format Amount and Total
#     df['Amount'] = df['Amount'].apply(lambda x: f"${float(x.replace(',', '')):,.2f}" if str(x).replace(',','').replace('.','').isdigit() else x)
    

#     # Format Date
#     df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%d-%b-%Y')

#     try:
#         if os.path.exists(filename):
#             existing_df = pd.read_excel(filename, engine='openpyxl')
#             df = pd.concat([existing_df, df], ignore_index=True)
#         df.to_excel(filename, index=False, engine='openpyxl')
#         print(f"✅ Saved extracted fields to {filename}")
#     except PermissionError:
#         print("❌ Cannot write to Excel. Close the file and try again.")

# # -------------------- Routes --------------------
# @app.route('/')
# def home():
#     return render_template("index.html")  # Upload form

# @app.route('/upload', methods=['POST'])
# def upload_invoice():
#     if 'invoice' not in request.files:
#         flash("No file part in the request.")
#         return render_template("index.html")

#     file = request.files['invoice']
#     if file.filename == '':
#         flash("No selected file.")
#         return render_template("index.html")

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(path)

#         # If PDF, convert to images
#         if filename.lower().endswith('.pdf'):
#             image_paths = pdf_to_images(path)
#             fields_list = []
#             for img_path in image_paths:
#                 fields_list.append(extract_fields(img_path))
#             # Merge fields (take first invoice number, date, combine items)
#             merged_fields = {"Invoice Number": fields_list[0].get("Invoice Number", ""),
#                              "Date": fields_list[0].get("Date", ""),
#                              "Items": []}
#             for f in fields_list:
#                 merged_fields["Items"].extend(f.get("Items", []))
#             fields = merged_fields
#             display_image = image_paths[0]  
#         else:
#             fields = extract_fields(path)
#             display_image = path

#         save_to_excel(fields)
#         return render_template("result.html", fields=fields, image=display_image)
#     else:
#         flash("File type not allowed. Please upload PNG, JPG, JPEG, or PDF.")
#         return render_template("index.html")

# @app.route('/download-excel')
# def download_excel():
#     path = "invoice_output.xlsx"
#     if os.path.exists(path):
#         return send_file(path, as_attachment=True)
#     else:
#         return "Excel file not found.", 404

# if __name__ == "__main__":
#     app.run(debug=True)




### ------ extracted properly ----------------------

# from flask import Flask, render_template, request, send_file, flash, url_for
# import pytesseract
# import cv2
# import os
# import re
# from werkzeug.utils import secure_filename
# import pandas as pd
# from pdf2image import convert_from_path
# from PIL import Image

# # -------------------- Setup --------------------
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# UPLOAD_FOLDER = "uploads"
# ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

# app = Flask(__name__)
# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# app.secret_key = "secret123"

# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)


# # -------------------- Helpers --------------------
# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# def extract_invoice_date(text):
#     # Pattern for "Invoice Date", "Date of Issue", etc.
#     date_pattern = r"(?:Invoice\s*Date|Date\s*of\s*Issue|Date)[:\s]*([A-Za-z]{3,9}\.? \d{1,2}, ?\d{4})"
#     match = re.search(date_pattern, text, re.I)
#     if match:
#         return match.group(1).strip()

#     # Fallback: first date found in text (likely top of invoice)
#     all_dates = re.findall(r"[A-Za-z]{3,9}\.? \d{1,2}, ?\d{4}", text)
#     return all_dates[0] if all_dates else "Not Found"


# def extract_invoice_data(text):
#     invoices = []
#     invoice_blocks = re.split(r"(?=Invoice\s*Number[:\s]*PO-\d+)", text, flags=re.I)

#     for block in invoice_blocks:
#         block = block.strip()
#         if not block:
#             continue

#         # -------- Invoice Number --------
#         invoice_number_match = re.search(r"(PO-\d+)", block, re.I)
#         if not invoice_number_match:
#             continue
#         invoice_number = invoice_number_match.group(1)

#         # -------- Date --------
#         date_value = "Not Found"
#         for pattern in [
#             r"(?:Invoice\s*Date|Date\s*of\s*Issue|Date)[:\s]*([A-Za-z]{3,9}\.? \d{1,2}, ?\d{4})",
#             r"([A-Za-z]{3,9}\.? \d{1,2}, ?\d{4})"
#         ]:
#             match = re.search(pattern, block, re.I)
#             if match:
#                 date_value = match.group(1)
#                 break

#         # -------- Clean lines & Merge broken lines --------

#         lines = [re.sub(r"\s+", " ", l).strip() for l in block.split("\n") if l.strip()]
#         filtered_lines = []
#         for line in lines:
#     # Remove lines that are clearly non-items or date-related
#                 if re.search(r"(subtotal|total|tax|due|net|term|paid|address|invoice number|page)", line, re.I):
#                     continue
#                 if re.search(r"[A-Za-z]{3,9}\.? \d{1,2}, ?\d{4}", line):  # date-like line
#                     continue
#                 filtered_lines.append(line)

# # Merge lines now without dates
#         merged_lines = []
#         temp = ""
#         for line in filtered_lines:
#             if re.search(r"\$?\d+(?:\.\d{1,2})?$", line):  
#                 if temp:
#                     merged_lines.append(temp + " " + line)
#                     temp = ""
#                 else:
#                     merged_lines.append(line)
#             else:
#                 if temp:
#                     temp += " " + line
#                 else:
#                     temp = line


#         # -------- Extract Items --------
#         items = []
#         item_pattern = re.compile(r"^(.*?)\s+(\$?\d+(?:\.\d{1,2})?)$")
#         for line in merged_lines:
#             m = item_pattern.search(line)
#             if m:
#                 description = m.group(1).strip()
#                 amount = m.group(2).strip()
#                 items.append({"Description": description, "Amount": amount})

#         if items:
#             invoices.append({
#                 "Invoice Number": invoice_number,
#                 "Date": date_value,
#                 "Items": items
#             })

#     return invoices


# def save_to_excel(all_invoices, output_file):
#     rows = []
#     for inv in all_invoices:
#         for item in inv["Items"]:
#             rows.append({
#                 "Invoice Number": inv["Invoice Number"],
#                 "Date": inv["Date"],
#                 "Description": item["Description"],
#                 "Amount": item["Amount"]
#             })
#     df = pd.DataFrame(rows)
#     df.to_excel(output_file, index=False)


# # -------------------- Routes --------------------
# @app.route("/", methods=["GET", "POST"])
# def upload_file():
#     if request.method == "POST":
#         if "files" not in request.files:
#             flash("No files selected")
#             return render_template("index.html")

#         files = request.files.getlist("files")
#         all_invoices = []

#         for file in files:
#             if file.filename == "":
#                 continue
#             if file and allowed_file(file.filename):
#                 filename = secure_filename(file.filename)
#                 filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
#                 file.save(filepath)

#                 extracted_text = ""

#                 if filename.lower().endswith(".pdf"):
#                     pages = convert_from_path(filepath, 300)
#                     for page in pages:
#                         text = pytesseract.image_to_string(page)
#                         extracted_text += text + "\n"
#                 else:
#                     img = cv2.imread(filepath)
#                     text = pytesseract.image_to_string(img)
#                     extracted_text = text
                
#                 invoices = extract_invoice_data(extracted_text)
#                 all_invoices.extend(invoices)

#         # Save Excel
#         output_excel = os.path.join(app.config["UPLOAD_FOLDER"], "all_invoices.xlsx")
#         save_to_excel(all_invoices, output_excel)

#         return render_template("result.html", invoices=all_invoices, excel_file="all_invoices.xlsx")

#     return render_template("index.html")
    

# @app.route("/download/<filename>")
# def download_file(filename):
#     return send_file(os.path.join(app.config["UPLOAD_FOLDER"], filename), as_attachment=True)


# # -------------------- Run --------------------
# if __name__ == "__main__":
#     app.run(debug=True)





## ------- now this code extracted properly ----------##

from flask import Flask, render_template, request, send_file, flash
import pytesseract
import cv2
import os
import re
import numpy as np
from werkzeug.utils import secure_filename
import pandas as pd
from pdf2image import convert_from_path
from PIL import Image

# -------------------- Setup --------------------
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "pdf"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "secret123"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# -------------------- Preprocessing --------------------
def preprocess_image(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    gray = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
    return gray


# -------------------- Helpers --------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def extract_invoice_data(text):
    invoices = []
    blocks = re.split(r"(?=Invoice\s*Number[:\s]*PO-\d+)", text, flags=re.I)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        invoice_number_match = re.search(r"(PO-\d+)", block, re.I)
        if not invoice_number_match:
            continue
        invoice_number = invoice_number_match.group(1)

        date_match = re.search(r"([A-Za-z]{3,9}\.? \d{1,2}, ?\d{4})", block)
        date_value = date_match.group(1) if date_match else "Not Found"

        # Clean lines
        lines = [l.strip() for l in block.split("\n") if l.strip()]
        lines = [re.sub(r"\s+", " ", l) for l in lines]
        filtered = []
        for line in lines:
            # Remove headers and totals
            if re.fullmatch(r"(description\s*amount|description|amount)", line, re.I):
                continue
            if re.search(r"(subtotal|total|tax|due|net|paid|page|invoice number|address)", line, re.I):
                continue
            if re.search(r"[A-Za-z]{3,9}\.? \d{1,2}, ?\d{4}", line):
                continue
            filtered.append(line)

        # Merge multi-line items
        items = []
        temp = ""
        for line in filtered:
            amt_match = re.search(r"(\$?\d+(?:\.\d{1,2})?)$", line)
            if amt_match:
                if temp:
                    items.append({"Description": temp.strip(), "Amount": amt_match.group(1)})
                    temp = ""
                else:
                    parts = re.split(r"(\$?\d+(?:\.\d{1,2})?)$", line)
                    if len(parts) >= 2:
                        items.append({"Description": parts[0].strip(), "Amount": parts[1].strip()})
            else:
                temp += " " + line

        if items:
            invoices.append({
                "Invoice Number": invoice_number,
                "Date": date_value,
                "Items": items
            })

    return invoices

def save_to_excel(all_invoices, output_file):
    rows = []
    for inv in all_invoices:
        for item in inv["Items"]:
            rows.append({
                "Invoice Number": inv["Invoice Number"],
                "Date": inv["Date"],
                "Description": item["Description"],
                "Amount": item["Amount"]
            })
    df = pd.DataFrame(rows)
    df.to_excel(output_file, index=False)


# -------------------- Routes --------------------
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "files" not in request.files:
            flash("No files selected")
            return render_template("index.html")

        files = request.files.getlist("files")
        all_invoices = []

        for file in files:
            if file.filename == "":
                continue
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)

                extracted_text = ""

                if filename.lower().endswith(".pdf"):
                    pages = convert_from_path(filepath, 300)
                    for page in pages:
                        page = page.convert("RGB")
                        img = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
                        processed = preprocess_image(img)
                        text = pytesseract.image_to_string(processed, config="--oem 3 --psm 6")
                        extracted_text += text + "\n"
                else:
                    img = cv2.imread(filepath)
                    processed = preprocess_image(img)
                    extracted_text = pytesseract.image_to_string(processed, config="--oem 3 --psm 6")

                invoices = extract_invoice_data(extracted_text)
                all_invoices.extend(invoices)

        # Save Excel
        output_excel = os.path.join(app.config["UPLOAD_FOLDER"], "all_invoices.xlsx")
        save_to_excel(all_invoices, output_excel)

        return render_template("result.html", invoices=all_invoices, excel_file="all_invoices.xlsx")

    return render_template("index.html")


@app.route("/download/<filename>")
def download_file(filename):
    return send_file(os.path.join(app.config["UPLOAD_FOLDER"], filename), as_attachment=True)


# -------------------- Run --------------------
if __name__ == "__main__":
    app.run(debug=True)

