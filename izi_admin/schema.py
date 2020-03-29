import graphene
import graphql_jwt

import apps.users.schema as users

from apps.users.schema import ObtainJSONWebToken


class Mutation(users.Mutation,
               graphene.ObjectType):
    token_auth = ObtainJSONWebToken.Field()


schema = graphene.Schema(mutation=Mutation)
