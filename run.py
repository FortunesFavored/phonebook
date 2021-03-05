from app import App, db
from app.models import User, gamePost

if __name__ == "__main__":
    App.run()

@App.shell_context_processor
def make_shell_context():
    return {'db':db, 'User':User, 'gamePost': gamePost}