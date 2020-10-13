from werkzeug.routing import Map, Rule, NotFound, RequestRedirect
import dash
import dash_html_components as html
import dash_core_components as dcc


class Router:
    def __init__(self, server_name='', layout=None, loading=None, not_found=None):
        self.server_name = server_name
        self.url_map = Map()
        self.view_functions = {}
        self._set_default_templates(layout, loading, not_found)

    def _set_default_templates(self, layout, loading, not_found):
        if layout is None:
            self.layout = html.Div([
                dcc.Location(id='url', refresh=False),
                html.Div(id='page-content'),
            ])
        else:
            self.layout = layout
        if loading is None:
            self.loading = 'Loading...'
        else:
            self.loading = loading
        if not_found is None:
            self.not_found = html.Div([
                html.P(["404 Page not found"])
            ], className="no-page")
        else:
            self.not_found = not_found

    def __str__(self):
        return str(self.url_map)

    def __repr__(self):
        return repr(self.url_map)

    def register_callbacks(self, dashapp):
        # Helper that includes basic layout and wires up callback
        dashapp.layout = self.layout
        @dashapp.callback(
            dash.dependencies.Output('page-content', 'children'),
            [dash.dependencies.Input('url', 'pathname')]
        )
        def display_page(pathname):
            return self.dispatch(pathname)        

    def dispatch(self, path, **kwargs):
        if path is None:
            return self.loading
        ma = self.url_map.bind(server_name=self.server_name)        
        try:
            endpoint, kwards = ma.match(path)
            return self.view_functions[endpoint](**kwards, **kwargs)
        except NotFound:
            return self.not_found

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