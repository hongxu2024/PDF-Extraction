import time
import fitz  # PyMuPDF
import os
import re

def clean_invalid_xml_chars(xml_data):
    # 使用正则表达式移除所有&#xf;等无效字符引用
    ##Remove all&# xf; using regular expressions; Wait for invalid character references
    return re.sub(r'&#\w+;', '', xml_data)

def process_directory(directory_PDF_path, output_dir):
    pdf_count = 0  # 初始化计数器
    for filename in os.listdir(directory_PDF_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(directory_PDF_path, filename)
            extract_xml_from_pdf(pdf_path, output_dir)
            pdf_count += 1  # 每处理一个PDF文件，计数器加1
    print(f"Total PDF files processed: {pdf_count}")  # 输出处理的PDF文件总数

def extract_xml_from_pdf(pdf_path, output_dir):
    # open pdf file
    doc = fitz.open(pdf_path)
    file_name = pdf_path.split('/')[-1]   # Get the last part of the path
    file_name_without_extension = os.path.splitext(file_name)[0]    # Remove file extension
    # 遍历第一页
    # Traverse the first page
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # print(f"Extracting XML content from Page {page_num + 1}...")
        
        # extract pdf to XML format
        xml_content = page.get_text("xml")
        cleaned_xml_data = clean_invalid_xml_chars(xml_content)
        # Generate a path to save the XML file
        output_path = f"{output_dir}/{file_name_without_extension}.xml"
        
        # Save XML content to a file
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(cleaned_xml_data)
        
        print(f"{file_name_without_extension} XML content saved to {output_path}")
        break

# start time
start_time = time.time()

# run the code
pdf_dir = "C:/Users/abc/Desktop/hongxu/"  # PDF directory
output_dir = "C:/Users/abc/Desktop/graduate_new/PyMuPDF+Elasticsearch/PDF_FirstPage_XML"  # Directory for saving XML files
process_directory(pdf_dir, output_dir)

# record end time
end_time = time.time()

# display running time
elapsed_time = end_time - start_time
print(f"Code runtime: {elapsed_time:.2f} seconds")
