from marshmallow import Schema, fields


class NewsRecommendationResponseSchema(Schema):
    model_name = fields.Str()
    model_id = fields.Str()
    output = fields.List(fields.Str())
