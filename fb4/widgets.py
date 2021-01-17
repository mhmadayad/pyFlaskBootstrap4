'''
Created on 2021-01-04

@author: wf
'''
from flask import render_template_string

class Widget(object):
    '''
    a HTML widget
    '''
    def __init__(self,indent=""):
        self.indent=indent
        pass
    
    def __str__(self):
        html=self.render()
        return html

class Link(Widget):   
    '''
    a HTML link
    '''
    def __init__(self,url,title,tooltip=None,indent=""):
        '''
        constructor
        
        Args:
            url(str):  the link 
            title(str): the title
            tooltip(str): the tooltip (if any)
        '''
        super().__init__(indent=indent)
        self.url=url
        self.title=title
        self.tooltip=tooltip
        
    def render(self):
        html="%s<a href='%s' title='%s'>%s</a>" % (self.indent,self.url,self.tooltip,self.title)
        return html
        
class Image(Widget):
    '''
    a HTML Image
    '''
    def __init__(self,url,alt=None,title=None,width=None,height=None,indent=""):
        '''
        constructor
        
        Args:
            url(str):  the link 
            alt(str):  alternative image representation (if any)
            title(str): title/tooltip (if any)
            width: width of the image (if any)
            height: height of the image (if any)
        '''
        super().__init__(indent=indent)
        self.url=url
        if alt is not None:
            self.alt=alt
        else:
            self.alt=url
        self.title=title
        self.width=width
        self.height=height
        
    def render(self):
        '''
        render me
        
        Returns:
            str: html code for Image
        '''
        width=" width='%d'" % self.width if self.width is not None else ""
        height=" height='%d'" % self.height if self.height is not None else ""
        title=" title='%s'" % self.title if self.title is not None else ""
        html="%s<img src='%s' alt='%s'%s%s%s/>" % (self.indent,self.url,self.alt,title,width,height)
        return html
    
class Icon(Widget):
    ''' 
    an Icon
    '''
    
    def __init__(self,name:str,size='32',color:str='primary',iconType:str='bootstrap'):
        '''
        constructor
        '''
        self.name=name
        self.size=str(size)
        self.color=color
        self.iconType=iconType
        pass
    
    def render(self)->str:
        '''
        render me as html
        
        Returns:
            str: html code for Icon
        '''
        # https://icons.getbootstrap.com/icons/ is the default
        template="""
{%% from 'bootstrap/utils.html' import render_icon %%}        
{{ render_icon('%s', %s,'%s') }}""" % (self.name,self.size,self.color)
        html=render_template_string(template)
        return html    
    
class MenuItem(Widget):
    '''
    a menu item
    '''
    
    def __init__(self,url:str,title:str,active:bool=False,indent=""):
        '''
        constructor
        
        Args:
            url(str):  the link
            title(str): the title of the menu item
            active(bool): whether the link is initially active 
        '''
        super().__init__(indent=indent)
        self.url=url
        self.title=title
        self.active=active
    
    def render(self):
        '''
        render me
        
        Returns:
            str: html code for MenuItem
        '''
        activeState='active' if self.active else ''
        html='''%s<li class="nav-item %s">
%s  <a class="nav-link" href="%s">%s</a>
%s</li>''' % (self.indent,activeState,self.indent,self.url,self.title,self.indent)
        return html