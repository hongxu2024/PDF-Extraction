import time
import os
import xml.etree.ElementTree as ET
import re
import json

def contains_keywords(text):
    # 将文本转换为小写以进行不区分大小写的比较
    return "key words" in text.lower()

def process_XML(xml_path):
    file_name = xml_path.split('/')[-1]   #Get the last part of the path
    file_name_without_extension = os.path.splitext(file_name)[0]    #Remove file extension
    # print(file_name_without_extension)
    error_file=""
    data=""
    date=""
    title=""
    author=""
    date_area=0
    if_summary=""
    if_summary_text=0
    summary_text=""
    after_summary=0
    key_word=""
    key_block=0
    
    # Parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Extract bbox information from blocks
    blocks = [child for child in root if child.tag == 'block']
    for index_block, line in enumerate(blocks):
        for index_line,bbox in enumerate(line):
            for font in bbox:
                if(index_block==0):
                    for char in font:
                        if(char.attrib['c']=="(" and date_area==0):
                            date_area=1
                            continue
                        if(date_area==1):
                            date=date+char.attrib['c']
                if(index_block==1):
                    for space_error, char in enumerate(font):
                        if(space_error==0 and title!="" and title[-1].isalpha()):  #If the title is more than one line
                            title=title+" "
                        title=title+char.attrib['c']
                if(font.attrib['name']=="Times-Roman" and float(font.attrib["size"])<=8.1 and index_block==2):
                    for space_error, char in enumerate(font):
                        if(space_error==0 and author!="" and author[-1].isalpha()):  #If the author is more than one line
                            author=author+" "
                        if(author!="" and author[-1]=="(" and char.attrib['c']==")"):
                            author = author[:len(author) - 1]
                            continue
                        author=author+char.attrib['c']
                if(font.attrib['name']=="Times-Bold" and float(font.attrib["size"])<=9.999) and (index_block==3 or index_block==4 or index_block==5):
                    for char in font:
                        if_summary=if_summary+char.attrib['c']
                    if(if_summary=="SUMMARY"):
                        if_summary_text=1
                        continue
                if(font.attrib['name']=="Times-Bold" and float(font.attrib["size"])<=9.1) and (if_summary_text==1):
                    for char in font:
                        summary_text=summary_text+char.attrib['c']
                    key_block=index_block+1
                if(font.attrib['name']=="Times-Roman" and index_block==key_block):
                    if(index_line!=0 and key_word!=""):
                        key_word=key_word+" "
                    for char in font:
                        key_word=key_word+char.attrib['c']
                    
    if(date_area==0):
        error_file=f"{file_name_without_extension}.pdf is a wrong format file"
        return error_file, data 
    date_pattern = re.compile(r'\b[A-Z]+\s\d{4}\b')
    date=date_pattern.search(date).group(0)

    if(title=="Editorial"):
        error_file=f"{file_name_without_extension}.pdf is an Editorial file"
        return error_file, data 
    if(if_summary==""):
        error_file=f"{file_name_without_extension}.pdf does not have summary"
        return error_file, data
    if(key_word=="" or contains_keywords(key_word)==False):
        error_file=f"{file_name_without_extension}.pdf does not have key words"
        return error_file, data

    # 使用正则表达式搜索关键词
    pattern = r'KEY\s+WORDS\s+(.*)'
    match = re.search(pattern, key_word)

    # 匹配到的内容，即 'KEY WORDS' 后面的所有字符
    keywords_str = match.group(1)
    keywords = keywords_str

    print("date:"+date)
    print("title:"+title)
    print("author:"+author)
    print("summary:"+summary_text)
    print("key word:"+keywords)
    
    data = {
        "Date": date,
        "Title": title,
        "Author": author,
        "Keywords": keywords,
        "Summary": summary_text
    }
    return error_file, data

def process_directory(directory_path):
    start_time = time.time()  # 记录开始时间
    results = []
    error_set = []
    total_files_processed = 0  # 处理的文件总数
    error_files_count = 0  # 错误文件数
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.xml'):
            pdf_path = os.path.join(directory_path, filename)
            error_file, data = process_XML(pdf_path)
            if(data != ""):
                results.append(data)
            else:
                error_set.append(error_file)
                error_files_count += 1
            total_files_processed += 1

    # 将信息保存到JSON文件
    with open('use_XML_output.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    with open('error_pdf_output.txt', 'w', encoding='utf-8') as file:
        for item in error_set:
            file.write(item + '\n')

    # 记录结束时间并计算运行时间
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    # 打印统计信息
    print(f"Total XML files processed: {total_files_processed}")
    print(f"Total error files: {error_files_count}")
    print(f"Code runtime: {elapsed_time:.2f} seconds")
    print("Data has been written to use_XML_output.json and error_pdf_output.txt")

# 运行代码
XML_dir = "C:/Users/abc/Desktop/graduate_new/PyMuPDF+Elasticsearch/PDF_FirstPage_XML"
process_directory(XML_dir)
