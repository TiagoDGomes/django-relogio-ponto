from core.templatetags import register
@register.filter
def next_item(value, arg):
    try:
        return value[int(arg)+1]
    except:
        return None
@register.filter    
def prev_item(value, arg):
    try:
        return value[int(arg)-1]
    except:
        return None