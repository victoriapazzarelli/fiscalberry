from kivy.uix.screenmanager import Screen
from kivy.app import App  # Import the App class
import os
import webbrowser
from fiscalberry.common.token_manager import delete_token
from kivy.properties import StringProperty
from os.path import join, dirname

class MainScreen(Screen):
    stop_image = StringProperty(join(dirname(__file__), "assets/stop.png"))
    play_image = StringProperty(join(dirname(__file__), "assets/play.png"))
    
    connected_image = StringProperty(join(dirname(__file__), "assets/connected.png"))
    disconnected_image = StringProperty(join(dirname(__file__), "assets/disconnected.png"))
    
    def start_service(self):
        """Inicia el servicio desde la GUI."""
        app = App.get_running_app()  # Use App.get_running_app()
        app.on_start_service()
        
    def toggle_service(self):
        """Alterna el estado del servicio desde la GUI."""
        app = App.get_running_app()
        app.on_toggle_service()

    def stop_service(self):
        """Detiene el servicio desde la GUI."""
        app = App.get_running_app()  # Use App.get_running_app()
        app.on_stop_service()

    def logout(self):
        """Cierra sesión y elimina el token JWT."""
        delete_token()

        app = App.get_running_app()  # Use App.get_running_app()
        app.root.current = "login"
    
    def open_sam4s_driver(self):
        """Abre el enlace del driver Sam4S Giant-100."""
        webbrowser.open("http://www.sam4s.com/eng/asp/products_detail.asp?seq=41")
    
    def open_citizen_driver(self):
        """Abre el enlace del driver Citizen CT-S310II."""
        webbrowser.open("https://www.citizen-systems.com/es/support/drivers-and-tools")
    
    def open_epson_tm20_driver(self):
        """Abre el enlace del driver Epson TM-T20."""
        webbrowser.open("https://support.epson.net/setupnavi/?PINF=swlist&OSC=WS&LG2=ES&MKN=TM-T20")
    
    def open_generic_pos_driver(self):
        """Información sobre el driver genérico POS."""
        from kivy.uix.popup import Popup
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.boxlayout import BoxLayout
        
        # Crear el contenido del popup
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        message = Label(
            text="Driver Genérico POS:\nPOS-Printer-Driver-Setup-V7.17.exe\n\nContacta al administrador del sistema\npara obtener este archivo.",
            text_size=(300, None),
            halign="center"
        )
        
        close_btn = Button(text="Cerrar", size_hint_y=None, height=40)
        
        content.add_widget(message)
        content.add_widget(close_btn)
        
        # Crear y mostrar el popup
        popup = Popup(
            title="Driver Genérico POS",
            content=content,
            size_hint=(None, None),
            size=(350, 200)
        )
        
        close_btn.on_press = popup.dismiss
        popup.open()
    
    def open_epson_tm88v_driver(self):
        """Abre el enlace del driver Epson TM-T88V."""
        webbrowser.open("https://support.epson.net/setupnavi/?PINF=swlist&OSC=WS&LG2=ES&MKN=TM-T88V")