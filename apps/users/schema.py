import django_filters
import graphene
import graphql_jwt
from django.core import exceptions
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql import GraphQLError
from graphql_jwt import shortcuts
from graphql_jwt.decorators import login_required

from .models import User


class UsuarioFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'first_name': ['icontains', ],
            'email': ['icontains', ],
        }

    @property
    def qs(self):
        # faz com que a listagem de usuarios retorne apenas usuarios ativos na aplicação
        return super(UsuarioFilter, self).qs.filter(is_active=True)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('is_active', 'is_staff', 'is_superuser', 'password')
        interfaces = (graphene.relay.Node,)


class CreateUser(graphene.relay.ClientIDMutation):
    # campos de retorno
    user = graphene.Field(UserNode)
    success = graphene.Boolean(default_value=False)
    token = graphene.String()

    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        user_type = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):

        user = User(**input)
        password = input.get('password')

        if len(password) < 6:
            raise GraphQLError('A senha deve ter 6 ou mais caracteres')

        try:
            # valida os dados informados
            user.full_clean()
        except exceptions.ValidationError as e:
            raise GraphQLError(e.messages)

        # Chama o metodo create_user no objeto de usuario.
        # Sem isso, o password do usuário é armazenado em texto plano.
        new_user = User.objects.create_user(**input)
        new_user.save()

        # token gerada a partir do novo usuario criado - permite login do usuario logo apos cadastro na aplicação
        token = shortcuts.get_token(user=new_user, context=info.context)

        return CreateUser(token=token, user=new_user, success=True)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


class Query(graphene.ObjectType):
    user_list = DjangoFilterConnectionField(UserNode, filterset_class=UsuarioFilter)

    @login_required
    def resolve_user_list(self, info, **kwargs):

        if 'email__icontains' not in kwargs:
            return []

        return UsuarioFilter(kwargs).qs
