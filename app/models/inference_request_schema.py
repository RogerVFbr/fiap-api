from marshmallow import Schema, fields


class InferenceRequestSchema(Schema):
    data = fields.List(fields.Float())

class InferenceRequestQuerySchema(Schema):
    name = fields.Str()
    id = fields.Str()
