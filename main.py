from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class MatchModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(100), nullable=False)
    team2 = db.Column(db.String(100), nullable=False)
    score1 = db.Column(db.Integer, nullable=False)
    score2 = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "Match(team1 = {team1}, team = {team2}, score1 = {score1}, score2 = {score2})"

match_put_args = reqparse.RequestParser()
match_put_args.add_argument("team1", type=str, required=True, location='form', help="Name of the first team is required")
match_put_args.add_argument("team2", type=str, required=True, location='form', help="Name of the second team is required")
match_put_args.add_argument("team1_score", type=int, required=True, location='form', help="Score of the first team is required")
match_put_args.add_argument("team2_score", type=int, required=True, location='form', help="Score of the second team is required")

resource_fields = {
    'id' : fields.Integer,
    'team1' : fields.String,
    'team2' : fields.String,
    'team1_score' : fields.Integer,
    'team2_score' : fields.Integer
}

class Match(Resource):
    @marshal_with(resource_fields)
    def get(self, match_id):
        result = MatchModel.query.filter_by(id=match_id).first()
        if not result:
            abort(404, message="Could not find match with that ID")
        return result

    @marshal_with(resource_fields)
    def put(self, match_id):
        args = match_put_args.parse_args()
        result = MatchModel.query.filter_by(id=match_id).first()
        if result:
            abort(409, message="Match ID taken...")
        match = MatchModel(id=match_id, team1=args['team1'], team2=args['team2'], team1_score=args['team1_score'], team2_score=args['team2_score'])
        db.session.add(match)
        db.session.commit()
        return match, 201

    def delete(self, match_id):
        return '', 204
 


api.add_resource(Match, "/match/<int:match_id>")

if __name__ == "__main__":
    app.run(debug=True)
