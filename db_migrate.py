from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager

from App import create_app, db

app = create_app()


manage = Manager(app)
migrate = Migrate(app,db)
manage.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manage.run()
# python db_migrate.py db migrate
