from database import db

class Stream(db.Model):
    """A stream representation in the database.

    Attributes:
        id: Stream unique identifier.
        name: Beautiful name to display.
        hostname: Hostname to connect to OBS.
        port: Port to connect to OBS.
        google_calendar_id: google calendar id.
    """
    __tablename__ = 'stream'

    id = db.Column(db.String(), primary_key=True)
    name = db.Column(db.String(), primary_key=False)
    hostname = db.Column(db.String, nullable=True)
    port = db.Column(db.Integer(), nullable=True)
    google_calendar_id = db.Column(db.String(), nullable=True)

    def __init__(self, id, name=None):
        """Instantiate a new stream with empty values.

        Args:
            id: Twitch unique identifier.
        """
        self.id = id
        self.name = name if name is not None else id

    @staticmethod
    def get(id):
        """Returns the stream defined by a unique identifier.

        Args:
            id: Twitch unique identifier.
        Returns:
            Stream object with the provided identifier or None if there is no information.
        """
        return Stream.query.filter_by(id=id).one_or_none()

    @staticmethod
    def upsert(id, name=None, hostname=None, port=None, google_calendar_id=None):
        """Insert a Stream or update it if present."""
        stream = db.session().query(Stream).filter(Stream.id==id).one_or_none()
        if stream is None:
            stream = Stream(id, name)
            db.session.add(stream)
        if name is not None:
            stream.name = name
        if hostname is not None:
            stream.hostname = hostname
        if port is not None:
            stream.port = port
        if google_calendar_id is not None:
            stream.google_calendar_id = google_calendar_id
        db.session.commit()
