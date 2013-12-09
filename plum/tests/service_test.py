from plum import Service
from .testcases import ServiceTestCase


class NameTestCase(ServiceTestCase):
    def test_name_validations(self):
        self.assertRaises(ValueError, lambda: Service(name=''))

        self.assertRaises(ValueError, lambda: Service(name=' '))
        self.assertRaises(ValueError, lambda: Service(name='/'))
        self.assertRaises(ValueError, lambda: Service(name='!'))
        self.assertRaises(ValueError, lambda: Service(name='\xe2'))

        Service('a')
        Service('foo')
        Service('foo_bar')
        Service('__foo_bar__')
        Service('_')
        Service('_____')


class ContainersTestCase(ServiceTestCase):
    def test_containers(self):
        foo = self.create_service('foo')
        bar = self.create_service('bar')

        foo.start()

        self.assertEqual(len(foo.containers), 1)
        self.assertEqual(foo.containers[0]['Names'], ['/foo_1'])
        self.assertEqual(len(bar.containers), 0)

        bar.scale(2)

        self.assertEqual(len(foo.containers), 1)
        self.assertEqual(len(bar.containers), 2)

        names = [c['Names'] for c in bar.containers]
        self.assertIn(['/bar_1'], names)
        self.assertIn(['/bar_2'], names)


class ScalingTestCase(ServiceTestCase):
    def setUp(self):
        super(ServiceTestCase, self).setUp()
        self.service = self.create_service("scaling_test")

    def test_up_scale_down(self):
        self.assertEqual(len(self.service.containers), 0)

        self.service.start()
        self.assertEqual(len(self.service.containers), 1)

        self.service.start()
        self.assertEqual(len(self.service.containers), 1)

        self.service.scale(2)
        self.assertEqual(len(self.service.containers), 2)

        self.service.scale(1)
        self.assertEqual(len(self.service.containers), 1)

        self.service.stop()
        self.assertEqual(len(self.service.containers), 0)

        self.service.stop()
        self.assertEqual(len(self.service.containers), 0)


class LinksTestCase(ServiceTestCase):
    def test_links_are_created_when_starting(self):
        db = self.create_service('db')
        web = self.create_service('web', links=[db])
        db.start()
        web.start()
        self.assertIn('/web_1/db_1', db.containers[0]['Names'])
        db.stop()
        web.stop()

