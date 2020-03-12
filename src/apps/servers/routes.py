from apps.servers import views as server_views
from core.routes import url


patterns = (
    url(
        method='GET',
        path='/servers/',
        handler=server_views.ServerListApiView.as_view('servers'),
    ),

    url(
        method='POST',
        path='/servers/purchases/',
        handler=server_views.ServerPurchaseActionApiView.as_view('servers_purchases'),
    ),

    url(
        method='POST',
        path='/servers/',
        handler=server_views.ServerCreateApiView.as_view('servers_post'),
    ),

    url(
        method='GET',
        path=f'/servers/<int:server_id>/',
        handler=server_views.ServerDetailApiView.as_view('server_detail'),
    ),

    url(
        method='DELETE',
        path=f'/servers/<int:server_id>/',
        handler=server_views.ServerDestroyApiView.as_view('server_destroy'),
    ),

    url(
        method='PUT',
        path=f'/servers/<int:server_id>/',
        handler=server_views.ServerUpdateApiView.as_view('server_put'),
    ),

    url(
        method='PATCH',
        path=f'/servers/<int:server_id>/',
        handler=server_views.ServerPatchApiView.as_view('server_patch'),
    ),

    url(
        method='GET',
        path='/racks/',
        handler=server_views.RackListApiView.as_view('rack_list'),
    ),

    url(
        method='POST',
        path='/racks/',
        handler=server_views.RackCreateApiView.as_view('rack_post'),
    ),

    url(
        method='GET',
        path=f'/racks/<int:rack_id>/',
        handler=server_views.RackDetailApiView.as_view('rack_detail'),
    ),

    url(
        method='PATCH',
        path=f'/racks/<int:rack_id>/',
        handler=server_views.RackPatchApiView.as_view('rack_patch'),
    ),

    url(
        method='PUT',
        path=f'/racks/<int:rack_id>/',
        handler=server_views.RackUpdateApiView.as_view('rack_update'),
    ),
)
