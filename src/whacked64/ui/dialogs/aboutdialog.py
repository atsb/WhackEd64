#!/usr/bin/env python
#coding=utf8

"""
Generic about dialog interface.
"""

from whacked64 import config
from whacked64.ui import windows
import wx


class AboutDialog(windows.AboutDialogBase):

    def __init__(self, parent):
        windows.AboutDialogBase.__init__(self, parent)

        self.SetEscapeId(windows.ABOUT_OK)

        self.Version.SetLabel('Version ' + config.APP_VERSION)

        with open('LICENSE', 'r') as f:
            self.license_text = f.read()

    def ok(self, event):
        self.EndModal(0)

    def license(self, event):
        wx.MessageBox(message=self.license_text, caption='License', style=wx.OK, parent=self)
