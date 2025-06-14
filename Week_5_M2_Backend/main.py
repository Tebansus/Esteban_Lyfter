from db import PgManager
from creationrepo import TableCreatorRepo
from modificationrepo import ModificationRepo
from flask import Flask
from api import api_bp, init_api
# Start the Flask application
app = Flask(__name__)
if __name__ == '__main__':
    # Create a database manager instance
    db_manager = PgManager(
            db_name="postgres",
            user="postgres",
            password="Estebanessupercool22",
            host="localhost",
            port=5432,
            options= "-c search_path=lyfter_car_rental"
        )
    # Initialize the table creator and create the necessary tables, load the mock data, and set up the API
    table_creator = TableCreatorRepo(db_manager)
    table_creator.create_tables()
    table_creator.populate_table_users()
    table_creator.populate_table_cars_first_pass()
    table_creator.populate_table_car_renters()
    table_creator.adjust_car_rented_state()
    mod_repo = ModificationRepo(db_manager)
    # Initialize the API with the modification repository
    init_api(mod_repo)
    # Register the API blueprint and run the Flask app
    app.register_blueprint(api_bp)
    app.run(debug=True, host='localhost', port=5002)
    db_manager.close_connection()