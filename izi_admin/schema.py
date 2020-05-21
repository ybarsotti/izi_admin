import graphene
import graphql_jwt

import apps.users.schema as users
import apps.projects.schema as projects
import apps.teams.schema as teams


# ObtainJSONWebToken customizado para retornar o usuario juntamente com a token
class ObtainJSONWebToken(graphql_jwt.relay.JSONWebTokenMutation):
    user = graphene.Field(users.UserNode)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)


class Mutation(users.Mutation,
               teams.Mutation,
               graphene.AbstractType):
    token_auth = ObtainJSONWebToken.Field()


class Query(users.Query,
            projects.Query,
            teams.Query,
            graphene.ObjectType):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query)
