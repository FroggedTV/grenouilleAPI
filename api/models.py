from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user representation in the database.

    Attributes:
        id: Steam unique identifier 64bits.
    """
    __tablename__ = 'user'

    id = db.Column(db.BigInteger(), primary_key=True)

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
