# from flask import Flask, render_template, request
# from elasticsearch import Elasticsearch, helpers
# import json

# app = Flask(__name__)

# # 连接到Elasticsearch，添加身份验证
# es = Elasticsearch(
#     hosts=[{
#         'host': 'localhost',
#         'port': 9200,
#         'scheme': 'https'
#     }],
#     http_auth=('elastic', 'E7PgV+sXuSdlgJv+Vcb='),
#     verify_certs=False
# )

# # 定义索引名称
# index_name = 'pdf_documents'

# def import_data():
#     # 读取JSON文件
#     with open('use_XML_output.json', 'r') as json_file:
#         data = json.load(json_file)

#     # 准备数据以进行批量导入
#     actions = [
#         {
#             "_index": index_name,
#             "_source": doc
#         }
#         for doc in data
#     ]

#     # 批量导入数据
#     helpers.bulk(es, actions)
#     print(f"Data has been indexed to Elasticsearch index '{index_name}'")

# @app.route('/', methods=['GET', 'POST'])
# def search():
#     query = None
#     results = None
#     if request.method == 'POST':
#         query = request.form['query']
#         results = es.search(index=index_name, body={
#             "query": {
#                 "multi_match": {
#                     "query": query,
#                     "fields": ["Title^3", "Summary^2", "Keywords", "Author"],
#                     "type": "best_fields"
#                 }
#             }
#         })
#         results = results['hits']['hits']
#     return render_template('index.html', query=query, results=results)

# if __name__ == '__main__':
#     # 删除旧的索引
#     if es.indices.exists(index=index_name):
#         es.indices.delete(index=index_name)
#         print(f"Deleted existing index '{index_name}'")

#     # 创建新的索引并导入数据
#     es.indices.create(index=index_name)
#     import_data()
#     app.run(debug=True)
#     # # 检查是否需要导入数据
#     # if not es.indices.exists(index=index_name):
#     #     es.indices.create(index=index_name)
#     #     import_data()
#     # app.run(debug=True)


from flask import Flask, render_template, request
from elasticsearch import Elasticsearch, helpers
import json

app = Flask(__name__)

# 连接到Elasticsearch，添加身份验证
es = Elasticsearch(
    hosts=[{
        'host': 'localhost',
        'port': 9200,
        'scheme': 'https'
    }],
    http_auth=('elastic', 'E7PgV+sXuSdlgJv+Vcb='),#身份验证信息
    verify_certs=False
)

# 定义索引名称
index_name = 'pdf_documents'

def import_data():
    # 读取JSON文件
    with open('use_XML_output.json', 'r') as json_file:
        data = json.load(json_file)

    # 准备数据以进行批量导入
    actions = [
        {
            "_index": index_name,
            "_source": doc
        }
        for doc in data
    ]

    # 批量导入数据
    helpers.bulk(es, actions)
    print(f"Data has been indexed to Elasticsearch index '{index_name}'")

@app.route('/', methods=['GET', 'POST'])
def search():
    exact_results = None
    fuzzy_results = None
    query = None
    if request.method == 'POST':
        query = request.form['query']
        
        # 精确查询
        exact_results = es.search(index=index_name, body={
            "query": {
                "term": {  # 使用 term 查询进行精确匹配
                    "Title": query
                }
            }
        })
        exact_results = exact_results['hits']['hits']
        
        # 模糊查询
        fuzzy_results = es.search(index=index_name, body={
            "query": {
                "multi_match": {
                    "query": query,
                    "fields": ["Title^3", "Summary^2", "Keywords", "Author"],
                    "fuzziness": "AUTO"
                }
            }
        })
        fuzzy_results = fuzzy_results['hits']['hits']
    
    return render_template('index.html', query=query, exact_results=exact_results, fuzzy_results=fuzzy_results)

if __name__ == '__main__':
    # 删除旧的索引
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)
        print(f"Deleted existing index '{index_name}'")

    # 创建新的索引并导入数据
    es.indices.create(index=index_name)
    import_data()
    app.run(debug=True)
