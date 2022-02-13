import numpy as np
import win32gui, win32ui, win32con, win32api

def WindowDraw(self, rect):
        '''
        Draws a rectangle to the window
        '''
        if self.hwnd is None:
            return
            #raise Exception("HWND is none. HWND not called or invalid window name provided.")
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        #Set background mode to transparent
        #dcObj.SetBkColor(0x12345)
        #dcObj.SetBkMode(0)
        dcObj.Rectangle(rect)
        # Free Resources
        dcObj.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC) 

#Original : https://github.com/Sentdex/pygta5/blob/master/grabscreen.py
def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left, top, x2, y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.frombuffer(signedIntsArray, dtype='uint8')

    img.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img


