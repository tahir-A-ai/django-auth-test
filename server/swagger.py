from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from django.utils.safestring import mark_safe


class CustomSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.security_definitions = {
            'Bearer': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'Authorization',
                'description': 'Paste your token below (Bearer will be auto-added)',
            }
        }
        schema.security = [{'Bearer': []}]
        return schema


schema_view = get_schema_view(
    openapi.Info(
        title="python swagger collection",
        default_version='v1',
        contact=openapi.Contact(email="ta@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    generator_class=CustomSchemaGenerator,
)

# Custom Swagger UI HTML with JS to auto-add 'Bearer '
swagger_ui_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Swagger UI</title>
    <link href="https://unpkg.com/swagger-ui-dist@3/swagger-ui.css" rel="stylesheet">
</head>
<body>
<div id="swagger-ui"></div>
<script src="https://unpkg.com/swagger-ui-dist@3/swagger-ui-bundle.js"></script>
<script>
    window.onload = function () {
        const ui = SwaggerUIBundle({
            url: '/swagger.json',
            dom_id: '#swagger-ui',
            presets: [SwaggerUIBundle.presets.apis],
            layout: "BaseLayout",
            requestInterceptor: function (req) {
                if (req.loadSpec) return req;
                const token = req.headers.Authorization;
                if (token && !token.startsWith('Bearer ')) {
                    req.headers.Authorization = 'Bearer ' + token;
                }
                return req;
            }
        });
    };
</script>
</body>
</html>
"""

from django.http import HttpResponse

def custom_swagger_ui(request):
    return HttpResponse(swagger_ui_html)


swagger_urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', custom_swagger_ui, name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0),
         name='schema-redoc'),
]