from django.test import TestCase

from frontend.models import Banner, ContentTranslate


class FrontendTestCase(TestCase):
    def setUp(self):
        Banner.objects.create(name="hello")
        ContentTranslate.objects.create(lang="en", tag_data="Hello", tag_value="halo")

    def test_data_banner(self):
        banner = Banner.objects.all()
        self.assertEqual(banner.count(), 1)

    def test_translate_content(self):
        content_translate = ContentTranslate.objects.all()
        self.assertEqual(content_translate.count(), 1)
