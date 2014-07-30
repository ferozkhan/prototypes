
from django.core.urlresolvers import resolve
from django.test import TestCase
from prototypes.app.views import prototype_listing


class HomePageViewTest(TestCase):

    def test_prototypes_url_resolves_to_prototype_listing(self):
        resolved = resolve('/prototypes/')
        self.assertEqual(resolved.func, prototype_listing)
