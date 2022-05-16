from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.list import OneLineAvatarIconListItem,IconLeftWidget
from kivy.properties import NumericProperty
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivy.core.audio import SoundLoader,Sound
import os
import re
import time


# Todo
# Working Slider 
# Back to Player    -----Done
# click list and play ------done
# play where left 

# Music Not Loaded msg screen no music  --- not perfect

Window.size = (400, 700)
# Window.clearcolor = (248/255, 200/255, 34/255)


appstyle = '''

ScreenManager:
    SplashScreen:
    Pick:
    Home:
    
<SplashScreen>:
    name: "splash"
    
    MDFloatLayout:
        md_bg_color: 1,1,1,1

        Image:
            source: "Music Player\Assets\logo.webp"
            pos_hint: {"center_x":0.5,"center_y": 0.5}

        MDLabel:
            text: "[color=#FC4850]Sangeet"
            pos_hint:{"center_x":0.5,"center_y":0.2}
            markup : True
            halign : "center"
            font_style: "H3"

<Pick>:
    name : "Main"
    
    MDLabel : 
        text:"[color=#FC4850]Where to look for Music"
        pos_hint:{"center_x":0.5,"center_y":0.55}
        markup : True
        halign : "center"
        font_style: "H4"
    MDRaisedButton:
        text: "Select"
        md_bg_color: 252/255, 72/255, 80/255
        size_hint: 0.3, 0.08
        pos_hint:{"center_x":0.5,"center_y":0.4}
        on_release:app.open_folder()

    MDFloatingActionButton:
        pos_hint:{"center_x":0.9,"center_y":0.06}
        icon: "music"
        md_bg_color: app.theme_cls.primary_color
        on_press : app.get_player()
 
    
<Home>:
    name : "player"
    MDBoxLayout:
        orientation : "vertical"
        MDFloatLayout:
            size_hint_y:0.2
            MDIconButton:
                icon: "keyboard-backspace"
                theme_icon_color: "Custom"
                icon_color: 252/255, 72/255, 80/255
                pos_hint:{"center_x":0.05,"center_y":0.5}
                on_press : app.back()
            MDLabel:
                text: "[color=#FC4850]Sangeet"
                pos_hint:{"center_x":0.5,"center_y":0.5}
                size_hint_y:0.25
                markup : True
                halign : "center"
                font_style: "H3"

        ScrollView:
            pos_hint:{"center_x":0.5,"center_y":0.5}
            MDList:
                id: container
    
        MDBoxLayout:
            orientation : "vertical"
            md_bg_color: 252/255, 72/255, 80/255,1
            size_hint:1,0.3

            MDSlider:
                id : time_bar
                hint: False
                color: 1,1,1,1
                size_hint_y:0.2
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding_x : 10
                hint: True
                # on_value : app.slider_val()
            MDBoxLayout:
                orientation : "vertical"
                size_hint:1,0.5      
                MDLabel:
                    id : musicname
                    text: "No Music Playing"
                    halign:"center"
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1
                    pos_hint:{"center_y":0.5,"center_y":0.5}
                    padding_x : 10

                MDFloatLayout:
                    orientation : "horizontal"
                    pos_hint:{"center_x":0.5,"center_y":0.5}
                    MDIconButton:
                        icon: "skip-previous"
                        theme_icon_color: "Custom"
                        icon_color: 1,1,1,1
                        pos_hint:{"center_x":0.3,"center_y":0.5}
                        on_press : app.prv()

                    MDCheckbox:
                        id :playpause
                        size_hint: None, None
                        size: "48dp", "48dp"
                        checkbox_icon_normal : "play"
                        checkbox_icon_down : "pause"
                        unselected_color :1,1,1,1
                        selected_color : 1,1,1,1
                        pos_hint: {'center_x': .5, 'center_y': .5}
                        on_state : app.play_pause()
                    MDIconButton:
                        icon: "skip-next"
                        theme_icon_color: "Custom"
                        icon_color: 1,1,1,1
                        pos_hint:{"center_x":0.7,"center_y":0.5}
                        on_press : app.next()
                    

'''

class SplashScreen(Screen):
    def on_enter(self, *args):
        Clock.schedule_once(self.switch_to_Pick,2)

    def switch_to_Pick(self, dt):
        self.manager.current = 'Main'
        self.manager.transition.direction =  "up"

class Pick(Screen):
    pass

class Home(Screen):
    pass

# class WindowManager(ScreenManager):
#     pass

class Music_player(MDApp):
    def build(self):
        
        self.theme_cls.primary_palette = "Red"  # "Purple", "Red"
        self.theme_cls.primary_hue = "400"  # "500"


        scrn = Screen()
        self.kvlang = Builder.load_string(appstyle)
        
        self.progress = NumericProperty()
        self.count = 0
        scrn.add_widget(self.kvlang)
        # Clock.schedule_once(self.play)
        return scrn

    def open_folder(self):
        self.file_manager = MDFileManager(exit_manager=self.exit_manager,select_path=self.select_path,preview=True)
        self.file_manager.show("C:")
        manager_open = True

    def select_path(self, path,):
        '''It will be called when you click on the file name
        or the catalog selection button.

        :type path: str;
        :param path: path to the selected directory or file;
        '''
        self.loc = path
        self.file= os.listdir(path)

        # Checing MP3 Files
        self.songs = []

        val = 0
        bar = MDProgressBar(orientation ="horizontal",size_hint =(1,0.01))
        for i in range(len(self.file)):
            extension = re.search("\.mp3", self.file[i])
            if extension :
                self.songs.append(self.file[i])
                val = val + 10
                bar.value = val


        # ---------------------Adding List------------
        
        for i in range(len(self.songs)):
            lst = OneLineAvatarIconListItem(text=self.songs[i],on_press=self.click_on_lst)
            # lst.bind()
            lst.add_widget(IconLeftWidget(icon="music"))
            self.kvlang.get_screen("player").ids.container.add_widget(lst)

        

        # ---------------------end List------------
        self.kvlang.get_screen("Main").add_widget(bar)
        self.exit_manager()
        self.kvlang.get_screen("Main").manager.current = 'player'

    def exit_manager(self, *args):
        self.manager_open = False
        self.file_manager.close()


    def play_pause(self):

            #path
            self.full_loc = os.path.join(self.loc,self.songs[self.count])

            # Music Name in bottom player sections
            m_name = re.split("\.mp3",self.songs[self.count])
            self.kvlang.get_screen("player").ids.musicname.text = f"{m_name[0]}"

            # Button val 
            p_val = self.kvlang.get_screen("player").ids.playpause.active
            slider = self.kvlang.get_screen("player").ids.time_bar
            # loading Music
            # self.music_lst = None
            if p_val == True:
                self.music_lst = SoundLoader.load(self.full_loc)             
                if self.music_lst:
                    self.music_lst.play()
                    slider.max = self.music_lst.length
                    # self.music_lst.seek(50)
                    slider.on_value = self.music_lst.seek(50)
                    print(self.music_lst.seek(50))
                    self.progress =  self.music_lst.get_pos()

                    slider = self.kvlang.get_screen("player").ids.time_bar.value = self.progress
                    print(self.progress)

            elif p_val == False :
                print(self.music_lst.get_pos())
                self.music_lst.stop()
                self.music_lst.unload()
                self.music_lst = None
        # except : 
        #     snackbar = Snackbar(text="Music Not Found!",snackbar_x="10dp",snackbar_y="10dp",)
        #     snackbar.size_hint_x = (Window.width - (snackbar.snackbar_x * 2)) / Window.width
        #     snackbar.buttons = [MDFlatButton(text="Add Music",theme_text_color ="Custom",text_color=(252/255, 72/255, 80/255,1),on_release=self.get_pick_for_snackbar)]
        #     snackbar.bg_color=(128/255, 128/255, 128/255)
        #     snackbar.open()
        #     self.kvlang.get_screen("player").ids.playpause.active = ""

    def slider_val(self):
        # slider = self.kvlang.get_screen("player").ids.time_bar
        # slider.max = self.music_lst.length
        # self.music_lst.stop()
        # self.music_lst.unload()
        # self.music_lst = None 
        # self.music_lst = self.music_lst = SoundLoader.load(self.full_loc)
        # self.music_lst.play()
        # self.music_lst.seek(slider.value)
        # self.play_pause()
        # print(slider.value)
        # print("hi")
        pass

    def click_on_lst(self,lst):
        song_name = self.songs.index(lst.text)
        # print(song_name)
        self.count = song_name
        self.music_lst.stop()
        self.music_lst.unload()
        self.music_lst = None
        self.play_pause()


    def prv(self):
        if self.count <= -len(self.songs):
            self.count = 0
        self.music_lst.stop()
        self.music_lst.unload()
        self.music_lst = None
        self.count = self.count-1
        self.play_pause()

    def next(self):
        if self.count >= len(self.songs)-1:
            self.count = 0
        self.music_lst.stop()
        self.music_lst.unload()
        self.music_lst = None
        self.count = self.count+1
        self.play_pause()
   
    def back(self):
        self.kvlang.get_screen("player").manager.current = 'Main'

    def get_player(self):
        self.kvlang.get_screen("Main").manager.current = 'player'
    def get_pick_for_snackbar(self,s):
        self.kvlang.get_screen("player").manager.current = 'Main'
Music_player().run()