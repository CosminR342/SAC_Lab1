from recombee_api_client.api_client import RecombeeClient, Region
from recombee_api_client.api_requests import AddItem, AddItemProperty, SetItemValues, ListItems
from recombee_api_client.exceptions import APIException
import pandas as pd

client = RecombeeClient(
  'upb-sac-dev', 
  'zmBSrKrHi0IImfXjbJyOFGaA5tjNZR2MdY0d7YtQX559zQlfY7gDjeN4MCG5QDnR', 
  region=Region.EU_WEST
)

df = pd.read_csv('./archive/top250.csv', usecols=["name", "rating", "genre", "year"])

def addItemProperties():
    client.send(AddItemProperty('name', 'string'))
    client.send(AddItemProperty('rating', 'double'))
    client.send(AddItemProperty('genre', 'string'))
    client.send(AddItemProperty('year', 'int'))


def addItems():
    # add items
    for index, row in df.iterrows():
        movie_id = str(index)  # You can use a unique identifier as the item ID

        try:
            # Send the item data to Recombee
            client.send(AddItem(movie_id))
            print(f"Added movie with ID {movie_id} to Recombee")
        except APIException as e:
            print(f"Error adding movie with ID {movie_id} to Recombee: {e}")

    addItemProperties()

    for index, row in df.iterrows():
        name = row['name']
        rating = row['rating']
        genre = row['genre']
        year = row['year']

        # Define the item data
        item_data = {
            'name': name,
            'rating': rating,
            'year': year,
            'genre': genre,
        }
        client.send(SetItemValues(str(index), item_data))

def printItems():
    result = client.send(ListItems(return_properties=True))
    print(result)

printItems()