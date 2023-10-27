from typing import Any, Mapping

from pymongo import *
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.typings import _DocumentType


def db_connection() -> tuple[MongoClient, Database, dict[str: Collection]]:
    client = MongoClient('localhost', 27017)
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    mydb = client['tag_changer']
    collections = {f'{name}_collection': mydb[name] for name in mydb.list_collection_names()}

    return client, mydb, collections


def insert_document(collection: Collection, data: _DocumentType) -> Any:
    """
    Function to insert a document into a collection and return the document's id.
    """
    return collection.insert_one(data).inserted_id


def find_document(collection: Collection, *elements:  Mapping[str, Any], multiple: bool = False) -> list[Mapping[str, Any]] | Mapping[str, Any] | None:
    """
    Function to retrieve single or multiple documents from a provided collection using a dictionary containing
    a document's elements.
    """
    if multiple:
        results = collection.find(*elements)
        return [r for r in results]
    else:
        return collection.find_one(*elements)


def delete_document(collection: Collection, elements: Mapping[str, Any], multiple: bool = False) -> None:
    """
    Function to delete single or multiple documents from a provided collection using a dictionary containing
    a document's elements.
    """
    if multiple:
        collection.delete_many(elements)
    else:
        collection.delete_one(elements)


def update_document(collection: Collection, query_elements, new_values) -> None:
    """
    Function to update a single document in a collection.
    """
    collection.update_one(query_elements, {'$set': new_values})


def find_duplicates(collection: Collection, library: str) -> list:
    """
    Function to find duplicate documents in one collection.
    """
    return list(collection.aggregate([
        {'$group': {'_id': ['$artist', '$title'], 'count': {'$sum': 1}}},
        {'$match': {'_id': {'$ne': 'null'}, 'count': {'$gt': 1}}},
        {'$project': {'name': '$_id', '_id': 0}}
    ]))


def main():
    client, mydb, collections = db_connection()


if __name__ == '__main__':
    main()
