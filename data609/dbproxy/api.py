from django.conf.urls import url, include, patterns
from dbproxy.models import Node, NodeUser, Profile
from rest_framework import routers, serializers, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status

class NodeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeUser
        fields = ('username', 'password')


# Serializers define the API representation.
class NodeSerializer(serializers.ModelSerializer):
    space_used = serializers.Field(source='get_space_used')
    total_space = serializers.Field(source='get_total_space')
    nodeuser_set = NodeUserSerializer(many=True, required=False)

    class Meta:
        model = Node
        fields = ('id', 'title', 'name', 'url', 'server', 'api_key', 'space_used', 'total_space', 'nodeuser_set')
        read_only_fields = ('name', 'url', 'server', 'api_key')


# ViewSets define the view behavior.
class NodeViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = NodeSerializer

    def get_queryset(self):
        return Node.objects.filter(is_grafanadb=False, user=self.request.user)

    def pre_save(self, obj):
        obj.user = self.request.user



class ProfileSerializer(serializers.ModelSerializer):
    num_of_nodes = serializers.Field(source='get_num_of_nodes')

    class Meta:
        model = Profile
        fields = ('num_of_nodes', 'max_nodes')


# ViewSets define the view behavior.
class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProfileSerializer
    # queryset = Profile.objects.all()

    def get_queryset(self):
        profile_qs = Profile.objects.filter(user=self.request.user)
        return profile_qs

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'nodes', NodeViewSet, base_name="nodes")
router.register(r'profiles', ProfileViewSet, base_name="profiles")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.


class DatasourcesAPI(APIView):
    """
    generates config.js for grafana
    """
    #authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        nodes = Node.objects.filter(user=request.user)
        resp = {}
        error = False
        for node in nodes:
            username, password = '', ''
            is_grafanadb = False
            if node.is_grafanadb:
                is_grafanadb = True
            support_metrics = not is_grafanadb
            node_qs = node.nodeuser_set.all()
            if node_qs:
                username = node_qs[0].username
                password = node_qs[0].password
            else:
                error = True
            resp_dict = [[
                '%s' % node.title,
                {
                    "type": "influxdb",
                    "url": node.url,
                    "username": username,
                    "password": password,
                    "grafanaDB": is_grafanadb,
                    "supportMetrics": support_metrics,
                },
            ],]
            resp = dict(resp_dict)
        if error:
            return Response('no datasources', status=status.HTTP_404_NOT_FOUND)
        return Response(resp)


urlpatterns = patterns(
    '',
    url(
        r'^',
        include(router.urls), name="nodes"),
    url(r'^datasources/$', DatasourcesAPI.as_view(), name="datasources"),
)
