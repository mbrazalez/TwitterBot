import json
import openai
import tweepy

from configuration import configuration as conf
from s3 import s3_save_file, s3_get_object

# AUTH IN TWITTER API
client = tweepy.Client(conf.BEARER_TOKEN, conf.API_KEY, conf.API_SECRET_KEY, conf.ACCESS_TOKEN, conf.ACCESS_TOKEN_SECRET)

# TODO: To use the previous API version uncomment the following lines
auth = tweepy.OAuth1UserHandler(conf.API_KEY, conf.API_SECRET_KEY, conf.ACCESS_TOKEN, conf.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


def handler():
    list_of_characters = s3_get_object(key='characters-list', bucketname=conf.S3_BUCKET_STORAGE)
    tweet = get_tweet(list_of_characters)
    s3_save_file(key='characters-list', content=str(list_of_characters + ', ' + tweet['personaje1']+', ' + tweet['personaje2']), bucketname=conf.S3_BUCKET_STORAGE)
    client.create_tweet(text=tweet['tweet'])


# Function which makes a call to the OpenAi API in order to get the tweet in json format
def get_tweet(list_of_characters):
    messages = [
    {"role": "system",
        "content": "Eres una IA entrenada para escribir un tweet inventándote una historia en la que dos personajes famosos de España pueden ser tanto personas reales como de la ficción, cine, literatura, televisión..., "
                   "combaten por algo y finalmente uno de los dos gana"},
    {"role": "user", "content": f"""Asegúrate de que el texto generado para el tweet no supere los 200 caracteres, que los personajes escogidos no estén en esta lista {list_of_characters}, que el tweet tenga sentido y sea cómico, 
        y debes darme la respuesta en un formato json con la siguiente forma:
        personaje1: (En este campo debes introducir el nombre del primer personaje escogido para el tweet en formato string),
        personaje2: (En este campo debes introducir el nombre del segundo personaje escogido para el tweet en formato string),
        tweet: (En este campo debes introducir el tweet que has creado en formato string)"""}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        n=1,
        stop=None,
        temperature=0)

    return json.loads(response.choices[0].message.content)


if __name__ == "__main__":
    handler()