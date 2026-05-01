# movies_update_and_delete.py
# Author: Rikki Kratochvil
# Assignment: Movies: Update & Deletes

import mysql.connector
from mysql.connector import errorcode

config = {
    "user": "root",
    "password": "Dragon@1",
    "host": "localhost",
    "database": "movies",
    "raise_on_warnings": True
}


def show_films(cursor, title):
    query = """
        SELECT film_name AS Name,
               film_director AS Director,
               genre_name AS Genre,
               studio_name AS Studio
        FROM film
        INNER JOIN genre ON film.genre_id = genre.genre_id
        INNER JOIN studio ON film.studio_id = studio.studio_id
    """

    cursor.execute(query)
    films = cursor.fetchall()

    print("\n-- {} --".format(title))

    for film in films:
        print("Film Name: {}\nDirector: {}\nGenre: {}\nStudio: {}\n".format(
            film[0], film[1], film[2], film[3]
        ))


try:
    db = mysql.connector.connect(**config)
    cursor = db.cursor()

    show_films(cursor, "DISPLAYING FILMS")

    # Insert a new movie. Do not use Star Wars.
    cursor.execute("""
        INSERT INTO film 
            (film_name, film_releaseDate, film_runtime, film_director, studio_id, genre_id)
        VALUES 
            ('The Dark Knight', '2008', 152, 'Christopher Nolan', 1, 1)
    """)

    show_films(cursor, "DISPLAYING FILMS AFTER INSERT")

    # Update Alien to Horror.
    cursor.execute("""
        UPDATE film
        SET genre_id = (SELECT genre_id FROM genre WHERE genre_name = 'Horror')
        WHERE film_name = 'Alien'
    """)

    show_films(cursor, "DISPLAYING FILMS AFTER UPDATE- Changed Alien to Horror")

    # Delete Gladiator.
    cursor.execute("""
        DELETE FROM film
        WHERE film_name = 'Gladiator'
    """)

    show_films(cursor, "DISPLAYING FILMS AFTER DELETE")

    db.commit()

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("The username or password is incorrect.")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("The database does not exist.")
    else:
        print(err)

finally:
    if "db" in locals() and db.is_connected():
        cursor.close()
        db.close()