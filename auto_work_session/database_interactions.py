from pymongo import MongoClient
def get_database():

   '''
   MongoDB bot user:
   username: fifaBot
   password: UlG5lHLkhVEhul79
   CONNECTION_STRING: "mongodb+srv://fifaBot:UlG5lHLkhVEhul79@fifa-scores.qdj1pi4.mongodb.net/?retryWrites=true&w=majority"
   ''' 
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://fifaBot:UlG5lHLkhVEhul79@fifa-scores.qdj1pi4.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   return client['Auto-Work-Session']

def reset_brothers():
    pass