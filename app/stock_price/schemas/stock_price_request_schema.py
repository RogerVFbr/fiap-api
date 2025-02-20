from marshmallow import Schema, fields


class StockPriceRequestSchema(Schema):
    data = fields.List(fields.Float())

class StockPriceRequestQuerySchema(Schema):
    name = fields.Str()
    id = fields.Str()
