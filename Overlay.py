import wx

########################################################################################
#                                OVERLAY FUNCTIONS                                     #
########################################################################################

class SubtitleFrame(wx.Frame):
    def __init__(self,rc, *args, **kw):
        super(SubtitleFrame, self).__init__(*args, **kw)
        self.rc = rc
        pnl = wx.Panel(self)
        #self.st =  wx.StaticText(pnl, -1, "align center", (100, 50), (160, -1), wx.ALIGN_CENTER)
        padding =20
        self.st = wx.TextCtrl (pnl, -1,  "Betting" , (padding,padding), (self.rc["extensionOfX"]-self.rc["X"]-padding, -1)
        , wx.TE_MULTILINE | wx.TE_NOHIDESEL | wx.TE_READONLY  |  wx.NO_BORDER | wx.TE_NO_VSCROLL | wx.TE_CENTER)
        self.st.SetDefaultStyle(wx.TextAttr(wx.NullColour, wx.LIGHT_GREY))
        self.st.SetBackgroundColour(wx.Colour(0,0,0))
        self.Disable()
        
        font = self.st.GetFont()
        font.PointSize = 20
        font = font.Bold()

        self.st.SetFont(font)
        self.SetSize(wx.Size(self.rc["extensionOfX"]-self.rc["X"], self.rc["extensionOfY"]-self.rc["Y"]))
        #center text
        #self.st.SetPosition(((self.GetSize()[0] - self.st.GetSize()[0])/2, (self.GetSize()[1] - self.st.GetSize()[1])/2))
   
        self.st.SetForegroundColour("White")
        self.SetBackgroundColour(wx.Colour(0,0,0))
        self.SetPosition((self.rc["X"],self.rc["Y"]))
        
        self.SetTransparent( 200 )        
        self.st.Bind(wx.EVT_KEY_UP, self.OnKeyDown)


    # Show Frame and initially call OnHello (use None to compensate for a lack of event)
        self.Show()
        self.SetText("GVT LOADED!")

    def OnKeyDown(self, event):
        """quit if user press q or Esc"""
        if event.GetKeyCode() == 27 or event.GetKeyCode() == ord('Q'): #27 is Esc
            self.Close(force=True)
        else:
            event.Skip()


    #hide the frame
    def HideWindow(self):
        self.SetPosition((10000,10000))
        #self.Close(True)

    def ShowWindow(self):
        self.SetPosition((self.rc["X"],self.rc["Y"]))
    def OnExit(self, event):
        self.Close(True)

    def SetText(self, text):
        self.st.SetLabel(text)


 
#start app  in a thread
import time
from threading import Thread

class Main(Thread):
    def __init__(self,rc):
        Thread.__init__(self)
        self.rc= rc
    def run(self):
        self.app = wx.App()
        style = ( wx.CLIP_CHILDREN | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR | wx.NO_BORDER | wx.FRAME_SHAPED)
        self.f = SubtitleFrame( self.rc ,None, title='GVT' , style = style)

        self.f.Show()
        self.app.MainLoop()
    
    def hide(self):
        self.f.HideWindow()

    def show(self):
        self.f.ShowWindow()
    
    def setTextx(self, text):
        self.f.SetText(text)