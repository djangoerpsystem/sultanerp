#context_processors.py

from sultanerp.models import DynamicText

# # with looping
# def dynamic_text_processor(request):
#     dynamic_texts = DynamicText.objects.all()
#     return {'dynamic_texts': dynamic_texts}

# without looping, works as expected
def dynamic_text_processor(request):
    dynamic_texts_objects = DynamicText.objects.all()
    dynamic_texts_dict = {dt.title: dt for dt in dynamic_texts_objects}
    return {'dynamic_texts': dynamic_texts_dict}
