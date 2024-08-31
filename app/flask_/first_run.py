import os

from flask_imp.auth import encrypt_password, generate_salt, generate_private_key


def first_run(imp):
    print("Running first run setup")

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

    get_genres = imp.model("Genre").read(all_rows=True)

    database_genres = {}

    if get_genres:
        for genre in get_genres:
            database_genres[genre.genre] = genre.description

    for genre, description in genres.items():
        if genre in database_genres:
            continue

        imp.model("Genre").create(
            values={
                "genre": genre,
                "description": description,
            }
        )

    default_admin_email_address = os.environ.get("DEFAULT_ADMIN_ACCOUNT", "admin@localhost")
    default_admin_password = os.environ.get("DEFAULT_ADMIN_PASSWORD", "password")

    salt = generate_salt()
    private_key = generate_private_key(salt)
    password = encrypt_password(default_admin_password, salt)

    get_admin = imp.model("User").read(
        fields={"email_address": default_admin_email_address}
    )

    if not get_admin:
        imp.model("User").create(
            values={
                "first_name": "EasyQuest Super Admin",
                "email_address": default_admin_email_address,
                "password": password,
                "salt": salt,
                "private_key": private_key,
                "permission_level": 10,
            }
        )

    imp.model("System").create_system()
