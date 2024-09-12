from flask import current_app as app
from flask import url_for

genres = {
    "Mythical Historic Fantasy": "Swords, shields, bows and magic",
    "Cult Mystery": "Cults, mysteries and conspiracies",
    "Zombie Apocalypse": "Zombies, bandits and looting",
    "Apocalypse": "Bandits and looting",
    "Crime Film Noir": "Smoke and back alleys, see!",
    "Existential Horror": "Your existence means nothing.",
    "Dystopian Future": "The future is bleak",
    "Mythic Folklore": "Werewolves, vampires, ghosts and other monsters",
    "Science Fiction": "Aliens, robots, space travel and other cool stuff",
}


@app.context_processor
def genre_img_processor():
    def genre_img(genre):

        try:
            genre = int(genre)
        except ValueError:
            genre = 0

        if genre == 0:
            return url_for("static", filename="purgatory.png")

        if genre == 1:
            return url_for("static", filename="mythical-historic-fantasy.png")

        if genre == 2:
            return url_for("static", filename="cult-mystery.png")

        if genre == 3:
            return url_for("static", filename="zombie-apocalypse.png")

        if genre == 4:
            return url_for("static", filename="apocalypse.png")

        if genre == 5:
            return url_for("static", filename="crime-film-noir.png")

        if genre == 6:
            return url_for("static", filename="existential-horror.png")

        if genre == 7:
            return url_for("static", filename="dystopian-future.png")

        if genre == 8:
            return url_for("static", filename="mythic-folklore.png")

        if genre == 9:
            return url_for("static", filename="science-fiction.png")

    return {
        "genre_img": genre_img
    }
