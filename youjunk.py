from app import app, db
from app.models import Channel, Video, Website, Article

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Channel': Channel, 'Video': Video, 'Website' : Website, 'Article' : Article}



#google.auth.exceptions.RefreshError: The credentials do not contain the necessary fields need to refresh the access token. You must specify refresh_token, token_uri, client_id, and client_secret.
