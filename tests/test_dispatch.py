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

        resp = router.dispatch('/report/monthly')
        self.assertIn('404', resp.children[0].children[0], 'Should have thrown a 404')
     
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
        
        resp = router.dispatch('/annual/section_b/full-view')
        self.assertIn('404', resp.children[0].children[0], 'Should have thrown a 404')


if __name__ == '__main__':
    unittest.main()