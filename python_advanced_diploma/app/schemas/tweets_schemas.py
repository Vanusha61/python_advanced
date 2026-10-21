from marshmallow import Schema, fields, validate


class TweetSchema(Schema):
    id = fields.Integer(dump_only=True)
    tweet_data = fields.String(
        required=True,
        validate=validate.Length(min=1, error="Длина поста больше 1 буквы"),
        error_messages={"required": "Tweet data is required"},
    )
    tweet_media_ids = fields.List(fields.Integer(), required=False)
