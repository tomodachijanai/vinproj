import wx
import sys, os
from contextlib import contextmanager
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

with suppress_stdout():
    from VoiceChanger import Voice_changer
    from pygame import mixer as m

class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title)
        
        m.init()
        self.VChanger = Voice_changer()
        self.playing = False
        self.InitUI()
        self.Centre()
        

    def InitUI(self):
        self.SetMinClientSize(wx.Size(169, 206))
        self.SetMaxClientSize(wx.Size(300, 206))
        self.CreateStatusBar()
        filemenu= wx.Menu()

        menuRecord = filemenu.Append(wx.ID_ANY,"&Record"," Record voice")
        filemenu.AppendSeparator()
        menuAbout = filemenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        filemenu.AppendSeparator()
        menuExit = filemenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)

        vbox = wx.BoxSizer(wx.VERTICAL)
        self.octTC = wx.TextCtrl(self, style=wx.TE_LEFT)
        self.nTC = wx.TextCtrl(self, style=wx.TE_LEFT)
        k = self.octTC.GetFont()
        k.SetPointSize(28)
        self.octTC.SetFont(k)
        self.nTC.SetFont(k)
        k.SetPointSize(36)
        self.playBut = wx.Button(self, label="&Play")
        self.playBut.SetFont(k)
        self.playBut.Disable()
        self.playBut.SetToolTip("Play recorded audio")
        self.chOctBut = wx.Button(self, label="Change &octave")
        self.chOctBut.SetFont(k)
        self.chOctBut.Disable()
        self.chOctBut.SetToolTip("Change current recording's octave")
        self.timer = wx.Timer(self)
        hbox = wx.BoxSizer()
        hbox.Add(self.octTC, flag=wx.EXPAND | wx.ALIGN_LEFT)# | wx.ALIGN_TOP | wx.ALIGN_BOTTOM )
        hbox.AddStretchSpacer()
        hbox.Add(self.nTC, flag=wx.EXPAND | wx.ALIGN_RIGHT)
        vbox.Add(hbox, flag=wx.EXPAND)
        vbox.AddStretchSpacer()
        vbox.Add(self.playBut, flag=wx.EXPAND )
        vbox.Add(self.chOctBut, flag=wx.EXPAND )
        self.SetSizer(vbox)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.OnRecord, menuRecord)
        self.Bind(wx.EVT_BUTTON, self.OnPlayClick, self.playBut)
        self.Bind(wx.EVT_BUTTON, self.OnChOClick, self.chOctBut)
        self.Bind(wx.EVT_TIMER, self.OnPlayTimer, self.timer)


    def OnRecord(self,e):
        self.n = (float(self.nTC.GetLineText(0)) if self.nTC.GetLineText(0).isnumeric() else 3)
        self.octaves = (float(self.octTC.GetLineText(0)) if self.octTC.GetLineText(0).isnumeric() else 1)
        self.VChanger.recognize_from_micro(n=self.n)
        self.recording = m.Sound(self.VChanger.voice_effect(octaves=self.octaves))
        self.playBut.Enable()
        self.chOctBut.Enable()

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "A small voice changing util", "About VoiceChanger", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def OnExit(self,e):
        self.Close(True)  # Close the frame.

    def OnPlayTimer(self,e):
        self.playing = False
        self.playBut.SetLabel("&Play")
        self.playBut.SetToolTip("Play recorded audio")

    def OnChOClick(self,e):
        if self.octTC.GetLineText(0).isnumeric():
            self.octaves = float(self.octTC.GetLineText(0))
            self.recording = m.Sound(self.VChanger.voice_effect(octaves=self.octaves))
            
    def OnPlayClick(self,e): 
        if self.playBut.GetLabel() == "&Play":
            if not self.playing:
                m.Channel(0).play(self.recording)
                self.playing = True
                self.timer.StartOnce(self.n*1000/(2 ** self.octaves)+500)
            else:
                m.Channel(0).unpause()
            self.playBut.SetLabel("&Pause")
            self.playBut.SetToolTip("Pause audio")
        else:
            m.Channel(0).pause()
            self.playBut.SetLabel("&Play")
            self.playBut.SetToolTip("Play recorded audio")





def main():
    app = wx.App()
    win = MainWindow(None, "VoiceChanger")
    win.Show()
    app.MainLoop()


if __name__ == "__main__":
    with suppress_stdout():
        main()