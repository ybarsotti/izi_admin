import graphene
from django.db import transaction
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphql_jwt.decorators import login_required
from graphql_relay import from_global_id

from apps.teams.models import Team
from apps.users.models import User
from apps.users.schema import UserNode


class TeamType(DjangoObjectType):
    class Meta:
        model = Team
        description = 'Objeto de time'
        interfaces = (graphene.relay.Node, )


class AddFavoriteProject(graphene.relay.ClientIDMutation):
    success = graphene.Boolean(default_value=False)
    project = graphene.Field(TeamType)

    class Input:
        project_id = graphene.ID(required=True)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user
        project_id = from_global_id(input.get('project_id'))[1]

        user.favorite_projects.add(project_id)

        return AddFavoriteProject(project=project_id, success=True)


class CreateTeam(graphene.relay.ClientIDMutation):
    success = graphene.Boolean(default_value=False)
    team = graphene.Field(TeamType)

    class Input:
        name = graphene.String(required=True)
        description = graphene.String(required=False)
        emails = graphene.List(required=True, of_type=graphene.String)

    @classmethod
    @login_required
    def mutate_and_get_payload(cls, root, info, **input):
        user = info.context.user

        with transaction.atomic():

            team = Team.objects.create(name=input.get('name'), description=input.get('description', None),
                                       company=user.company)
            users = input.get('emails')

            for user in users:
                user_obj = User.objects.filter(email__iexact=user)

                if user_obj.exists():
                    team.users.add(user_obj.first())

        return CreateTeam(success=True)


class Mutation(graphene.AbstractType):
    create_favorite_project = AddFavoriteProject.Field()
    create_team = CreateTeam.Field()


class Query(graphene.AbstractType):
    teams = DjangoConnectionField(TeamType)

    @login_required
    def resolve_teams(self, info, **kwargs):
        """
        Retorna os times desse usuário
        :param info:
        :type info:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        user = info.context.user
        return Team.objects.filter(company__owner=user)
