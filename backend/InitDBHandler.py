import sqlite3

def init_db(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS stations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        token TEXT NOT NULL,
        UNIQUE(token)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id INTEGER NOT NULL,
        datetime DATETIME NOT NULL,
        temperature DOUBLE PRECISION NOT NULL,
        humidity DOUBLE PRECISION NOT NULL,
        wspeed DOUBLE PRECISION NOT NULL,
        wdirection DOUBLE PRECISION NOT NULL,
        rain DOUBLE PRECISION NOT NULL,
        FOREIGN KEY (station_id) REFERENCES stations(id)
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id INTEGER,
        data_id INTEGER NOT NULL,
        token TEXT NOT NULL,
        opened_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (station_id) REFERENCES stations(id),
        FOREIGN KEY (data_id) REFERENCES data(id)
    )
    ''')
    cursor.execute('''
    CREATE TRIGGER immutable_datetime_onupdate
    BEFORE UPDATE ON data
    FOR EACH ROW
    WHEN NEW.datetime <> OLD.datetime
    BEGIN
        SELECT RAISE(ABORT, 'datetime is immutable and cannot be modified');
    END;
    ''')
    cursor.execute('''
    CREATE TRIGGER immutable_station_id_onupdate
    BEFORE UPDATE ON data
    FOR EACH ROW
    WHEN NEW.station_id <> OLD.station_id
    BEGIN
        SELECT RAISE(ABORT, 'station_id is immutable and cannot be modified');
    END;
    ''')
    conn.commit()
    conn.close()
