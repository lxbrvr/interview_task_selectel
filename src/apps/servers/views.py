from apps.servers.models import Rack, Server
from apps.servers import serializers, services
from core import views as core_views


class RackListApiView(core_views.ListApiView):
    model_class = Rack
    schema_class = serializers.RackSchema


class RackCreateApiView(core_views.CreateApiView):
    model_class = Rack
    schema_class = serializers.RackSchema


class RackDetailApiView(core_views.DetailApiView):
    schema_class = serializers.RackSchema
    model_class = Rack
    url_param = 'rack_id'


class RackUpdateApiView(core_views.UpdateApiView):
    schema_class = serializers.RackSchema
    model_class = Rack
    url_param = 'rack_id'


class RackPatchApiView(core_views.PatchApiView):
    schema_class = serializers.RackSchema
    model_class = Rack
    url_param = 'rack_id'


class ServerListApiView(core_views.ListApiView):
    model_class = Server
    schema_class = serializers.ServerSchema


class ServerDetailApiView(core_views.DetailApiView):
    model_class = Server
    schema_class = serializers.ServerSchema
    url_param = 'server_id'


class ServerCreateApiView(core_views.ActionApiView):
    schema_class = serializers.ServerSchema

    def make_action(self, deserialized_data: dict) -> dict:
        server = Server(**deserialized_data)
        rack_service = services.RackService().from_id(server.rack_id)
        rack_service.add_server(server)

        return self.get_schema().serialize(server.asdict())


class ServerUpdateApiView(core_views.UpdateApiView):
    model_class = Server
    schema_class = serializers.ServerSchema
    url_param = 'server_id'


class ServerPatchApiView(core_views.PatchApiView):
    model_class = Server
    schema_class = serializers.ServerSchema
    url_param = 'server_id'


class ServerDestroyApiView(core_views.DestroyApiView):
    model_class = Server
    schema_class = serializers.ServerSchema
    url_param = 'server_id'

    def destroy(self, obj: Server) -> None:
        services.ServerService().from_obj(obj).mark_as_deleted()


class ServerPurchaseActionApiView(core_views.ActionApiView):
    schema_class = serializers.PurchaseSchema

    def make_action(self, deserialized_data: dict) -> dict:
        server_id = deserialized_data['server_id']
        server_service = services.ServerService().from_id(server_id)
        server_service.pay()

        return self.get_schema().serialize(server_service.obj.asdict())
