from pymongo import MongoClient
def get_db_handle(db_name, host, port, username, password):

 client = MongoClient(host="localhost",
                      port=int("27017"),
                      username="adi",
                      password="adi"
                     )
 db_handle = client['CRM']
 return db_handle, client