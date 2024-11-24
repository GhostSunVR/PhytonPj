import psycopg2

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        port="5432",
        database="db",
        user="user",
        password="password"
    )

def create_tables():
    connection = get_db_connection()
    cursor = connection.cursor()

    # Помилки (Errors)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Errors (
        error_id SERIAL PRIMARY KEY,
        description TEXT NOT NULL,
        date_received DATE NOT NULL,
        severity_level VARCHAR(20) NOT NULL CHECK (severity_level IN ('Critical', 'Important', 'Minor')),
        functionality_category VARCHAR(50) NOT NULL CHECK (functionality_category IN ('Interface', 'Data', 'Algorithm', 'Other', 'Unknown')),
        source VARCHAR(20) NOT NULL CHECK (source IN ('User', 'Tester'))
    );
    """)

    # Програмісти (Programmers)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Programmers (
        programmer_id SERIAL PRIMARY KEY,
        last_name VARCHAR(50) NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        phone_number VARCHAR(15) NOT NULL
    );
    """)

    # Виправлення помилок (Fixes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Fixes (
        fix_id SERIAL PRIMARY KEY,
        error_id INT NOT NULL,
        programmer_id INT NOT NULL,
        start_date DATE NOT NULL,
        duration_days INT NOT NULL CHECK (duration_days IN (1, 2, 3)),
        daily_rate DECIMAL(10, 2) NOT NULL,
        FOREIGN KEY (error_id) REFERENCES Errors(error_id) ON DELETE CASCADE,
        FOREIGN KEY (programmer_id) REFERENCES Programmers(programmer_id) ON DELETE CASCADE
    );
    """)

    connection.commit()
    cursor.close()
    connection.close()


if __name__ == "__main__":
    create_tables()
