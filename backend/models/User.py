from database import db

class User(db.Model):
    """A user representation in the database.

    Attributes:
        id: Steam unique identifier 64bits.
        name: User name refreshed from Steam.
        refresh_token: current refresh_token valid for this user
    """
    __tablename__ = 'user'

    id = db.Column(db.BigInteger(), primary_key=True)
    name = db.Column(db.String, nullable=True)
    refresh_token = db.Column(db.String(), nullable=True)

    def __init__(self, id):
        """Instantiate a new user with default values.

        Args:
            id: Steam unique identifier 64bits.
        """
        self.id = id

    @staticmethod
    def get(id):
        """Returns the user defined by a unique identifier.

        Args:
            id: Steam unique identifier.
        Returns:
            User object with the provided identifier or None if there is no
            User with this identifier.
        """
        return User.query.filter_by(id=id).one_or_none()


class APIKey(db.Model):
    """An API Key used in the system

    Attributes:
        key_hash: sha1 of a valid API_KEY.
        description: description of the API key usage.
        refresh_token: current refresh_token valid for this API_KEY
    """
    __tablename__ = 'api_key'

    key_hash = db.Column(db.String(), primary_key=True)
    description = db.Column(db.String(), nullable=True)
    refresh_token = db.Column(db.String(), nullable=True)

    def __init__(self, key_hash, description=None):
        self.key_hash = key_hash
        self.description = description

    @staticmethod
    def get(key_hash):
        """Returns the APIKey data if found.

        Args:
            key_hash: sha1 hash of the key to find data about.
        Returns:
            APIKey object if it exists, none otherwise.
        """
        return APIKey.query.filter_by(key_hash=key_hash).one_or_none()
