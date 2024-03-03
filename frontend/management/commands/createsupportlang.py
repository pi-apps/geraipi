from deep_translator import GoogleTranslator
from django.core.management.base import BaseCommand

from profiles.models import LangSupport


class Command(BaseCommand):
    help = "Import and insert langsupport"

    def handle(self, *args, **options):
        LangSupport.objects.all().delete()
        translate_lang = GoogleTranslator().get_supported_languages(as_dict=True)
        for tl in translate_lang:
            lang_codes = translate_lang[tl]
            langs = tl
            print(tl)
            LangSupport.objects.create(code=lang_codes, alias=langs)
