import os, difflib
from PIL import Image
import tkinter as tk
from tkinter import ttk, CENTER
from Model import PasswordManager, Database
import customtkinter
from CTkMessagebox import CTkMessagebox

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class PasswordManagerGUI(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.database = None
        self.passwordManager = PasswordManager.PasswordManager("Données à hacher")
        
        self.title("Password Manager.py")
        self.geometry("700x450")
        customtkinter.set_appearance_mode('Dark')
        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")),
                                                 size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "CustomTkinter_logo_single.png")), size=(100, 100))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")),
                                                       size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "home_light.png")),
                                                 size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "chat_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "chat_light.png")),
                                                 size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(
            light_image=Image.open(os.path.join(image_path, "add_user_dark.png")),
            dark_image=Image.open(os.path.join(image_path, "add_user_light.png")), size=(20, 20))

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="MyLogin",
                                                             compound="left",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=50, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10,
                                                   text="Home",
                                                   fg_color="transparent", text_color=("gray10", "gray90"),
                                                   hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text=" Add Password",
                                                      fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w",
                                                      command=self.frame_2_button_event)

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40,
                                                      border_spacing=10, text="Generate",
                                                     fg_color="transparent", text_color=("gray10", "gray90"),
                                                      hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w",
                                                      command=self.frame_3_button_event)

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame,
                                                                values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame
        self.home_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="",
                                                                   image=self.large_test_image, corner_radius=500)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=(30, 0))
        self.welcome_label = customtkinter.CTkLabel(self.home_frame, text="Welcome to your Password Manager!",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.welcome_label.grid(row=1, column=0, padx=20, pady=(10, 2))
        self.welcome_label_subtitle = customtkinter.CTkLabel(self.home_frame,
                                                             text="Please enter your password to continue.",
                                                             font=customtkinter.CTkFont(size=15, weight="bold"))
        self.welcome_label_subtitle.grid(row=2, column=0, padx=25, pady=(0, 15))

        self.password_label = customtkinter.CTkLabel(self.home_frame, text="Password:",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
        self.password_label = customtkinter.CTkLabel(self.home_frame, text="Password:",
                                                     font=customtkinter.CTkFont(size=15, weight="bold"))
        self.password_label.grid(row=10, column=0, padx=20, pady=5)

        self.password_entry = customtkinter.CTkEntry(self.home_frame, show="*")
        self.password_entry.grid(row=11, column=0, padx=20, pady=5)

        self.login_button = customtkinter.CTkButton(self.home_frame, text="Login", command=self.login)
        self.login_button.grid(row=12, column=0, padx=20, pady=10)

        # create second frame
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.third_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("home")

    def login(self):

        self.database = Database.MySQLDatabase('localhost', 'root', '<wmk6Px2hnGAd>', 'usere')
        self.passwordManager.database_row(self.database.execute_query('SELECT * FROM passwords'))




        self.frame_2_button.grid(row=2, column=0, sticky="ew")
        self.frame_3_button.grid(row=3, column=0, sticky="ew")
        password = self.password_entry.get()

        self.unpacked_home_widgets()
        self.connexion_frame()
        self.adduser_frame_configuration()
        self.adduser_frame_configuration()

        # Example: Check if username and password are correct
        if password == "password":
            print("Login successful")
            # Add code to proceed to the password manager interface
        else:
            print("Login failed")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def connexion_frame(self):

        self.home_title = customtkinter.CTkLabel(self.home_frame, text="Successfully connected to database !",
                                                 font=customtkinter.CTkFont(size=20, weight="bold"))
        self.home_title.grid(row=0, column=0, padx=20, pady=(40, 2))

        self.table = ttk.Treeview(self.home_frame, columns=("Website", "Username", "Password"), show="headings")
        custom_font = customtkinter.CTkFont(size=35, weight="bold")
        self.table.heading("Website", text="Website")
        self.table.heading("Password", text="Password")
        self.table.heading("Username", text="Username")
        self.table.column("#0", width=40)
        for column in self.table["columns"]:
            self.table.column(column, anchor=CENTER)
        custom_style = ttk.Style()
        custom_style.theme_use('default')
        custom_style.configure("Treeview", font=custom_font, fieldbackground="silver", background='silver')
        custom_style.configure("Treeview.Heading", font=custom_font, background="grey")

        for website, credentials in self.passwordManager.get_passwords_dict().items():
            username = credentials['username']
            print(credentials['password'])
            password = self.passwordManager._decrypt(credentials['password'])

            self.table.insert("", "end", values=(website, username, password))


        self.table.grid(row=1, column=0, padx=20, pady=20)
        self.search_entry = customtkinter.CTkEntry(self.home_frame, placeholder_text="Enter Text..")
        self.search_entry.grid(row=2, column=0, padx=20, pady=(0, 2))
        self.search_button = customtkinter.CTkButton(self.home_frame, text="search",
                                                     font=customtkinter.CTkFont(size=14, weight="bold"),
                                                     command=self.search)
        self.search_button.grid(row=3, column=0, padx=20, pady=(0, 2))

    def unpacked_home_widgets(self):
        self.password_entry.grid_forget()
        self.login_button.grid_forget()
        self.password_label.grid_forget()
        self.welcome_label_subtitle.grid_forget()
        self.welcome_label.grid_forget()
        self.home_frame_large_image_label.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")


    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")


    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def search(self):
        search_label = self.search_entry.get()

        weblist = []

        for item_id in self.table.get_children():
            weblist.append(self.table.item(item_id, 'values')[0])

        closest_string = difflib.get_close_matches(search_label, weblist, cutoff=0.3)

        if len(closest_string) != 0:
            for item_id in self.table.get_children():
                if self.table.item(item_id, 'values')[0] == closest_string[0]:
                    password = self.table.item(item_id, 'values')[2]
                    self.search_entry.delete(0, tk.END)
                    self.search_entry.insert(0, password)
                    element = self.table.item(item_id, 'values')
                    self.table.delete(item_id)
                    self.table.insert('', '0', values=element)
        else:
            self.search_entry.delete(0, tk.END)
            self.search_entry.insert(0, 'no match found')

    def adduser_frame_configuration(self):
        # configure second frame
        self.title_second_frame = customtkinter.CTkLabel(self.second_frame, text='ADD YOUR NEW PASSWORD TO DATABASE', font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_second_frame.grid(row=0, column=0, padx=70, pady=40, sticky="nsew")
        self.website_field = customtkinter.CTkEntry(self.second_frame, placeholder_text="Website")
        self.website_field.grid(row=1, column=0, padx=20, pady=(0, 2), )
        self.username_field = customtkinter.CTkEntry(self.second_frame, placeholder_text="Username")
        self.username_field.grid(row=2, column=0, padx=20, pady=(0, 2), )
        self.password_field = customtkinter.CTkEntry(self.second_frame, placeholder_text="Password")
        self.password_field.grid(row=3, column=0, padx=20, pady=(0, 2))
        self.submit_button = customtkinter.CTkButton(self.second_frame, text="SUBMIT",
                                            font=customtkinter.CTkFont(size=18, weight="bold"), command=self.add_to_database)
        self.submit_button.grid(row=4, column=0, padx=20, pady=(20, 2),)

        # configure thrid frame
        self.title_third_frame = customtkinter.CTkLabel(self.third_frame, text='GENERATE PASSWORD',
                                                         font=customtkinter.CTkFont(size=20, weight="bold"))
        self.title_third_frame.grid(row=0, column=0, padx=150, pady=40, sticky="nsew")
        self.website_field_third = customtkinter.CTkEntry(self.third_frame, placeholder_text="Website")
        self.website_field_third.grid(row=1, column=0, padx=20, pady=(0, 2), )
        self.username_field_third = customtkinter.CTkEntry(self.third_frame, placeholder_text="Username")
        self.username_field_third.grid(row=2, column=0, padx=20, pady=(0, 2), )
        self.generate_button = customtkinter.CTkButton(self.third_frame, text="GENERATE",
                                                     font=customtkinter.CTkFont(size=18, weight="bold"),
                                                     command=self.generate_password_popup)
        self.generate_button.grid(row=4, column=0, padx=20, pady=(20, 2), )


    def add_to_database(self):
        website = self.website_field.get()
        password = self.password_field.get()
        username = self.username_field.get()

        self.table.insert("", "end", values=(website, username, password))
        CTkMessagebox(title="Generate Password", message="Successfully add", icon='info')
        password = self.passwordManager._encrypt(password)
        self.database.execute_query(f"INSERT INTO passwords (website, username, password) VALUES ('{website}', '{username}', '{password}')")

    def generate_password_popup(self):
        website = self.website_field_third.get()
        username = self.username_field_third.get()
        password = self.passwordManager.generate_password(24)

        self.password_popup = CTkMessagebox(title="Generate Password", message="Website={}, Username={}, Password={}".
                                            format(website, username, password)
                                            , icon='check', option_1='Add to database'
                                            , option_2='Copy', password=password, website=website, username=username)
        if self.password_popup.get() == 'add':
            self.table.insert("", "end", values=(website, username, password))
            password = self.passwordManager._encrypt(password)
            self.database.execute_query(f"INSERT INTO passwords (website, username, password) "
                                        f"VALUES ('{website}', '{username}', '{password}')")



if __name__ == "__main__":
    app = PasswordManagerGUI()
    app.mainloop()
