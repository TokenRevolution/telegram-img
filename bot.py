import os
import hashlib
from telegram.ext import Updater, MessageHandler, Filters

# Dizionario per memorizzare gli hash delle immagini già viste
image_hashes = {}

# Funzione per calcolare l'hash SHA1 di un'immagine
def hash_image(image_path):
    with open(image_path, "rb") as image:
        return hashlib.sha1(image.read()).hexdigest()

# Funzione per gestire i messaggi ricevuti
def handle_message(update, context):
    message = update.message
    if message.photo:
        image_file = message.photo[-1].get_file()
        image_path = "image.jpg"
        image_file.download(image_path)
        image_hash = hash_image(image_path)
        user_id = message.from_user.id
        
        if image_hash in image_hashes:
            # Immagine già vista, aumentare il contatore delle copie
            image_hashes[image_hash]["copies"] += 1
            image_hashes[image_hash]["users"].append(user_id)
            print("Copie trovate: ", image_hashes[image_hash]["copies"])
            print("User IDs: ", image_hashes[image_hash]["users"])
        else:
            # Nuova immagine, aggiungere l'hash al dizionario
            image_hashes[image_hash] = {"copies": 1, "users": [user_id]}
            
        os.remove(image_path)

# Creare un oggetto Updater
updater = Updater(token="5827462043:AAGu6fI0rcYkxEki8RvbhNhhtD585lCyBhg", use_context=True)

# Ottenere l'id del gruppo
chat_id = -1001723784468

# Aggiungere il gestore dei messaggi al dispatcher
updater.dispatcher.add_handler(MessageHandler(Filters.photo, handle_message))

# Avviare l'ascolto degli aggiornamenti
updater.start_polling()
updater.idle()
