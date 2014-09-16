#!/usr/bin/env python2
from gi.repository import Gtk, GLib, GObject
from query import url, retrieve_result, opener
import threading

class SimpleTextWindow(Gtk.Window):
    def __init__(self,file_name):
        Gtk.Window.__init__(self,title = file_name)
        self.box = Gtk.Box(orientation = Gtk.Orientation.VERTICAL,spacing = 6)
        self.add(self.box)
        self.scrolledWindow = Gtk.ScrolledWindow()
        self.scrolledWindow.set_hexpand(True)
        self.scrolledWindow.set_vexpand(True)
        self.box.pack_start(self.scrolledWindow,True,True,0)

        self.textview = Gtk.TextView()
        self.scrolledWindow.add(self.textview)
        self.textbuffer = self.textview.get_buffer()
        fin = open(file_name, 'r') # reading contents of file
        file_data = fin.read()
        fin.close()
        self.textbuffer.set_text(file_data)

        self.hbox = Gtk.Box(spacing = 10)
        self.quitButton = Gtk.Button(label="quit")
        self.saveButton = Gtk.Button(label = "save")
        self.quitButton.connect("clicked",self.quit)
        self.saveButton.connect("clicked",self.save_file,file_name)
        self.hbox.pack_start(self.quitButton,True,True,0)
        self.hbox.pack_start(self.saveButton,True,True,0)
        self.box.pack_start(self.hbox,True,True,0)

    def save_file(self,widget,file_name):
        fout = open(file_name,'w')
        file_data = self.textbuffer.get_text(self.textbuffer.get_start_iter(),
            self.textbuffer.get_end_iter(), True)
        fout.write(file_data)
        fout.close()
        return None
    def quit(self,widget):
        self.destroy()
        return None

class GenerateRegnoLst(Gtk.Window):

    def __init__(self,file_name):
        Gtk.Window.__init__(self, title = "Generate Register Number List")
        self.box =  Gtk.Box(orientation = Gtk.Orientation.VERTICAL,spacing = 10)
        self.add(self.box)
        self.hbox1 = Gtk.Box(spacing = 5)
        self.lblCommon = Gtk.Button(label = "Common part of RegNo")
        self.txtEntryCommon = Gtk.Entry()
        self.hbox1.pack_start(self.lblCommon,True,True,0)
        self.hbox1.pack_start(self.txtEntryCommon,True,True,0)

        self.hbox2 = Gtk.Box(spacing = 5)
        self.hbox3 = Gtk.Box(spacing = 5)
        self.lblStart = Gtk.Button(label = "Start")
        self.lblEnd = Gtk.Button(label = "End")
        self.txtEntryStart = Gtk.Entry()
        self.txtEntryEnd = Gtk.Entry()
        self.hbox2.pack_start(self.lblStart,True,True,0)
        self.hbox2.pack_start(self.txtEntryStart,True,True,0)
        self.hbox3.pack_start(self.lblEnd,True,True,0)
        self.hbox3.pack_start(self.txtEntryEnd,True,True,0)

        self.box.pack_start(self.hbox1,True,True,0)
        self.box.pack_start(self.hbox2,True,True,0)
        self.box.pack_start(self.hbox3,True,True,0)
        self.hbox4 = Gtk.Box(spacing = 10)
        self.quitButton = Gtk.Button(label="quit")
        self.generateButton = Gtk.Button(label = "Generate")
        self.quitButton.connect("clicked",self.quit)
        self.generateButton.connect("clicked",self.generate_file,file_name)
        self.hbox4.pack_start(self.quitButton,True,True,0)
        self.hbox4.pack_start(self.generateButton,True,True,0)
        self.box.pack_start(self.hbox4,True,True,0)

    def quit(self,widget):
        self.destroy()
        return None

    def generate_file(self,widget,file_name):
        comm = self.txtEntryCommon.get_text()
        start = int(self.txtEntryStart.get_text())
        end = int(self.txtEntryEnd.get_text())
        try:
            fout = open(file_name,'w')
            for i in range(start,end+1):
                fout.write('%s%02d\n' % (comm,i))
            fout.close()
        except:
            print('Some Error has occured when writing file')
        dialog =Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
        Gtk.ButtonsType.OK, 'File %s generated successfully' % file_name)
        dialog.run()
        dialog.destroy()
        self.destroy()
        return None


class ResultScrapMainWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title = "pondiuni.edu.in ResultScrapper")

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(10)
        self.grid.set_row_spacing(5)
        self.grid.margin = 15
        self.add(self.grid)
        self.create_widgets()
        self.pack_widgets()
        self.connect_callbacks()
        self.file_name = ""
        self.output_dir = ""

    def create_widgets(self):
        self.label1 = Gtk.Label(label = "Input RegisterNumber List")
        self.fileNameTxtEntry = Gtk.Entry()
        self.btnChooseFile = Gtk.Button(label="...")
        self.btnListPreview = Gtk.Button(label="preview")
        self.btnListGenerate = Gtk.Button(label="generate")
        self.lblDept = Gtk.Label(label = "Dept.")
        depts = ['Select Department','BTECH','BTHCS','BTHIT','BTHEC']
        self.comboBoxDept = Gtk.ComboBoxText.new_with_entry()
        for dept in depts:
            self.comboBoxDept.append_text(dept)
        self.lblSemester = Gtk.Label(label = "Sem.")
        sems = ['1','2','3','4','5','6','7','8']
        self.comboBoxSemester = Gtk.ComboBoxText()
        for sem in sems:
            self.comboBoxSemester.append_text(sem)
        self.label2 = Gtk.Label(label = "Choose Output Directory")
        self.outDirTxtEntry = Gtk.Entry()
        self.btnChooseOutDir = Gtk.Button(label="...")
        self.btnStart = Gtk.Button(label= "Start")
        self.btnStop = Gtk.Button(label = "Stop")
        self.progressBar = Gtk.ProgressBar()
        self.progressBar.set_show_text(True)
        return None

    def pack_widgets(self):
        self.grid.attach(self.label1,0,0,4,1)
        self.grid.attach(self.fileNameTxtEntry,0,1,3,1)
        self.grid.attach(self.btnChooseFile,3,1,1,1)
        self.grid.attach(self.btnListGenerate,1,2,1,1)
        self.grid.attach(self.btnListPreview,2,2,2,1)
        self.grid.attach(self.lblDept,0,3,1,1)
        self.grid.attach(self.comboBoxDept,1,3,1,1)
        self.grid.attach(self.comboBoxSemester,3,3,1,1)
        self.grid.attach(self.lblSemester,2,3,1,1)
        self.grid.attach(self.label2,0,4,4,1)
        self.grid.attach(self.outDirTxtEntry,0,5,3,1)
        self.grid.attach(self.btnChooseOutDir,3,5,1,1)
        self.grid.attach(self.btnStart,0,6,2,1)
        self.grid.attach(self.btnStop,2,6,2,1)
        self.grid.attach(self.progressBar,0,7,4,1)
        return None

    def connect_callbacks(self):
        self.btnChooseFile.connect("clicked",self.choose_input_file)
        self.btnChooseOutDir.connect("clicked",self.choose_output_folder)
        self.btnListPreview.connect("clicked",self.priview_regno_lst)
        self.btnListGenerate.connect("clicked",self.generate_regno_lst)
        self.btnStart.connect("clicked",self.start_retrive)
        self.btnStop.connect("clicked",self.stop_retrive)
        return None

    def choose_input_file(self,widget):
        dialog = Gtk.FileChooserDialog("Please choose registerlist file",self,
        Gtk.FileChooserAction.OPEN,
        (Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN,Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.file_name = dialog.get_filename()
            self.fileNameTxtEntry.set_text( self.file_name)
        dialog.destroy()
        return None

    def choose_output_folder(self,widget):
        dialog = Gtk.FileChooserDialog("Choose Dir where HTML to be saved",self,
        Gtk.FileChooserAction.SELECT_FOLDER,
        (Gtk.STOCK_CANCEL,Gtk.ResponseType.CANCEL,
        'Select',Gtk.ResponseType.OK))

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.output_dir = dialog.get_filename()
            self.outDirTxtEntry.set_text( self.output_dir)
        dialog.destroy()
        return None


    def priview_regno_lst(self,widget):
        self.file_name = self.fileNameTxtEntry.get_text()
        if self.file_name == "":
            print('Choose a file Before viewing it')
            return None
        textviewer = SimpleTextWindow(self.file_name)
        textviewer.show_all()
        return None

    def generate_regno_lst(self,widget):
        self.file_name = self.fileNameTxtEntry.get_text()
        if self.file_name == "":
            print('Choose a file to store generated register nos')
            return None
        generate_regno_window = GenerateRegnoLst(self.file_name)
        generate_regno_window.show_all()
        return None

    def start_retrive(self, widget):
        self.file_name = self.fileNameTxtEntry.get_text()
        if self.file_name == "":
            print('Choose file containing list of register nos')
            return None
        else:
            fin = open(self.file_name, 'r')
            self.lstregno = (fin.read()).split()
            self.dept_id = self.comboBoxDept.get_active_text()
            self.sem = self.comboBoxSemester.get_active_text()
            self.thread = threading.Thread(target = self.retrieve_results)
            self.thread.daemon = True
            #self.retrivingThread = RetriveThread(lstregno, dept_id, sem, self,
            #                        self.out_dir)
            try:
                self.stop_flag = False
                self.thread.start()
                #self.retrivingThread.start()
                #self.retrivingThread.join()
            except:
                print('Some Error has occurred in Retriving results from internet')
        return None

    def stop_retrive(self, widget):
        self.stop_flag = True
        self.progressBar.set_fraction(0.0)
        self.progressBar.set_text('Nothing in Progress')
        return None

    def retrieve_results(self):
        for regno, i in zip(self.lstregno, range(len(self.lstregno))):
            if self.stop_flag == True :
               return None
            if retrieve_result(regno, self.dept_id, self.sem, url, opener,
                        self.output_dir) != None :
                raise Exception('Some Error Occured')
            else:
                fraction = (i / float(len(self.lstregno)))
                GLib.idle_add(self.update_progressbar, fraction, regno)
        return None

    def update_progressbar(self, fraction, regno):
        #print(fraction)
        self.progressBar.set_fraction(fraction)
        self.progressBar.set_text('%s is processed' % regno)
        if self.stop_flag == True:
            self.progressBar.set_fraction(0.0)
            self.progressBar.set_text('Nothing in Progress')
        return None


#class RetriveThread(threading.Thread):
#    def __init__(self, lstregno, dept_id, sem, scrapWindow, output_dir):
#        threading.Thread.__init__(self)
#        self.lstregno = lstregno
#        self.dept_id = dept_id
#        self.sem = sem
#        self.scrapWindow = scrapWindow
#        self.output_dir = output_dir

#    def run(self):
#        for regno, i in zip(self.lstregno, range(len(self.lstregno))):
#            if retrieve_result(regno, self.dept_id, self.sem, url, opener,
#                        self.output_dir) != None :
#                raise Exception('Some Error Occured')
#            else:
#                fraction = (i / len(self.lstregno))
#                self.scrapWindow.progressBar.set_fraction(fraction)
#                self.scrapWindow.progressBar.set_text('%s is processed' % regno)

def app_main():
    window = ResultScrapMainWindow()
    window.connect("delete-event",Gtk.main_quit)
    window.show_all()

if __name__ == "__main__":
    GObject.threads_init()
    app_main()
    Gtk.main()

