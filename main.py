from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

from scrapeFiles import scrapeMatch

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class MatchModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team1 = db.Column(db.String(100), nullable=False)
    team2 = db.Column(db.String(100), nullable=False)
    team1_score = db.Column(db.Integer, nullable=False)
    team2_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        text = f"Match(team1 = {self.team1}, team = {self.team2}, team1_score = {self.team1_score}, team2_score = {self.team2_score})"

match_put_args = reqparse.RequestParser()
match_put_args.add_argument("team1", type=str, required=True, location='form', help="Name of the first team is required")
match_put_args.add_argument("team2", type=str, required=True, location='form', help="Name of the second team is required")
match_put_args.add_argument("team1_score", type=int, required=True, location='form', help="Score of the first team is required")
match_put_args.add_argument("team2_score", type=int, required=True, location='form', help="Score of the second team is required")

match_update_args = reqparse.RequestParser()
match_update_args.add_argument("team1", type=str, required=False, location='form', help="Name of the first team is required")
match_update_args.add_argument("team2", type=str, required=False, location='form', help="Name of the second team is required")
match_update_args.add_argument("team1_score", type=int, required=False, location='form', help="Score of the first team is required")
match_update_args.add_argument("team2_score", type=int, required=False, location='form', help="Score of the second team is required")

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
        #result = MatchModel.query.filter_by(id=match_id).first()
        result = scrapeMatch.find_matches(match_id)
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

    @marshal_with(resource_fields)
    def patch(self, match_id):
        args = match_update_args.parse_args()
        result = MatchModel.query.filter_by(id=match_id).first()
        if not result:
            abort(404, message="Could not find match with that ID")
        if "team1" in args:
            result.team1 = args['team1']
        if "team2" in args:
            result.team2 = args['team2']
        if "team1_score" in args:
            result.team1_score = args['team1_score']
        if "team2_score" in args:
            result.team2_score = args['team2_score']

        db.session.add(result)
        db.session.commit()

        return result, 200


    def delete(self, match_id):
        result = MatchModel.query.filter_by(id=match_id).first()
        if not result:
            abort(404, message="Could not find match with that ID")
        db.session.delete(result)
        db.session.commit()
        return f'Deleted {match_id}', 204
 


api.add_resource(Match, "/match/<int:match_id>")

if __name__ == "__main__":
    app.run(debug=True)
