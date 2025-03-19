#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, GLib
from gaia import Gaia
gaiaReference = Gaia()


class GaiaWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Window setup
        self.set_title("Gaia")
        self.set_default_size(300, 400)
        
        # Main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.set_child(vbox)
        
        # Chat display (using TextView)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        vbox.append(scrolled)
        
        self.chat_display = Gtk.TextBuffer()
        text_view = Gtk.TextView(buffer=self.chat_display)
        text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        text_view.set_editable(False)
        text_view.set_cursor_visible(False)
        scrolled.set_child(text_view)
        
        # Create text tags for colors
        self.chat_display.create_tag("user_msg", foreground="#007BFF")
        self.chat_display.create_tag("bot_msg", foreground="#28A745")
        
        # Input area
        input_box = Gtk.Box(spacing=5)
        input_box.set_margin_start(5)
        input_box.set_margin_end(5)
        input_box.set_margin_bottom(5)
        vbox.append(input_box)
        
        # Entry box
        self.entry = Gtk.Entry()
        self.entry.set_hexpand(True)
        self.entry.connect('activate', self.send_message)
        input_box.append(self.entry)
        
        # Send button
        send_button = Gtk.Button(label="Send")
        send_button.connect('clicked', self.send_message)
        send_button.add_css_class('suggested-action')  # Blue accent
        input_box.append(send_button)

    def send_message(self, widget):
        user_message = self.entry.get_text()
        if user_message.strip():
            # Get end iterator for append
            end_iter = self.chat_display.get_end_iter()
            
            # Display user message
            self.chat_display.insert_with_tags_by_name(
                end_iter, f"You: {user_message}\n", "user_msg"
            )
            
            # Get bot response
            chatbot_response = str(gaiaReference.get_response(user_message))
            end_iter = self.chat_display.get_end_iter()
            self.chat_display.insert_with_tags_by_name(
                end_iter, f"Bot: {chatbot_response}\n", "bot_msg"
            )
            
            # Clear input
            self.entry.set_text("")

class GaiaApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.example.gaia')
        
    def do_activate(self):
        window = GaiaWindow(application=self)
        window.present()

if __name__ == '__main__':
    app = GaiaApp()
    app.run(None)
