from app.database import initialize_database

if __name__ == "__main__":
    print("Recreating database tables...")
    initialize_database()
    print("Tables created successfully.")
