from app import db, ma
from passlib.hash import pbkdf2_sha256 as sha256


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String, unique=False, nullable=False)
    title = db.Column(db.String, unique=False, nullable=False)
    description = db.Column(db.String, unique=False, nullable=False)
    link = db.Column(db.String, unique=False, nullable=False)
    location = db.Column(db.String, unique=False, nullable=False)

    def save_to_db(self):
        if (
            not Job.query.filter_by(
                company=self.company, title=self.title).first()
        ):  # Same position on different websites
            db.session.add(self)
            db.session.commit()

    # def __repr__(self):
    #     return f"TestPrint('{self.company}')"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
                'username': x.username,
                'password': x.password
            }

        return {'users': list(map(lambda x: to_json(x), User.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {'message': '{} row(s) deleted'.format(num_rows_deleted)}
        except Exception:
            return {'message': 'Something went wrong'}

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)


class JobSchema(ma.ModelSchema):
    class Meta:
        model = Job
