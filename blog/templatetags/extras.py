from django.template.defaulttags import register

# necessary to register every function written (abstracted away)
@register.filter
def get_item(dictionary, key):
    # get returns 'None' when something is not found
    return dictionary.get(key)