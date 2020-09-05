from app import create_app
from models import db_drop_and_create_all

def main ():
    app = create_app()
    db_drop_and_create_all()

if __name__== '__main__':
    main()