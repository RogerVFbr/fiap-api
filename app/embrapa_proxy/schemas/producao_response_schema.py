from marshmallow import Schema, fields


class ProducaoResponseSchema(Schema):
    id = fields.Int()
    produto = fields.Str()
    historico = fields.Dict()
