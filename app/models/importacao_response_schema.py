from marshmallow import Schema, fields


class ImportacaoResponseSchema(Schema):
    id = fields.Int()
    pais = fields.Str()
    categoria = fields.Str()
    historico_qtd = fields.Dict()
    historico_vlr = fields.Dict()
