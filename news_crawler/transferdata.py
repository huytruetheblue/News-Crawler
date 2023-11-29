from pymongo import MongoClient
from pymongo.server_api import ServerApi
from elasticsearch import Elasticsearch


uri = "mongodb+srv://huytrue02:huytrue2002@cluster0.bxyokxl.mongodb.net/?retryWrites=true&w=majority"

mongo_client = MongoClient(uri, server_api=ServerApi('1'))
mongo_db = mongo_client['news-data']
mongo_collection = mongo_db['news']

es = Elasticsearch(['http://elastic:znfDJQK0Mb*XrYDDEFKg@localhost:9200'])

# Truy xuất dữ liệu từ MongoDB
mongo_data = mongo_collection.find()

# Chuyển đổi và lưu trữ dữ liệu vào Elasticsearch
for document in mongo_data:
    # Chuyển đổi dữ liệu từ MongoDB sang định dạng tương thích với Elasticsearch
    elastic_data = {
        'index': 'search-football_news',
        'id': document['_id'],  # Trường _id của MongoDB sẽ là _id của Elasticsearch
        'body': {
            'title': document['title'],  # Thay 'field1' bằng tên trường thích hợp trong MongoDB
            'content': document['content'],  # Thay 'field2' bằng tên trường thích hợp trong MongoDB
            "url": document['url'],
        }
    }

    # Lưu trữ dữ liệu vào Elasticsearch
    es.index(**elastic_data)
    
    # Đóng kết nối với MongoDB
mongo_client.close()

# Đóng kết nối với Elasticsearch
es.transport.close()