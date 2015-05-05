#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#
import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect("dbname=tournament")
    cursor = conn.cursor()
    return conn, cursor

def deleteMatches():
    """Remove all the match records from the database."""
    DB, cursor = connect()
    cursor.execute('DELETE from matches')

    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB, cursor = connect()
    cursor.execute('DELETE from players')

    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB, cursor = connect()
    cursor.execute("SELECT count(*) FROM players")
    results = cursor.fetchone()

    DB.close()
    return results[0]

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB, cursor = connect()
    # use bleach on input "name" to protect from SQL injection, if this is was a front facing app.
    name = bleach.clean(name)
    SQL = "INSERT INTO players (player_name) VALUES (%s);"
    data = (name,)
    cursor.execute(SQL, data)
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB, cursor = connect()

    SQL = "SELECT players.id, player_name, COALESCE(win_count,0), COALESCE(played_count,0) from players left join standings on standings.id = players.id;"
    cursor.execute(SQL)

    results = cursor.fetchall()

    DB.close()
    return results

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB, cursor = connect()
    # use bleach on input "name" to protect from SQL injection, if this is was a front facing app.
    winner = bleach.clean(winner)
    loser = bleach.clean(loser)

    SQL = "INSERT INTO matches (winner, loser) VALUES (%s,%s);"
    data = (winner,loser)
    cursor.execute(SQL, data)

    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    items = playerStandings()
    matches = []
    # loop through entire player standings, 2 at a time, and pair up
    for i in range (0, len(items), 2):
        matches.append( (items[i][0],items[i][1],items[i+1][0],items[1][1]) )

    return matches
