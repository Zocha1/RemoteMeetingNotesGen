from app import create_app
from database.db import init_db
import os
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)  
    if not os.path.exists('mydb.db'):
        init_db()
        print("Database initialized!")