from deep_translator import GoogleTranslator

from frontend.models import ContentTranslate


def translater(translate_to, page, values):
    content = ContentTranslate.objects.all()
    if translate_to:
        if content.count() > 0:
            content = content.filter(lang=translate_to, tag_data=page)
    content = content.first()
    if not content:
        translator = GoogleTranslator("auto", translate_to).translate(values)
        content = ContentTranslate()
        content.lang = translate_to
        content.tag_data = page
        content.tag_value = translator
        content.save()
    return content.tag_value
