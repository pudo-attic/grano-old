from colander import SchemaType, Invalid, null

from grano.model import Network, Entity

class ValidationContext(object):

    def __init__(self, network=None):
        self.network = network


class NetworkSchemaType(SchemaType):
    
    def __init__(self, context):
        self.context = context

    def serialize(self, node, appstruct):
        return appstruct.slug

    def deserialize(self, node, cstruct):
        slug = cstruct.get('slug') if isinstance(cstruct, dict) else cstruct
        if slug is null or slug is None:
            raise Invalid(node, "No network specified")
        obj = Network.by_slug(slug)
        if obj is None:
            raise Invalid(node, "No such network: %r")
        if self.context.network and obj.id != self.context.network.id:
            raise Invalid(node, "%r is not the current network.")
        return obj


class EntitySchemaType(SchemaType):

    def __init__(self, context):
        self.context = context

    def serialize(self, node, appstruct):
        return {'id': appstruct.id, 'slug': appstruct.slug, 
                'type': appstruct.type}

    def deserialize(self, node, cstruct):
        id = cstruct.get('id') if isinstance(cstruct, dict) else cstruct
        if id is null or id is None:
            raise Invalid(node, "No network specified")
        obj = Entity.current_by_id(id)
        if obj is None:
            raise Invalid(node, "No such entity: %r")
        if obj.network_id != self.context.network.id:
            raise Invalid(node, "%r is not the current network.")
        return obj

