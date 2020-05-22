import graphene
from graphene_django import DjangoObjectType, DjangoConnectionField
from graphql_jwt.decorators import login_required

from apps.projects.models import Project


class ProjectsType(DjangoObjectType):
    class Meta:
        model = Project
        description = 'Endpoints pertinentes à projetos'
        interfaces = (graphene.relay.Node, )


class Query(graphene.ObjectType):
    projects = DjangoConnectionField(ProjectsType)
    project_detail = graphene.Field(ProjectsType, id=graphene.String())

    @login_required
    def resolve_projects(self, info, **kwargs):
        """
        Retorna os projetos (quadros) do usuário
        :param info:
        :type info:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        user = info.context.user
        return Project.objects.filter(company__user__id=user.id)

    @login_required
    def resolve_project_detail(self, info, id, **kwargs):
        """
        Retorna os dados pro quadro
        :param id:
        :type id:
        :param info:
        :type info:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        user = info.context.user
        qs = Project.objects.filter(id=id, user__in=[user])
        if not qs.exists():
            return None
        return qs.first()
