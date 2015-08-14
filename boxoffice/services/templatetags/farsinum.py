from django.template import Library

register = Library()

@register.filter
def farsi_num( value ):

  en_2_fa = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}

  farsi_num = ''
  for i in str(value):
      farsi_num += en_2_fa[i]

  return farsi_num