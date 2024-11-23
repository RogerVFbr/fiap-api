from marshmallow import Schema, fields


class ComercializacaoResponseSchema(Schema):
    id = fields.Int()
    produto = fields.Str()
    historico = fields.Dict()