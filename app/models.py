import mysql.connector
from config.config import Config


# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------
def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )


# -------------------------------------------------
# GAME OPERATIONS
# -------------------------------------------------
def create_game(player_x, player_o):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO games (player_x, player_o, board_state)
        VALUES (%s, %s, %s)
        """,
        (player_x, player_o, ' ' * 9)
    )

    conn.commit()
    game_id = cursor.lastrowid

    cursor.close()
    conn.close()
    return game_id


def update_game(game_id, board_state, winner=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE games
        SET board_state = %s, winner = %s
        WHERE id = %s
        """,
        (board_state, winner, game_id)
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_scores():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT winner
        FROM games
        WHERE winner IS NOT NULL
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    scores = {"X": 0, "O": 0}
    for (winner,) in rows:
        if winner in scores:
            scores[winner] += 1

    return scores


# -------------------------------------------------
# MATCH HISTORY (LAST 10 GAMES)
# -------------------------------------------------
def save_match(player_x, player_o, winner):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO match_history (player_x, player_o, winner)
        VALUES (%s, %s, %s)
        """,
        (player_x, player_o, winner)
    )

    conn.commit()
    cursor.close()
    conn.close()


def get_match_history():
    """
    Fetch last 10 matches (most recent first)
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT player_x, player_o, winner, played_at
        FROM match_history
        ORDER BY played_at DESC
        LIMIT 10
    """)

    matches = cursor.fetchall()

    cursor.close()
    conn.close()
    return matches
