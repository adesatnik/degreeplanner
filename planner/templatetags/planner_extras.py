from django import template

register = template.Library()

@register.simple_tag
def tabtimes(number):
    try:
        times = int(number)
    except:
        times = 0
    space = ""
    for i in range(0,times*4):
        space = space + "&nbsp;"
    
    
    return space
        
    

    

    