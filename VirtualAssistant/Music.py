from pywinauto.application import Application
import time

class Music:

    def Start_Player_Music(self):
        app = Application().Start(cmd_line=u'"C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe" \\prefetch:1')
        wmplayerapp = app.WMPlayerApp
        wmplayerapp.Wait('ready')
        wmplayerapp.SetFocus()
        wmplayerapp.TypeKeys('{TAB}')
        time.sleep(0.2)
        wmplayerapp.TypeKeys('{ENTER}')

    def Close_Player_Music(self):
        app = Application().Connect(title = 'Windows Media Player')
        app.Kill_()

    def Play_Pause_Music(self):
        app = Application().Connect(title = 'Windows Media Player')
        wmplayerapp = app.WMPlayerApp
        wmplayerapp.Wait('ready')
        wmplayerapp.SetFocus()
        wmplayerapp.TypeKeys('{SPACE}')
        time.sleep(0.2)

    def Next_Song_Music(self):
        app = Application().Connect(title = 'Windows Media Player')
        wmplayerapp = app.WMPlayerApp
        wmplayerapp.Wait('ready')
        wmplayerapp.SetFocus()
        wmplayerapp.TypeKeys('{DOWN}')
        time.sleep(0.2)
        wmplayerapp.TypeKeys('{ENTER}')
        time.sleep(0.2)

    def Prev_Song_Music(self):
        app = Application().Connect(title = 'Windows Media Player')
        wmplayerapp = app.WMPlayerApp
        wmplayerapp.Wait('ready')
        wmplayerapp.SetFocus()
        wmplayerapp.TypeKeys('{UP}')
        time.sleep(0.2)
        wmplayerapp.TypeKeys('{ENTER}')
        time.sleep(0.2)