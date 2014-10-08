# django for reg
# dashboard form influx_admin
# UserDB(Model):
#     host
#     port
#     name
#     ds_users[]
#     api_key

# Dashboards(Model):
#     json_struct

# /settings/
#     user dbs
#     create db(with user)
#     no more than 5
import uuid
import random

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Node(models.Model):
    server = models.ForeignKey('Server')
    title = models.CharField(max_length=256)
    name = models.CharField(max_length=256, blank=True)
    api_key = models.CharField(max_length=256, blank=True)
    url = models.CharField(max_length=1000, blank=True)
    user = models.ForeignKey(User)
    grafanadb = models.ForeignKey('Node', blank=True, null=True)
    is_grafanadb = models.BooleanField(default=False)
    #node_size in GB, default 10
    #node_size = models.PositiveIntegerField(default=10)
    #http://127.0.0.1:8086/db/freeloading
    #db_users

    def __str__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.server:
            self.server = get_free_server()
        if not self.name:
            self.name = '%s__%s' % (self.user.username, self.title)
        if not self.url:
            self.url = 'http://%s:%s/db/%s' % (self.server.host, self.server.port, self.name)
        if not self.api_key:
            self.api_key = str(uuid.uuid1())
        super(Node, self).save(*args, **kwargs)

    def get_space_used(self):
        return round(random.random()*10, 2)

    def get_total_space(self):
        space = 0
        try:
            user_space = self.userspace_set.last()
            space = user_space.space.space
        except:
            pass
        return space


class NodeUser(models.Model):
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    node = models.ForeignKey(Node)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User)
    info = models.CharField(max_length=1000)
    #rename to max_nodes
    max_nodes = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.user

    def get_num_of_nodes(self):
        return self.user.node_set.filter(is_grafanadb=False).count()


class Space(models.Model):
    space = models.PositiveIntegerField(default=10, unique=True)

    def __str__(self):
        return '%s' % self.space


class UserSpace(models.Model):
    user = models.OneToOneField(User)
    date_up_to = models.DateField(blank=True, null=True)
    node = models.ForeignKey(Node)
    space = models.ForeignKey(Space)

    def __str__(self):
        return '%s  %s' % (self.space, self.node.url)


class Server(models.Model):
    host = models.CharField(max_length=256)
    port = models.PositiveIntegerField(default=8086)

    def __str__(self):
        return '%s %s' % (self.host, self.port)

from django.db.models import Count

def get_free_server():
    server = Server.objects.last()
    return server

from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def profile_handler(sender, **kwargs):
    profile_sq = Profile.objects.filter(user=kwargs['instance'])
    if not profile_sq:
        Profile.objects.create(user=kwargs['instance'])
    grafana_nodes_qs = Node.objects.filter(user=kwargs['instance'], is_grafanadb=True)
    if not grafana_nodes_qs:
        server = get_free_server()
        if not server:
            server = Server.objects.create(
                host=settings.PROJECT_SETTINGS['default_grafanadb_host'],
                port=settings.PROJECT_SETTINGS['default_grafanadb_port'])
        print(server)
        Node.objects.create(
            user=kwargs['instance'],
            is_grafanadb=True,
            title=settings.PROJECT_SETTINGS['default_grafanadb_title'],
            server=server)


@receiver(post_save, sender=Node)
def node_users_handler(sender, **kwargs):
    users_qs = kwargs['instance'].nodeuser_set.all()
    if not users_qs:
        username = str(uuid.uuid1())[:6]
        password = str(uuid.uuid1())[:6]
        NodeUser.objects.create(
            username=username, password=password, node=kwargs['instance'])
