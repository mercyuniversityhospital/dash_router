import unittest
from .context import dash_router
from werkzeug.routing import NotFound


class TestRouter(unittest.TestCase):
    def test_decorator(self):
        router = dash_router.Router()

        @router.route('/report/monthly/<section>')
        @router.route('/report/monthly/<section>/full-view')
        def monthly(section, fullview=None):
            return 'monthly', section, fullview

        @router.route('/report/annual')
        @router.route('/report/annual/full-view')
        def annual(fullview=None):    
            return 'annual', fullview

        try:
            router.dispatch('/report/monthly')
            self.fail('Should have thrown a 404')
        except NotFound:
            pass            
     
        self.assertEqual(
            router.dispatch('/report/monthly/sectiona'), 
            ('monthly', 'sectiona', None)
        )
        
        self.assertEqual(
            router.dispatch('/report/annual'),
            ('annual', None)
        )        
        self.assertEqual(
            router.dispatch('/report/annual/full-view'),
            ('annual', None)
        )
        
        try:
            router.dispatch('/annual/section_b/full-view')
            self.fail('Should have thrown a 404')
        except NotFound:
            pass


if __name__ == '__main__':
    unittest.main()