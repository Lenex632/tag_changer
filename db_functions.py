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


def find_document(collection, *elements, multiple=False):
    """
    Function to retrieve single or multiple documents from a provided collection using a dictionary containing
    a document's elements.
    """
    if multiple:
        results = collection.find(*elements)
        return [r for r in results]
    else:
        return collection.find_one(*elements)


def delete_document(collection, elements, multiple=False):
    """
    Function to delete single or multiple documents from a provided collection using a dictionary containing
    a document's elements.
    """
    if multiple:
        collection.delete_many(elements)
    else:
        collection.delete_one(elements)


def update_document(collection, query_elements, new_values):
    """
    Function to update a single document in a collection.
    """
    collection.update_one(query_elements, {'$set': new_values})


def find_duplicates(collection, library):
    """
    Function to find duplicate documents in one collection.
    """
    return list(collection.aggregate([
        {'$group': {'_id': ['$artist', '$title'], 'count': {'$sum': 1}}},
        {'$match': {'_id': {'$ne': 'null'}, 'count': {'$gt': 1}}},
        {'$project': {'name': '$_id', '_id': 0}}
    ]))


if __name__ == '__main__':
    client, mydb, collections = db_connection()
    print(find_duplicates(collections['music_collection'], '/home/lenex/code/tag_changeer/source_dir'))
