#!/usr/bin/env python
#coding=utf8

import webbrowser
import os

from whacked64 import config
from whacked64.ui import windows


class StartDialog(windows.StartDialogBase):
    """
    This dialog is meant to be displayed on startup of the application. It allows the user to quickly
    access some common functions without having to dig down into a menu first.
    """

    def __init__(self, parent):
        windows.StartDialogBase.__init__(self, parent)

        self.SetEscapeId(windows.START_CANCEL)

        client_width = self.FileList.GetClientSize()[0] - 4
        self.FileList.InsertColumn(0, 'Filename', width=client_width)

        # Populate the list of recently accessed Dehacked patches.
        config.settings.recent_files_clean()
        recent_files = config.settings['recent_files']
        for index, filename in enumerate(recent_files):
            self.FileList.InsertItem(index, filename)

    def open_file_list(self, event):
        """
        Opens a Dehacked patch directly from the file list.
        """

        self.EndModal(0)
        filename = config.settings['recent_files'][event.GetIndex()]
        self.GetParent().open_file(filename)

    def new_file(self, event):
        self.EndModal(0)
        self.GetParent().new_file()

    def open_file(self, event):
        self.EndModal(0)
        self.GetParent().open_file_dialog()

    def cancel(self, event):
        self.EndModal(0)

    def help(self, event):
        file = 'file://' + os.path.join(os.getcwd(), 'docs/index.html')
        webbrowser.open(file)
