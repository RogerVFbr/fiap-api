from marshmallow import Schema, fields


class ProcessamentoResponseSchema(Schema):
    id = fields.Int()
    control = fields.Str()
    cultivar = fields.Str()
    historico = fields.Dict()