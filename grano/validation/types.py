from colander import SchemaType, Invalid, null


class ValidationContext(object):

    def __init__(self, network=None, account=None, query=None):
        self.network = network
        self.account = account
        self.query = query


class EntitySchemaType(SchemaType):

    def __init__(self, context):
        self.context = context

    def serialize(self, node, appstruct):
        return {'id': appstruct.id,
                'type': appstruct.type}

    def deserialize(self, node, cstruct):
        id = cstruct.get('id') if isinstance(cstruct, dict) else cstruct
        if id is null or id is None:
            raise Invalid(node, "No entity specified")
        obj = self.context.network.Entity.current_by_id(id)
        if obj is None:
            raise Invalid(node, "No such entity: %r")
        return obj
