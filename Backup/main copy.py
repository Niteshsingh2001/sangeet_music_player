from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.list import OneLineAvatarIconListItem,IconLeftWidget
from kivy.core.audio import SoundLoader,Sound
import os
import re


# Todo
# Working Slider
# Back to Player
# click list and play
# play where left


Window.size = (400, 700)
Window.clearcolor = (248/255, 200/255, 34/255)


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
    MDBoxLayout:
        orientation : "vertical"
        md_bg_color: 252/255, 72/255, 80/255,1
        size_hint:0.8,0.2
        pos_hint:{"center_x":0.5,"center_y":0.1}
        MDLabel:
            id : musicname
            text: "No Music Playing"
            halign:"center"
            theme_text_color: "Custom"
            text_color: 1, 1, 1, 1
            # pos_hint:{"center_y":0.5,"center_y":0.5}
            padding_x : 10

        MDCheckbox:
            id :playpause
            size_hint: None, None
            size: "48dp", "48dp"
            checkbox_icon_normal : "play"
            checkbox_icon_down : "pause"
            unselected_color :1,1,1,1
            selected_color : 1,1,1,1
            # pos_hint: {'center_x': .5, 'center_y': .5}
            on_state : app.play_pause()
    
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
                min: 0
                max: 100
                value: 40
                hint: False
                color: 1,1,1,1
                size_hint_y:0.2
                pos_hint:{"center_x":0.5,"center_y":0.5}
                padding_x : 10

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
                    # MDIconButton:
                    #     id :playpause
                    #     icon: "play"
                    #     theme_icon_color: "Custom"
                    #     icon_color: 1,1,1,1
                    #     pos_hint:{"center_x":0.5,"center_y":0.5}
                    #     on_press : app.play_pause()
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
            lst = OneLineAvatarIconListItem(text=self.songs[i])
            # lst.bind(on_press=self.play)
            lst.add_widget(IconLeftWidget(icon="music"))
            self.kvlang.get_screen("player").ids.container.add_widget(lst)

        

        # ---------------------end List------------
        self.kvlang.get_screen("Main").add_widget(bar)
        self.exit_manager()
        self.kvlang.get_screen("Main").manager.current = 'player'
        

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''
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
        
        # loading Music


        if p_val == True:
            self.music_lst = SoundLoader.load(self.full_loc)
            if self.music_lst:
                self.music_lst.play()
        elif p_val == False :
            self.music_lst.stop()
            self.music_lst.unload()
            self.music_lst = None
    
    def prv(self):
        if self.count <= -len(self.songs):
            self.count = 0
        
        print(self.count)
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
Music_player().run()