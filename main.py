#!/usr/bin/python
# -*- coding: utf-8 -*-
import query
from gi.repository import Gtk
class GUI:
    #this call back calls query.py with parametrs
    def on_retrieve_button_click(self,widget,Data=None):
        self.regno_common = self.comm_name_text_entry.get_text()
        self.start_no = self.start_no_text_entry.get_text()
        self.end_no=self.end_no_text_entry.get_text()
        self.dept_id=self.dept_combo_box.get_active_text()
        self.sem_no=self.sem_combo_box.get_active_text()
        self.sem_no=chr(int(self.sem_no)+64)
        for number in range(int(self.start_no),int(self.end_no)+1):
            query.retrieve_result(self.regno_common,number,self.dept_id,self.sem_no,query.url,query.opener)
    #Call back functions for closing the window
    def destroy(widget,data=None):
        Gtk.main_quit()
    def delete_event(widget, event, data=None):
        return False

    def __init__(self):
        #using gtk builder to get objects from UI files
        self.builder = Gtk.Builder()
        self.builder.add_from_file('main.glade')
        self.main_window = self.builder.get_object('window')
        self.retrieve_button = self.builder.get_object('button1')
        self.comm_name_text_entry = self.builder.get_object('reg_entry')
        self.start_no_text_entry = self.builder.get_object('entry1')
        self.end_no_text_entry = self.builder.get_object('entry2')
        self.dept_combo_box = self.builder.get_object('combobox1')
        self.sem_combo_box = self.builder.get_object('combobox2')

        #connecting windows delete_event
        self.main_window.connect("delete_event", self.delete_event)
        self.main_window.connect("destroy", self.destroy)

        #connecting retrieve_button,to a function
        self.retrieve_button.connect("clicked",self.on_retrieve_button_click,None)
        self.main_window.show_all()
    def main(self):
        Gtk.main()
if __name__ == '__main__':
    gui = GUI()
    gui.main()


