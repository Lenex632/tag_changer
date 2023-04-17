import pymongo


def db_connection():
    client = pymongo.MongoClient('localhost', 27017)
    mydb = client['tag_changer']
    collections = {f'{name}_collection': mydb[name] for name in mydb.list_collection_names()}

    return client, mydb, collections


def insert_document(collection, data):
    """
    Function to insert a document into a collection and return the document's id.
    """
    return collection.insert_one(data).inserted_id


def find_document(collection, elements, multiple=False):
    """
    Function to retrieve single or multiple documents from a provided collection using a dictionary containing
    a document's elements.
    """
    if multiple:
        results = collection.find(elements)
        return [r for r in results]
    else:
        return collection.find_one(elements)


def update_document(collection, query_elements, new_values):
    """
    Function to update a single document in a collection.
    """
    collection.update_one(query_elements, {'$set': new_values})


if __name__ == '__main__':
    client, mydb, collections = db_connection()