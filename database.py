import sqlite3

DB_PATH = "app.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def init_db():
    conn = get_db()

    tables = {r[0] for r in conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()}
    if 'teams' in tables:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(teams)").fetchall()}
        if 'leader_id' not in cols:
            conn.executescript("""
                DROP TABLE IF EXISTS participations;
                DROP TABLE IF EXISTS members;
                DROP TABLE IF EXISTS teams;
            """)
            conn.commit()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS events (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            description TEXT,
            slug        TEXT UNIQUE NOT NULL,
            location    TEXT DEFAULT 'IT Cube',
            is_active   INTEGER DEFAULT 1
        );

        CREATE TABLE IF NOT EXISTS cases (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id    INTEGER REFERENCES events(id) ON DELETE CASCADE,
            title       TEXT NOT NULL,
            description TEXT,
            limit_teams INTEGER DEFAULT 8
        );

        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            age       INTEGER NOT NULL,
            email     TEXT,
            phone     TEXT,
            login     TEXT UNIQUE NOT NULL,
            password  TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS invite_codes (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            code      TEXT UNIQUE NOT NULL,
            event_id  INTEGER REFERENCES events(id),
            is_used   INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS teams (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            name       TEXT NOT NULL,
            event_id   INTEGER REFERENCES events(id) ON DELETE CASCADE,
            case_id    INTEGER REFERENCES cases(id),
            leader_id  INTEGER REFERENCES users(id),
            team_code  TEXT UNIQUE NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS members (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            team_id INTEGER REFERENCES teams(id) ON DELETE CASCADE,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(team_id, user_id)
        );

        CREATE TABLE IF NOT EXISTS admins (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            email      TEXT UNIQUE NOT NULL,
            password   TEXT NOT NULL,
            name       TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

    conn.close()
