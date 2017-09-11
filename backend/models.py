from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserRefreshToken(db.Model):
    """The only valid refresh token for this user..

    Attributes:
        id: Steam unique identifier 64bits.
        token: String of the valid token
    """
    __tablename__ = 'user_refresh_token'

    id = db.Column(db.BigInteger(), primary_key=True)
    refresh_token = db.Column(db.String(), primary_key=True)

    @staticmethod
    def get(id):
        """Returns the token of a specific user.

        Args:
            id: Steam unique identifier.
        Returns:
            UserRefreshToken of the target user or None if no refresh token existing.
        """
        return UserRefreshToken.query.filter_by(id=id).one_or_none()

    @staticmethod
    def upsert(id, token):
        """Update the current refresh token valid for a user.

        Args:
            id: Steam unique identifier of the user.
            token: Refresh JWT of the user.
        Returns:
            UserRefreshToken of the target user, with the token updated.
        """
        refresh_token = UserRefreshToken.get(id)
        if refresh_token is None:
            refresh_token = UserRefreshToken()
            refresh_token.id = id
            refresh_token.refresh_token = token
        db.session.commit()

        return refresh_token

    @staticmethod
    def revoke(id):
        """Revoke the token of a specified user when logout.

        Args:
            id: Steam unique identifier of the user.
        """
        UserRefreshToken.query.filter_by(id=id).delete()
        db.session.commit()

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
