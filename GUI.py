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
    import pydub.playback as pb
    import pydub as pd
    from VoiceChanger import Voice_changer
    from pygame import mixer as m

class MainWindow(wx.Frame):

    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title)
        
        self.VChanger = Voice_changer()
        self.playing = False
        self.InitUI()
        self.Centre()
        

    def InitUI(self):
        self.SetMinClientSize(wx.Size(300, 300))
        self.SetMaxClientSize(wx.Size(300, 300))
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
        self.octTC = wx.TextCtrl(self)
        self.nTC = wx.TextCtrl(self)
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
        k.SetPointSize(30)
        self.chOctBut.SetFont(k)
        self.chOctBut.Disable()
        self.chOctBut.SetToolTip("Change current recording1's octave")
        self.timer = wx.Timer(self)
        hbox = wx.BoxSizer()
        hbox.Add(self.octTC, flag=wx.EXPAND)# | wx.ALIGN_TOP | wx.ALIGN_BOTTOM )
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
        try:
            self.n = float(self.nTC.GetLineText(0))
        except ValueError:
            self.n = 3
        try:
            self.tones = list(map(float, self.octTC.GetLineText(0).split()))
        except ValueError:
            self.tones = [0, 4]
        self.VChanger.recognize_from_micro(n=self.n)
        sr = self.VChanger.voice_effect(tones=self.tones)
        # if not m.get_init():
        #     m.init(sr)
        self.playBut.Enable()
        self.chOctBut.Enable()
        # self.recording1 = m.Sound("sounds.mp3")
        # self.recording2 = m.Sound("male.wav")
        dlg = wx.MessageDialog(self, "Finished recording and processing", "Recording", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy()

    def OnAbout(self,e):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        print(self.GetSize())
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
        try:
            self.tones = list(map(float, self.octTC.GetLineText(0).split()))
            self.VChanger.voice_effect(tones=self.tones)
            # self.recording1 = m.Sound("sounds.mp3")
            # self.recording2 = m.Sound("male.wav")
            dlg = wx.MessageDialog(self, "Octave changing is finished", "Octave changing", wx.OK)
            dlg.ShowModal() # Show it
            dlg.Destroy()
        except ValueError:
            pass

    def OnPlayClick(self,e):
        pb.play(pd.AudioSegment.from_file("sounds.wav"))
        if False:
            if self.playBut.GetLabel() == "&Play":
                if not self.playing:
                    m.Channel(0).play(self.recording1)
                    # m.Channel(1).play(self.recording2)
                    self.playing = True
                    self.timer.StartOnce(self.n*1000+500)
                else:
                    m.Channel(0).unpause()
                    # m.Channel(1).unpause()
                self.playBut.SetLabel("&Pause")
                self.playBut.SetToolTip("Pause audio")
            else:
                m.Channel(0).pause()
                # m.Channel(1).pause()
                self.playBut.SetLabel("&Play")
                self.playBut.SetToolTip("Play recorded audio")





def main():
    app = wx.App()
    win = MainWindow(None, "VoiceChanger")
    win.Show()
    app.MainLoop()


if __name__ == "__main__":
    # with suppress_stdout():
    main()