from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
import dash
import dash_html_components as html
import dash_core_components as dcc


class Router:
    def __init__(self, server_name=''):
        self.server_name = server_name
        self.url_map = Map()
        self.view_functions = {}

    def __str__(self):
        return str(self.url_map)

    def __repr__(self):
        return repr(self.url_map)

    def register_callbacks(self, dashapp):
        # Helper that includes basic layout and wires up callback
        dashapp.layout = html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content'),
        ])
        @dashapp.callback(
            dash.dependencies.Output('page-content', 'children'),
            [dash.dependencies.Input('url', 'pathname')]
        )
        def display_page(pathname):
            return self.dispatch(pathname)        

    def dispatch(self, path):
        if path is None:
            return 'Loading...'        
        ma = self.url_map.bind(server_name=self.server_name)
        endpoint, kwards = ma.match(path)
        return self.view_functions[endpoint](**kwards)

    def add_url_rule(self, rule, endpoint=None, view_func=None, **options):
        if endpoint is None:
            endpoint = view_func.__name__
        options["endpoint"] = endpoint 
        methods = ("GET", "POST")

        rule = Rule(rule, methods=methods, **options)
        self.url_map.add(rule)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError(
                    "View function mapping is overwriting an "
                    "existing endpoint function: %s" % endpoint
                )        
            self.view_functions[endpoint] = view_func

    def route(self, rule, **options):
        def decorator(f):
            endpoint = options.pop("endpoint", None)
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator