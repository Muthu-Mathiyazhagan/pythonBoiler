from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)
api = Api(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uId = db.Column(db.Integer)
    userName = db.Column(db.String(50))
    email = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    purpose = db.Column(db.String(255))
    poc = db.Column(db.String(255))
    base64 = db.Column(db.Text())

    def __repr__(self):
        return '<User %s>' % self.userName


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "userName", "email", "phone", "purpose", "poc", "base64")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return users_schema.dump(users)

    def post(self):
        payload = request.json

        new_user = User()
        if 'userName' in payload and payload['userName']:
            new_user.userName = payload['userName']
        if 'uId' in payload and payload['uId']:
            new_user.uId = payload['uId']

        if 'email' in payload and payload['email']:
            new_user.email = payload['email']

        if 'phone' in payload and payload['phone']:
            new_user.phone = payload['phone']

        if 'purpose' in payload and payload['purpose']:
            new_user.purpose = payload['purpose']

        if 'poc' in payload and payload['poc']:
            new_user.poc = payload['poc']

        if 'base64' in payload and payload['base64']:
            new_user.base64 = payload['base64']

        # new_user = User(
        #     userName=request.json['userName'],
        #     email=request.json['email'],
        #     phone=request.json['phone'],
        #     purpose=request.json['purpose'],
        #     poc=request.json[''],
        #     base64=request.json['base64'],
        # )

        db.session.add(new_user)
        db.session.commit()
        return user_schema.dump(new_user)


class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    def patch(self, user_id):
        user = User.query.get_or_404(user_id)

        if 'userName' in request.json:
            user.userName = request.json['userName']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'phone' in request.json:
            user.phone = request.json['phone']
        if 'purpose' in request.json:
            user.purpose = request.json['purpose']
        if 'poc' in request.json:
            user.poc = request.json['poc']
        if 'base64' in request.json:
            user.base64 = request.json['base64']

        db.session.commit()
        return user_schema.dump(user)

    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
