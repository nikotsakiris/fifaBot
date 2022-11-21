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
 
   return client['Fifa-Scores']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()


#    collection = dbname["Games"]
#    items = collection.find()
#    for item in items:
#     print(int(item["winner_score"]))