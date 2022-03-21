"""
For correct work needed custom_select.css
css base on Bootstrap4

For example, on classes:
for select_item in document.select(".brython-select"):
    BrythonSelect(select_item)

or element id:
BrythonSelect(document['your_id'])


"""

from browser import document, html, window


class BrythonSelect():

    default_value_trigger = "Выберите из списка"

    def __init__(self, target, live_search=True, max_options=4):
        self.target = target
        self.initUIComponent()
        self.render_target()
        self.live_search = live_search
        self.max_options = max_options
        self.selectedIndex = self.target.selectedIndex
        self.multiselectable = self.target.multiple
        self.update_tigger()
        self.render()
        self.register_events()
        
    def initUIComponent(self):
        self.main_div = html.DIV(Class="select sm")
        self.dropdown = html.DIV(html.DIV(Class="dropdown__inner"), Class='select__dropdown')
        self.trigger = html.BUTTON(html.DIV(self.default_value_trigger, Class='trigger_inner'), 
            Class='btn select__trigger', **{'data-select': 'trigger'})
        self.listbox = html.UL(Class="select__items")
        self.search = html.INPUT(Class='form-control', type="search")
        self.backdrop = html.DIV(Class='select__backdrop', **{'data-select': 'backdrop'})
        
    def _cut_text_trigger(self, text):
        pass

    def update_tigger(self):
        text = ""
        sel_options = [item for item in self.target.options if item.selected]
        if len(sel_options) > self.max_options:
            text = f"Выбрано {len(sel_options)} позиций"
        else:
            for item in sel_options:
                if text:
                    text += "; " + item.text
                else:
                    text = item.text
        if text:
            self.trigger.select_one(".trigger_inner").text = text
            self.trigger.select_one(".trigger_inner").attrs["title"] = text
        else:
            self.trigger.select_one(".trigger_inner").text = self.default_value_trigger

    def register_events(self):

        self.trigger.bind('click', self.toogle)
        self.listbox.bind('click', self.change_value)
        self.backdrop.bind('click', self.toogle)
        self.search.bind('input', self.apply_filter)
    
    def render_target(self):
        self.target.parent.insertBefore(self.main_div, self.target)
        self.main_div.prepend(self.target)
        self.target.style = {"opacity": 0, "position": "absolute"}
        self.target.width = 31
    
    def render(self):
        self.dropdown.prepend(html.DIV(self.search, Class='search'))
        self.dropdown.select_one(".dropdown__inner").append(self.listbox)
        self.main_div <= self.backdrop
        self.main_div <= self.trigger
        self.main_div <= self.dropdown
        
    def apply_filter(self, event):
        event.preventDefault()
        str_search = event.target.value
        self.listbox.html = self._get_listbox(str_search)

    def change_value(self, event):
        item = event.target
        self.set_value_item(item)
        self.update_tigger()
        if not self.multiselectable:
            self.hide_listbox()

    def set_value_item(self, item):
        index = item.attrs.get("data-select")
        if self.multiselectable:
            if item.classList.contains("select__item_selected"):
                item.classList.remove("select__item_selected")
                self.target.options[index].selected = False
                
            else:
                item.classList.add("select__item_selected")
                self.target.options[index].selected = True
        else:
            for prev_item in self.listbox.select(".select__item_selected"):
                prev_item.classList.remove("select__item_selected")
                
            item.classList.add("select__item_selected")
            item.attrs["aria-selected"] = "true"
            self.target.options[index].selected = True
        
    
    def _is_show(self):
        if self.main_div.classList.contains("select_show"):
            return True
        else:
            return False
    
    def toogle(self, event):
        event.preventDefault()
        if self._is_show():
            self.hide_listbox()
        else:
            self.show_listbox()
    
    def _get_height(self, elt, height=0):
        if elt.height == "auto":
            return self._get_height(elt.parent)
        else:
            return elt.height
        
    def _get_dropdown_style(self):

        el_height = self._get_height(self.dropdown)
        search_height = self._get_height(self.search)
        padding = 10

        li_height = len(self.listbox.children) * el_height
        to_bot = window.innerHeight - self.dropdown.scrolled_top - el_height
        if self.dropdown.scrolled_top < to_bot:
            top = el_height - 3
            max_height = to_bot - padding
        else:
            top = -(self.dropdown.scrolled_top - padding)
            max_height = top * -1
        max_height_listbox = max_height - search_height
        dropdown_style = {"max-height": f"{max_height}px",
            "overflow": "hidden",
            "min-height": "162px",
            "position": "absolute",
            "transform": f"translate3d(0px, {top}px, 0px)",
            "top": "1px",
            "left": "0px",
            "will-change": "transform"
                          }
        listbox_style = {"max-height": f"{max_height_listbox}px",
            "overflowY": "auto",
            "min-height": "98px"
                         }
        return dropdown_style, listbox_style

    def show_listbox(self):
        if self.listbox.html == "":
            self.listbox.html = self._get_listbox()
        self.dropdown.style, self.listbox.style = self._get_dropdown_style()
        self.main_div.classList.add("select_show")
        self.dropdown.classList.add("select_show")
        try:
            self.listbox.select('.select__item_selected')[0].focus(preventScroll=False)
        except IndexError:
            pass

    def hide_listbox(self):
        self.dropdown.classList.remove("select_show")
        self.main_div.classList.remove("select_show")
        self.search.value = ""
        self.listbox.html = self._get_listbox()

    
    def _get_listbox(self, str_filter=""):
        li = ''
        for item in self.target.options:
            if str_filter.lower() in item.text.lower():
                li += '<li class="select__item'
                if item.selected:
                    li += ' select__item_selected"' 
                else:
                    li += '"'
                li += f' data-select="{item.index}" tabindex="0">{item.text}</li>'
        return li

    def refresh(self):
        self.listbox.html = ""
