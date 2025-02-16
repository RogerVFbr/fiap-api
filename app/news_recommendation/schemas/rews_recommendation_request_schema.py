from marshmallow import Schema, fields


class NewsRecommendationRequestBodySchemaItem(Schema):
    news_id = fields.Str()
    scroll_percentage = fields.Float()
    time_on_page = fields.Float()
    viewed_at = fields.DateTime(format='%Y-%m-%d %H:%M:%S')

class NewsRecommendationRequestBodySchema(Schema):
    user_id = fields.Str()
    views = fields.List(fields.Nested(NewsRecommendationRequestBodySchemaItem))

class NewsRecommendationRequestQuerySchema(Schema):
    name = fields.Str()
    id = fields.Str()

