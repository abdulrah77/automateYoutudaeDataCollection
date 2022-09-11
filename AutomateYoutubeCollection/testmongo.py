from flask import Flask, request, jsonify
import pymongo

app= Flask(__name__)
client = pymongo.MongoClient("mongodb+srv://abdulrah77:mongodb@cluster0.eveyiyi.mongodb.net/?retryWrites=true&w=majority")
db = client['taskdb']
collection = db['taskcollection']

@app.route("/insert/mongo", methods=['POST', 'GET'])
def insert():
    if request.method == 'POST':
        _id= request.json['_id']
        name = request.json['name']
        number = request.json['number']
        collection.insert_one({"_id":_id,"name":name,"number":number})
        return jsonify(str("successfully inserted"))



@app.route("/update/mongo" , methods= ['POST', 'GET'])
def update():
    if request.method=='POST':
         get_name = request.json['get_name']
         collection.find_one_and_update({"name":get_name},{"$inc":{"number":20}})
         return jsonify(str("successfully updated"))


@app.route("/delete/mongo", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        get_name = request.json['get_id']
        collection.delete_one({"_id":get_name})
        return jsonify(str("Successfully Deleted"))


@app.route("/fetch/mongo", methods=['POST', 'GET'])
def fetch():
    data = collection.find()
    return jsonify(str(data))


if __name__=="__main__":
    app.run(port=5002)