
import sqlite3
import os

# Store database in the main project folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "analysis_history.db")


def initialize_db():
    """Create the analysis history table."""

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            analysis_type TEXT NOT NULL,
            result_label TEXT NOT NULL,
            summary TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_analysis(analysis_type, result_label, summary):
    """Save non-sensitive analysis metadata."""

    connection = sqlite3.connect(DATABASE_PATH)

    connection.execute("""
        INSERT INTO analysis_history
        (analysis_type, result_label, summary)
        VALUES (?, ?, ?)
    """, (analysis_type, result_label, summary))

    connection.commit()
    connection.close()


def get_history():
    """Retrieve previous analysis records."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    records = connection.execute("""
        SELECT id, analysis_type, result_label, summary, created_at
        FROM analysis_history
        ORDER BY id DESC
    """).fetchall()

    connection.close()

    return [dict(record) for record in records]


def get_dashboard_stats():
    """Calculate dashboard statistics."""

    connection = sqlite3.connect(DATABASE_PATH)

    total_passwords = connection.execute("""
        SELECT COUNT(*)
        FROM analysis_history
        WHERE analysis_type = 'Password'
    """).fetchone()[0]

    weak_passwords = connection.execute("""
        SELECT COUNT(*)
        FROM analysis_history
        WHERE analysis_type = 'Password'
        AND LOWER(result_label) LIKE '%weak%'
    """).fetchone()[0]

    total_analyses = connection.execute("""
        SELECT COUNT(*)
        FROM analysis_history
    """).fetchone()[0]

    connection.close()

    return {
        "total_passwords": total_passwords,
        "weak_passwords": weak_passwords,
        "total_analyses": total_analyses
    }


if __name__ == "__main__":

    initialize_db()

    print("Database initialized successfully!")

    print("\nDashboard Statistics:")
    print(get_dashboard_stats())

    print("\nDatabase History:")

    for record in get_history():
        print(record)
