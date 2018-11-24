from database import db

class DynamicConfiguration(db.Model):
    """Dynamic configuration used by multiple elements, modified using the API."""
    __tablename__ = 'dynamic_configuration'

    key = db.Column(db.String(), primary_key=True)
    value = db.Column(db.String(), nullable=False)

    def __init__(self, key, value):
        self.key = key
        self.value = value

    @staticmethod
    def get(key, default_value):
        """Get the value of a configuration key.

        Attributes:
            key: key of the configuration.
            default_value: value if not present in database.
        Returns:
            The value associated with the key.
        """
        dc = db.session().query(DynamicConfiguration).filter(DynamicConfiguration.key==key).one_or_none()
        if dc is None:
            return default_value
        else:
            return dc.value

    @staticmethod
    def update(key, value):
        dc = db.session().query(DynamicConfiguration).filter(DynamicConfiguration.key==key).one_or_none()
        if dc is None:
            dc = DynamicConfiguration(key, value)
            db.session().add(dc)
        dc.value = value
        db.session().commit()
        return dc

class CSVData(db.Model):
    """CSV Holders"""
    __tablename__= 'csv_data'

    key = db.Column(db.String(), primary_key=True)
    value = db.Column(db.Text(), nullable=False)

    def __init__(self, key):
        self.key = key

    @staticmethod
    def upsert(key, value):
        data = db.session.query(CSVData).filter(CSVData.key==key).one_or_none()
        if data is None:
            data = CSVData(key)
            db.session.add(data)
        data.value = value
        db.session.commit()
