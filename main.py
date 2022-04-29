from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from scrapeFiles import scrapeMatch

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
class Match(Resource):
    def get(self, match_id):
        result = scrapeMatch.find_matches(match_id)
        return result
 


api.add_resource(Match, "/match/<int:match_id>")

if __name__ == "__main__":
    app.run(debug=True)
