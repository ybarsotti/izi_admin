import graphene
import graphql_jwt

import apps.users.schema


# class Query(apps.users.schema.Query, graphene.ObjectType):
#     pass


class Mutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(mutation=Mutation)
