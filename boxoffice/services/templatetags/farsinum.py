from django.template import Library

register = Library()

@register.filter
def farsi_num( value ):

  en_2_fa = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}

  farsi_num = ''
  for i in str(value):
    if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9':
      farsi_num += en_2_fa[i]
    else:
      farsi_num += i

  return farsi_num