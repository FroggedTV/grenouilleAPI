from database import db

class Stream(db.Model):
    """A stream representation in the database.

    Attributes:
        id: Steam unique identifier.
        hostname: Hostname to connect to OBS.
        port: Port to connect to OBS.
        google_calendar_id: google calendar id.
    """
    __tablename__ = 'stream'

    id = db.Column(db.String(), primary_key=True)
    hostname = db.Column(db.String, nullable=True)
    port = db.Column(db.Integer(), nullable=True)
    google_calendar_id = db.Column(db.String(), nullable=True)

    def __init__(self, id):
        """Instantiate a new stream with empty values.

        Args:
            id: Twitch unique identifier.
        """
        self.id = id

    @staticmethod
    def get(id):
        """Returns the stream defined by a unique identifier.

        Args:
            id: Twitch unique identifier.
        Returns:
            Stream object with the provided identifier or None if there is no information.
        """
        return User.query.filter_by(id=id).one_or_none()
