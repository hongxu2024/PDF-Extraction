# PDF-Extraction
This project aims at extracting metadata(including date, title, author, summary, keywords) from a specific corpus of academic PDF documents. 
<img src="https://github.com/user-attachments/assets/f1158803-7ed1-46e2-8b06-85af5810285c" width="260px">

output:
<img src="https://github.com/user-attachments/assets/64957101-e95d-4f39-8a8e-66924f56cc02" width="260px">
# How to run it
# run extract_multiply_PDF_for_XML.py
You will get XML files, including layout analysis result.

# run extract_from_Mul_XML.py
You will get a json file, including metadata(date, title, author, summary, keywords).

# run Elasticsearch:
gei into Elasticsearch directory:
start Elasticsearch by using command: bin\elasticsearch.bat
When you start it, you will get authentication information
Retrieve Elasticsearch connection information for authentication, modify app.py file
es = Elasticsearch(
  hosts=[{
  'host': 'localhost',
  'port': 9200,
  'scheme': 'https'
  }],
  Http_auth=('****** ','**************'), # Authentication Information
  verify_certs=False
)

# run app.py

You will get link to Web service, click the link to begin your search!
