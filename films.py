import sqlite3
# films.py
# Menu based system demonstrating the film database.


def main():
    # Make a dictionary to use in the menu.
    opts = {'1': addFilm, '2': delFilm, '3': showAll,
            '4': sortYear, '5': findYear, '6': findGenre}

    # Make empty database, if one doesn't exist.
    if showAll() == -1:
        makeFilmTable()

    print("*** FILM DATABASE ***")
    print("""
    Please select an option
    1 - Add a new film
    2 - Delete a film
    3 - Show all films
    4 - Sort films by year
    5 - Find films by year
    6 - Find films by genre
    q - Exit """)

    choice = input("Your choice: ")
    try:
        print(opts[choice]())
    except KeyError:
        while choice != 'q':
            return
#        print ("Huh?")


def getNum(msg):
    """Validates integer input"""
    while 1:
        try:
            return int(input(msg))
        except ValueError:
            print ("Please enter a number.")


def makeFilmTable():
    """This creates a database with a blank table."""
    with sqlite3.connect("films.db") as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE film(
            FilmID integer,
            Title text,
            Genre string,
            Year integer,
            Primary Key (FilmID));""")
        db.commit()


def findYear():
    """Finds films made in a certain year."""
    return find("year", getNum("Enter the year: "))


def findGenre():
    """Select all films with a certain genre."""
    return find("genre", input("Genre: "))


def find(search, term):
    """Helper function for the find functions."""
    with sqlite3.connect("films.db") as db:
        cursor = db.cursor()
        sql = "SELECT * FROM film WHERE {} = ?".format(search)
        cursor.execute(sql, (term,))
        db.commit()
        results = cursor.fetchall()
        if results:
            return pretty(results)
        else:
            return "The query returned no results."


def pretty(r):
    """Prepares the result for printing"""
    msg = "\n {0:3} {1:<15} {2:<20} {3:<4}\n".format("ID", "Title", "Genre", "Year")
    msg += ' = ' * 45 + '\n'
    msg += '\n'.join("{0:3} {1:<15} {2:<20} {3:<4}".format(*i) for i in r)
    return msg


def delFilm():
    """Removes a film from the database."""
    with sqlite3.connect("films.db") as db:
        sqlite3.Cursor = db.cursor()
        sql = "delete from film where filmid = ?"
        sqlite3.Cursor.execute(sql, (getNum("Enter film ID: "),))
        db.commit()
    return ("Record removed from the database.")


def addFilm():
    """Adds a record to the database."""
    title = input("Title: ")
    genre = input("Genre: ")
    year = getNum("Year: ")
    with sqlite3.connect("films.db") as db:
        sqlite3.Cursor = db.cursor()
        sql = "INSERT INTO Film (title, genre, year) values(?, ?, ?)"
        sqlite3.Cursor.execute(sql, (title, genre, year))
        db.commit()
    return ("\"{}\" added to database.".format(title))


def sortYear():
    """Returns all the films, sorted by year."""
    return showAll("ORDER BY year")


def showAll(n=''):
    """Prints all the films in the database."""
    try:
        with sqlite3.connect("films.db") as db:
            sqlite3.Cursor = db.cursor()
            sql = "SELECT * FROM Film {}".format(n)
            sqlite3.Cursor.execute(sql)
            r = sqlite3.Cursor.fetchall()
            if r:
                return pretty(r)
            else:
                return "Empty database."
    # This is the error code returned if sql finds no data file.
    except sqlite3.OperationalError:
        return

if __name__ == "__main__":
    main()
