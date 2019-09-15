'''
-billy_gui.py
-Defines the interface of the Billy program split between two classes:
    -The Billy_GUI class which serves as the base parent for the main frame of the program, housing both it and a menu
     bar. Aside from being a container, the main point of the Billy_GUI class is to hold an instance of the Billy class
     to be used as an editor allowing the GUI to keep track of and edit the state of a given Shelf object. It is
     allotted the tasks of adding contents to the Shelf object to be displayed and edited as well as file I/O for
     saving, loading, and creating Shelf objects.
    -The Shelf_Frame class which displays most of the Billy object's Shelf object's contents. It houses most of the
     actual display portion of the GUI and provides the primary interface for the user to edit the contents of the
     Billy editor's Shelf.
-The KeywordInStringException is defined in order to maintain certain strings are not included within Shelf data for
 the benefit of the file I/O portion of the program.
-The EmptyShelfNameException is defined to be raised whenever the user attempts to provide an empty string as a Shelf
 name, which the program does not allow

Traven 'tkwtph' Gonzales 2019
'''


import tkinter as tk
import entry
import media_sublist
import media_list
import shelf
import billy


class Billy_GUI(tk.Tk):
    '''Defines the base of the Billy UI'''


    # INITIALIZATION
    def __init__(self, *args, **kwargs):
        '''Initializes the starting state and window of the Billy program'''
        tk.Tk.__init__(self, *args, **kwargs)
        # Sets the attributes of the title bar
        self.wm_title("Billy")
        self.iconbitmap("billy_icon.ico")
        self.editor = billy.Billy()

        # Creates base window for program
        self.container = tk.Frame(self)
        self.container.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Defines the current frame to be raised, in this case initially a Shelf_Frame meant to display an empty Shelf
        self.cur_frame = Shelf_Frame(self.container, self)
        self.cur_frame.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W)
        self.cur_frame.grid_rowconfigure(3, weight=2)
        self.cur_frame.grid_columnconfigure(0, weight=1)
        self.cur_frame.tkraise()

        # Creates the menubar for the program
        self.menubar = tk.Menu(self)
        # Sets up File Menu
        file_menu = tk.Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="New", command=self._make_new_shelf)
        file_menu.add_command(label="Load", command=self._load_shelf)
        file_menu.add_command(label="Save", command=self._save_shelf)
        self.menubar.add_cascade(label="File", menu=file_menu)
        # Sets up Edit Menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label="Add Media", command=self._add_media)
        self.edit_menu.add_command(label="Add Entry", state="disabled")
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        # Sets up View Menu along with its associated Sort submenu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_command(label="Refresh", command=self.cur_frame.update_media_widgets)
        self.view_menu.add_command(label="Back", state="disabled", command=self._transition_to_media_widgets)
        self.sort_menu = tk.Menu(self.view_menu, tearoff=0)
        for sort_name in ("Default", "Name", "Author", "Genre", "Price", "Release", "Date Added"):
            self.sort_menu.add_command(label=sort_name)
        self.view_menu.add_cascade(label="Sort", menu=self.sort_menu, state="disabled")
        self.menubar.add_cascade(label="View", menu=self.view_menu)
        self.config(menu=self.menubar)

        # Configures the weight for the origin position of the Billy_Root
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    # SHELF FILE I/O
    def _make_new_shelf(self):
        '''Attempts to make a new Shelf object using the name from the shelf name entry in the Shelf_Frame'''
        shelf_name = self.cur_frame.shelf_name.get()
        try:
            valid_name = self.validate_shelf_name(shelf_name).strip()
            self.editor.make_new(valid_name)
            self._transition_to_media_widgets()
        except EmptyShelfNameException:
            self.cur_frame.set_error_message("Shelf name cannot be empty")

    def _load_shelf(self):
        '''Attempts to load a Shelf object using the name from the shelf name entry in the Shelf_Frame'''
        shelf_name = self.cur_frame.shelf_name.get()
        try:
            valid_name = self.validate_shelf_name(shelf_name).strip()
            self.editor.load(valid_name)
            self._transition_to_media_widgets()
        except EmptyShelfNameException:
            self.cur_frame.set_error_message("Shelf name cannot be empty")
        except FileNotFoundError:
            self.cur_frame.set_error_message(f"No Shelf exists with the name {shelf_name}")
        except OSError:
            self.cur_frame.set_error_message("Error occurred in loading Shelf")

    def _save_shelf(self):
        '''Attempts to save a Shelf object using thename from the shelf name variable in the Shelf_Frame'''
        shelf_name = self.cur_frame.shelf_name.get()
        try:
            valid_name = self.validate_shelf_name(shelf_name).strip()
            if self.editor.get_shelf().get_name() != valid_name:
                self.editor.get_shelf().set_name(valid_name)
            self.editor.save()
            self.cur_frame.clear_error_message()
        except EmptyShelfNameException:
            self.cur_frame.set_error_message("Shelf name cannot be empty")
        except OSError:
            self.cur_frame.set_error_message("Error occurred in saving Shelf")


    # SHELF EDITING
    def _add_media(self):
        '''Creates a new Media_List to add to the shelf'''
        try:
            type_name, user_confirmed = self.retrieve_title_str("Enter Media Type:")
            if user_confirmed:
                self.editor.get_shelf().add_media(Billy_GUI.validate_title_str(type_name))
                self.cur_frame.destroy_content_widgets()
                self.cur_frame.content_widgets = self.cur_frame.make_media_widgets(self.editor.get_shelf().get_media())
                self.cur_frame.draw_content_widgets()
            self.cur_frame.clear_error_message()
        except KeywordInStringException:
            self.cur_frame.set_error_message("'=+/', '/*/', '\\n', and '?=n' cannot appear in a Media name")
        except shelf.ShelfOverflowException:
            self.cur_frame.set_error_message("Shelf is at capacity with Media, cannot add more")

    def add_entry(self, media_i: int):
        '''Creates a new Entry object to add to a Media_List object's backlog'''
        try:
            entry_info, confirmed = self.edit_entry_info()
            if confirmed:
                new_entry = entry.Entry(entry_info[0], entry_info[1], entry_info[2], entry_info[3], entry_info[4],
                                        entry_info[5], entry_info[6])
                m_list = self.editor.get_shelf().get_media()[media_i]
                m_list.backlog.insert_item(new_entry)
                self.cur_frame.update_backlog_widgets(media_i)
            self.cur_frame.clear_error_message()
            self.cur_frame.clear_error_message()
        except ValueError:
            self.cur_frame.set_error_message("Price, Release Year, and Priority fields must be filled in")
        except KeywordInStringException:
            self.cur_frame.set_error_message("'=+/', '/*/', '\\n', and '?=n' cannot appear in Entry fields")
        except media_sublist.MSOverflowException:
            self.cur_frame.set_error_message("Backlog is full, cannot add Entry")


    # VIEW ACTIONS
    def _transition_to_media_widgets(self):
        '''Changes the contents of the Billy_GUI's Shelf_Frame to display the Shelf object's list of Media_List
        objects'''
        self.cur_frame.destroy_content_widgets()
        self.cur_frame.content_widgets = self.cur_frame.make_media_widgets(self.editor.get_shelf().get_media())
        self.cur_frame.draw_content_widgets()
        self.view_menu.entryconfigure("Refresh", command=self.cur_frame.update_media_widgets)
        self.view_menu.entryconfigure("Back", state="disabled")
        self.view_menu.entryconfigure("Sort", state="disabled")
        self.edit_menu.entryconfigure("Add Entry", state="disabled")
        self.edit_menu.entryconfigure("Add Media", state="normal")
        self.cur_frame.clear_error_message()

    def configure_sort_submenu(self, backlog_flag: bool, media_i: int):
        '''Given the index of a Media_List object in a Shelf object, configures the commands of the Sort submenu
        to properly sort a Media_Sublist at the index and display propelry on the Shelf_Frame'''
        self.sort_menu.entryconfigure("Default", command=lambda: self._resort_widgets(backlog_flag, "default", media_i))
        self.sort_menu.entryconfigure("Name", command=lambda: self._resort_widgets(backlog_flag, "name", media_i))
        self.sort_menu.entryconfigure("Author", command=lambda: self._resort_widgets(backlog_flag, "author", media_i))
        self.sort_menu.entryconfigure("Genre", command=lambda: self._resort_widgets(backlog_flag, "genre", media_i))
        self.sort_menu.entryconfigure("Price", command=lambda: self._resort_widgets(backlog_flag, "price", media_i))
        self.sort_menu.entryconfigure("Release", command=lambda: self._resort_widgets(backlog_flag, "release", media_i))
        self.sort_menu.entryconfigure("Date Added", command=lambda: self._resort_widgets(backlog_flag, "date", media_i))

    def _resort_widgets(self, backlog_flag: bool, sort_key: str, media_i: int):
        '''Makes a command for a process for sorting Entry widgets in a backlog or completed Media_Sublist'''
        m_list = self.editor.get_shelf().get_media()[media_i]

        if backlog_flag:
            m_list.backlog.change_sort(sort_key)
            self.cur_frame.update_backlog_widgets(media_i)
        else:
            m_list.completed.change_sort(sort_key)
            self.cur_frame.update_completed_widgets(media_i)


    # DATA RETRIEVAL
    def retrieve_title_str(self, command_str: str) -> (str, bool):
        '''Creates a top level to retrieve a string to be used as name for a multitude of purposes. Has a command_str
        parameter to tell user what to do'''
        top = tk.Toplevel(self)
        top.iconbitmap("billy_icon.ico")
        # Label tells user what to do
        command = tk.Label(top, text=command_str)
        command.pack(side=tk.TOP, fill=tk.X, padx=2, pady=2)

        # Portion for Data Retrieval
        class Nonlocal:
            '''Used to allow the nested function on_confirm to access a bool variable to set'''
            pass

        # Variables to return
        result = tk.StringVar()
        nl = Nonlocal()
        nl.confirmed = False

        # Defines widgets and their commands
        def on_confirm():
            '''Upon call, destroys the toplevel it was called upon and sets the confirm flag to True'''
            top.destroy()
            nl.confirmed = True

        name_entry = tk.Entry(top, textvariable=result, font="helvetica 14")
        name_entry.pack(side=tk.LEFT, padx=2, pady=2)
        enter_btn = tk.Button(top, text="Enter", background="gainsboro", relief=tk.GROOVE, command=lambda: on_confirm())
        enter_btn.pack(side=tk.RIGHT, padx=2, pady=2)
        name_entry.bind("<Return>", lambda event: on_confirm())

        top.resizable(width=False, height=False)
        top.wait_window()
        result_str = str(result.get())
        return result_str, nl.confirmed

    def edit_entry_info(self, item: entry.Entry = None) -> ([str, str, str, float, int, float], bool):
        '''Creates a toplevel that may either be used to retrieve info to create and Entry object or display the
        attributes of an Entry object for viewing or editing'''
        top = tk.Toplevel(self.container)
        top.iconbitmap("billy_icon.ico")
        top.wm_title("Enter Info") if item is None else top.wm_title(item.get_name())

        # Data Retrieval
        # Variables
        class Nonlocal:
            '''Dummy class used to store a boolean variable for out of local scope setting'''
            pass

        name = tk.StringVar(value=item.get_name() if item is not None else "")
        author = tk.StringVar(value=item.get_author() if item is not None else "")
        genre = tk.StringVar(value=item.get_genre() if item is not None else "")
        price = tk.StringVar(value=str(item.get_price()) if item is not None else "")
        release = tk.StringVar(value=str(item.get_release_year()) if item is not None else "")
        priority = tk.IntVar()
        priority.set(item.get_priority() if item is not None else 1)
        nl = Nonlocal()
        nl.confirmed = False
        nl.notes = item.get_notes() if item is not None else ""

        # Validate Commands
        int_vdcm = (self.register(self.validate_only_digits), "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")
        float_vdcm = (self.register(self.validate_only_float), "%d", "%i", "%P", "%s", "%S", "%v", "%V", "%W")

        # Widgets
        # Name
        name_lb = tk.Label(top, text="Entry Name")
        name_lb.grid(row=0, column=0, columnspan=3, sticky=tk.W, padx=5, pady=(5, 0))
        name_entry = tk.Entry(top, font="helvetica 18", textvariable=name)
        name_entry.grid(row=1, column=0, columnspan=3, sticky=tk.N + tk.S + tk.E + tk.W, padx=5)
        # Author, Genre, Price, Release Year
        for attr, row, col, padx, v, v_cm, tv in [("Author", 2, 0, (5, 0), "none", None, author),
                                                  ("Genre", 2, 1, (5, 0), "none", None, genre),
                                                  ("Price", 2, 2, 5, "key", float_vdcm, price),
                                                  ("Release Year", 4, 0, (5, 0), "key", int_vdcm, release)]:
            attr_lb = tk.Label(top, text=attr)
            attr_lb.grid(row=row, column=col, sticky=tk.W, padx=padx)
            attr_entry = tk.Entry(top, font="helvetica 14", validate=v, validatecommand=v_cm, textvariable=tv)
            attr_entry.grid(row=row + 1, column=col, sticky=tk.N + tk.S + tk.E + tk.W, padx=padx)
        # Priority
        priority_lb = tk.Label(top, text="Priority")
        priority_lb.grid(row=4, column=1, sticky=tk.W, columnspan=2, padx=5)
        p_radio_base = tk.Label(top)
        p_radio_base.grid(row=5, column=1, sticky=tk.E + tk.W, columnspan=2, padx=5)
        for i in range(1, 6):
            priority_btn = tk.Radiobutton(p_radio_base, text=f"{i}", variable=priority, value=i)
            priority_btn.grid(row=0, column=i - 1, sticky=tk.W + tk.N + tk.S + tk.E)
        # Notes
        note_lb = tk.Label(top, text="Notes")
        note_lb.grid(row=6, column=0, columnspan=3, sticky=tk.W, padx=5)
        note_text = tk.Text(top)
        note_text.grid(row=7, columnspan=3, sticky=tk.W + tk.E + tk.S + tk.N, padx=5)
        note_text.insert("1.0", nl.notes)
        # Date Completed and Added
        if item is not None:
            added_lb = tk.Label(top, text=f"Date Added: {item.get_datetime_added().strftime('%m/%d/%Y')}")
            added_lb.grid(row=8, column=0, columnspan=2, sticky=tk.W, padx=(5, 0), pady=(5, 0))
            if item.get_datetime_completed() is not None:
                completed_lb = tk.Label(top,
                                        text=f"Date Completed: {item.get_datetime_completed().strftime('%m/%d/%Y')}")
                completed_lb.grid(row=9, column=0, columnspan=2, sticky=tk.W, padx=(5, 0), pady=(0, 5))

        # Save Button to confirm information selection (Including its command)
        def on_confirm():
            '''Destroys top and confirms that the user is sure of the values they have entered'''
            nl.confirmed = True
            nl.notes = note_text.get("1.0", tk.END)
            top.destroy()

        save_btn = tk.Button(top, text="Save", relief=tk.GROOVE, background="gainsboro", command=on_confirm)
        save_btn.grid(row=8, column=2, rowspan=2, sticky=tk.E + tk. N + tk.S, padx=(0, 5), pady=(5, 5))

        top.resizable(width=False, height=False)
        top.wait_window()
        name_r = self.validate_title_str(name.get())
        author_r = self.validate_title_str(author.get())
        genre_r = self.validate_title_str(genre.get())
        price_r = round(float(price.get()), 2)
        release_r = int(release.get())
        priority_r = priority.get()
        notes_r = Billy_GUI.validate_notes_str(nl.notes)
        return [name_r, author_r, genre_r, price_r, release_r, priority_r, notes_r], nl.confirmed

    def validate_only_digits(self, d, i, P, s, S, v, V, W) -> bool:
        '''Used for Entry objects to assure only digits are entered (Parameter names chosen according to Tk validate
        documentation)'''
        if P:
            try:
                int(P)
                return True
            except ValueError:
                return False
        else:
            return False

    def validate_only_float(self, d, i, P, s, S, v, V, W) -> bool:
        '''Used for Entry objects to assure only values representing a valid float can be entered (Parameter names
        chosen according to Tk validate documentation)'''
        if P:
            try:
                float(P)
                return True
            except ValueError:
                return False
        else:
            return False

    @staticmethod
    def validate_title_str(title_str: str) -> str:
        '''Raised an error if any of the keyword disallowed from most strings in the program are in the string srgument.
        Otherwise strips and returns the string. Different from other validate functions in that it is not used as a
        validate command for an Entry object.'''
        for keyword in ("=+/", "/*/", "\n", "?=n"):
            if keyword in title_str:
                raise KeywordInStringException()
        return title_str.strip()

    @staticmethod
    def validate_notes_str(notes_str: str) -> str:
        '''Unlike the validate command methods, takes a string meant to represent a potential Entry object's notes
        attribute and raises an error if it contains any certain keyword other than \n. Otherwise returns a stripped
        version of the notes'''
        for keyword in ("=+/", "/*/", "?=n"):
            if keyword in notes_str:
                raise KeywordInStringException()
        return notes_str.strip()

    @staticmethod
    def validate_shelf_name(shelf_str: str) -> str:
        '''Takes a string meant to be used as a Shelf name and confirms that the name is not empty'''
        if len(shelf_str) == 0:
            raise EmptyShelfNameException()
        return shelf_str


class Shelf_Frame(tk.Frame):
    '''Defines the frame displaying a Shelf object's contents, including its list of Media_Lists as well as those
    Media_List's entry objects'''


    # INITIALIZATION
    def __init__(self, parent: tk.Frame, controller: Billy_GUI):
        '''Initializes the start state of each Shelf_Frame'''
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Creates the "Shelf Name" portion of the UI
        shelf_label = tk.Label(self, text="Shelf Name")
        shelf_label.grid(row=0, column=0, sticky=tk.W, padx=10)
        self.shelf_name = tk.StringVar(value=controller.editor.get_shelf().get_name())
        shelf_name_entry = tk.Entry(self, font="helvetica 24", textvariable=self.shelf_name)
        shelf_name_entry.grid(row=1, column=0, sticky=tk.E + tk.W, padx=10)

        # Creates the "Error Message" portion of the UI
        self.error_message = tk.StringVar()
        error_display = tk.Label(self, textvariable=self.error_message, foreground="red")
        error_display.grid(row=2, column=0, padx=10)

        # Creates the "Shelf Contents" display portion of the UI
        # Defines and configures the initial container of the display, a base frame to hold the display comprised of a
        # a canvas, frame, and scrollbar
        self.base_frame = tk.Frame(self, height=500, width=500)
        self.base_frame.grid(row=3, column=0, sticky=tk.E + tk.W + tk.N + tk.S, padx=10, pady=(0, 10))
        self.base_frame.grid_rowconfigure(0, weight=1)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_propagate(False)
        # Defines and configures the Shelf display canvas, associating its view with the scrollbar
        self.shelf_canvas = tk.Canvas(self.base_frame, background="gainsboro")
        self.shelf_canvas.grid(row=0, column=0, sticky=tk.N + tk.S + tk.W + tk.E)
        # Defines and configures scrollbar
        self.shelf_vsb = tk.Scrollbar(self.base_frame, orient=tk.VERTICAL, command=self.shelf_canvas.yview)
        self.shelf_vsb.grid(row=0, column=1, sticky=tk.N + tk.S)
        self.shelf_canvas.configure(yscrollcommand=self.shelf_vsb.set)
        # Defines and configures the frame meant to hold all widgets representing Shelf item widgets (i.e. Media, Entry)
        self.content_frame = tk.Frame(self.shelf_canvas, background="gainsboro")
        self.update()
        self.shelf_canvas.create_window((0, 0), window=self.content_frame, anchor=tk.N + tk.W,
                                        tags="self.content_frame")
        self.bind("<Configure>", self.on_resize)
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        # Defines the list of widgets to be currently displayed in the Shelf_Frame
        self.content_widgets = []


    # INTERACTIONN HANDLING
    def set_error_message(self, error_str: str):
        '''Sets an error message for the user to see'''
        self.error_message.set(error_str)

    def clear_error_message(self):
        '''Clears the current error message after an interaction goes through without raising an exception'''
        self.error_message.set("")

    def on_resize(self, event):
        '''Resizes certain widgets upon configuring of base window size'''
        # Process for matching content frame width to shelf canvas width (20 used to account for padding)
        width = event.width - self.shelf_vsb.winfo_width() - 20
        self.shelf_canvas.itemconfigure("self.content_frame", width=width)

    def on_frame_configure(self, event):
        '''Properly sets up scrollregion for Shelf Display after content widgets are packed and configured'''
        self.shelf_canvas.configure(scrollregion=self.shelf_canvas.bbox(tk.ALL))


    # SHELF CONTENT CREATION/EDITING
    # GENERAL
    def destroy_content_widgets(self):
        '''Destroys all the content widget currently in the Shelf_Frame's content widgets list'''
        for widget in self.content_widgets:
            widget.destroy()

    def draw_content_widgets(self):
        '''Packs the content widgets currently in the Shelf_Frame's content widgets list'''
        for widget in self.content_widgets:
            widget.pack(fill=tk.X, padx=4, pady=4)

    # MEDIA WIDGETS
    def _remove_media(self, media_i: int):
        '''Given the index for a Media_List in a Shelf, removes the Media_List object at media_i in the Shelf'''
        self.controller.editor.get_shelf().remove_media(media_i)
        self.update_media_widgets()
        self.clear_error_message()

    def _rename_media(self, media_i: int):
        '''Given the index for a Media_List in a shelf, renames the type for the Media_List object at media_i in the
        Shelf'''
        try:
            type_name, user_confirmed = self.controller.retrieve_title_str("Enter New Media Name:")
            if user_confirmed:
                valid_type = self.controller.validate_title_str(type_name)
                self.controller.editor.get_shelf().get_media()[media_i].set_type(valid_type)
                self.controller.editor.get_shelf().resort_media()
                self.update_media_widgets()
            self.clear_error_message()
        except KeywordInStringException:
            self.set_error_message("'=+/', '/*/', '\\n', and '?=n' cannot appear in a Media name")

    def _transition_to_backlog_contents(self, media_i: int):
        '''Given the index for a Media_List in a Shelf, transitions the contents frame to display the backlog of the
        Media_List at media_i'''
        self.destroy_content_widgets()
        m_list = self.controller.editor.get_shelf().get_media()[media_i]
        self.content_widgets = self._make_entry_widgets(m_list.backlog.get_items(), True, media_i)
        self.draw_content_widgets()
        self.controller.view_menu.entryconfigure("Refresh", command=lambda: self.update_backlog_widgets(media_i))
        self.controller.view_menu.entryconfigure("Back", state="normal")
        self.controller.view_menu.entryconfigure("Sort", state="normal")
        self.controller.configure_sort_submenu(True, media_i)
        self.controller.edit_menu.entryconfigure("Add Entry", state="normal",
                                                 command=lambda: self.controller.add_entry(media_i))
        self.controller.edit_menu.entryconfigure("Add Media", state="disabled")
        self.clear_error_message()

    def _transition_to_completed_contents(self, media_i: int):
        '''Given the index for a Media_List in a Shelf, transitions the contents frame to display the completed sublist
        of the Media_List at media_i'''
        self.destroy_content_widgets()
        m_list = self.controller.editor.get_shelf().get_media()[media_i]
        self.content_widgets = self._make_entry_widgets(m_list.completed.get_items(), False, media_i)
        self.draw_content_widgets()
        self.controller.view_menu.entryconfigure("Refresh", command=lambda: self.update_completed_widgets(media_i))
        self.controller.view_menu.entryconfigure("Back", state="normal")
        self.controller.view_menu.entryconfigure("Sort", state="normal")
        self.controller.configure_sort_submenu(False, media_i)
        self.controller.edit_menu.entryconfigure("Add Media", state="disabled")
        self.controller.edit_menu.entryconfigure("Add Entry", state="disabled")
        self.clear_error_message()

    def update_media_widgets(self):
        '''Redraws media widgets upon a change or interaction being made being made'''
        self.destroy_content_widgets()
        self.content_widgets = self.make_media_widgets(self.controller.editor.get_shelf().get_media())
        self.draw_content_widgets()
        self.clear_error_message()

    def make_media_widgets(self, medias: [media_list.Media_List]) -> [tk.Label]:
        '''Returns a list of widgets meant to represent a Shelf object's list of Media_List objects'''
        result = []
        for i in range(len(medias)):
            result.append(self._make_media_widget(medias[i], i))
        return result

    def _make_media_widget(self, media: media_list.Media_List, media_i: int) -> tk.Label:
        '''Given a Media_List object and its index within a Shelf object's contents list, makes a widget to represent
        the Media_List'''
        # Defines layout of media widget
        media_widget = tk.Label(self.content_frame, relief=tk.GROOVE, background="white smoke", height=5)
        name = tk.Label(media_widget, text=media.get_type(), font="helvetica 16")
        name.grid(row=0, column=0, columnspan=4, sticky=tk.N + tk.S + tk.W, padx=2)
        for (text, col, funct) in [("View Backlog", 0, lambda: self._transition_to_backlog_contents(media_i)),
                                   ("View Completed", 1, lambda: self._transition_to_completed_contents(media_i)),
                                   ("Rename", 2, lambda: self._rename_media(media_i)),
                                   ("Remove", 3, lambda: self._remove_media(media_i))]:
            btn = tk.Button(media_widget, text=text, background="gainsboro", relief=tk.GROOVE, command=funct)
            btn.grid(row=1, column=col, sticky=tk.N + tk.S + tk.E + tk.W, padx=2, pady=(0, 2))

        # Configures media widget
        for row_i in range(2):
            media_widget.grid_rowconfigure(row_i, weight=1)
        for col_i in range(4):
            media_widget.grid_columnconfigure(col_i, weight=1)
        media_widget.grid_propagate(False)
        return media_widget

    # ENTRY WIDGETS
    def _view_and_edit_entry(self, backlog_flag: bool, media_i: int, item_i: int):
        '''Process For viewing an Entry objects' attributes and possible editing'''
        try:
            m_list = self.controller.editor.get_shelf().get_media()[media_i]
            m_sublist = m_list.backlog if backlog_flag else m_list.completed
            entry_attrs, confirmed = self.controller.edit_entry_info(m_sublist.get_items()[item_i])

            if confirmed:
                m_sublist.edit_item(item_i, ["name", "author", "genre", "price", "release", "priority", "notes"],
                                    entry_attrs)
                if backlog_flag:
                    self.update_backlog_widgets(media_i)
                else:
                    self.update_completed_widgets(media_i)
            self.clear_error_message()
        except ValueError:
            self.set_error_message("Keep Price, Release, and Priority fields filled to make Entry")
        except KeywordInStringException:
            self.set_error_message("'=+/', '/*/', '\\n', and '?=n' cannot appear in Entry fields")

    def _remove_entry_widget(self, backlog_flag: bool, media_i: int, item_i: int):
        '''Process for removing a backlog entry as well as the widgt representing it'''
        m_list = self.controller.editor.get_shelf().get_media()[media_i]
        if backlog_flag:
            m_list.backlog.remove_item(item_i)
            self.update_backlog_widgets(media_i)
        else:
            m_list.completed.remove_item(item_i)
            self.update_completed_widgets(media_i)
        self.clear_error_message()

    def _mark_complete(self, media_i: int, item_i: int):
        '''Given the index for a Media_List in a Shelf and an Entry within that Media_List's backlog, marks the Entry
        as complete and updates Shelf_Frame view as necessary'''
        m_list = self.controller.editor.get_shelf().get_media()[media_i]
        m_list.mark_complete(item_i)
        self.destroy_content_widgets()
        self.content_widgets = self._make_entry_widgets(m_list.backlog.get_items(), True, media_i)
        self.update_backlog_widgets(media_i)
        self.clear_error_message()

    def _mark_incomplete(self, media_i: int, item_i: int):
        '''Given the index for a Media_List in a Shelf and an Entry within that Media_List's backlog, marks the Entry
        as incomplete and updates the Shelf_Frame view as necessary'''
        m_list = self.controller.editor.get_shelf().get_media()[media_i]
        m_list.mark_incomplete(item_i)
        self.destroy_content_widgets()
        self.content_widgets = self._make_entry_widgets(m_list.completed.get_items(), False, media_i)
        self.update_completed_widgets(media_i)
        self.clear_error_message()

    def update_backlog_widgets(self, media_i: int):
        '''Given the index for a Media_List in a Shelf, redraws the Entry objects of the backlog of the Media_List at
        media_i'''
        self.destroy_content_widgets()
        m_list = self.controller.editor.get_shelf().get_media()[media_i]
        self.content_widgets = self._make_entry_widgets(m_list.backlog.get_items(), True, media_i)
        self.draw_content_widgets()
        self.clear_error_message()

    def update_completed_widgets(self, media_i: int):
        '''Given the index for a Media_List in a Shelf, redraws the widgets for the Entry objects of the completed list
        of the Media_List at media_i'''
        self.destroy_content_widgets()
        m_list = self.controller.editor.get_shelf().get_media()[media_i]
        self.content_widgets = self._make_entry_widgets(m_list.completed.get_items(), False, media_i)
        self.draw_content_widgets()
        self.clear_error_message()

    def _make_entry_widgets(self, items: [entry.Entry], backlog_flag: bool, media_i: int) -> [tk.Label]:
        '''Given a list of Entry objects and a flag to indicate whether or not the items are a part of a
        Current_Backlog or Completed_List, returns a list of widgets representing the list of Entry objects'''
        result = []
        for item_i in range(len(items)):
            result.append(self._make_entry_widget(items[item_i], backlog_flag, media_i, item_i))
        return result

    def _make_entry_widget(self, item: entry.Entry, backlog_flag: bool, media_i: int, item_i: int) -> tk.Label:
        '''Given an Entry object and its index within a Media_Sublist, makes a widget to represent the Entry'''
        entry_widget = tk.Label(self.content_frame, relief=tk.GROOVE, background="white smoke", height=5)
        name = tk.Label(entry_widget, text=item.get_name(), font="helvetica 16")
        name.grid(row=0, column=0, columnspan=4, sticky=tk.N + tk.S + tk.W, padx=2)
        # Decides which set of button arguments to use
        btn_args = [("View/Edit Entry", 0, lambda: self._view_and_edit_entry(backlog_flag, media_i, item_i)),]
        if backlog_flag:
            btn_args.insert(1, ("Mark Complete", 1, lambda: self._mark_complete(media_i, item_i)))
            btn_args.insert(2, ("Remove", 2, lambda: self._remove_entry_widget(True, media_i, item_i)))
        else:
            btn_args.insert(1, ("Mark Incomplete", 1, lambda : self._mark_incomplete(media_i, item_i)))
            btn_args.insert(2, ("Remove", 2, lambda: self._remove_entry_widget(False, media_i, item_i)))
        for (text, col, funct) in btn_args:
            btn = tk.Button(entry_widget, text=text, background="gainsboro", relief=tk.GROOVE, command=funct)
            btn.grid(row=1, column=col, sticky=tk.N + tk.S + tk.E + tk.W, padx=2, pady=(0, 2))

        # Configures entry widget
        for row_i in range(2):
            entry_widget.grid_rowconfigure(row_i, weight=1)
        for col_i in range(4):
            entry_widget.grid_columnconfigure(col_i, weight=1)
        entry_widget.grid_propagate(False)
        return entry_widget


class KeywordInStringException(Exception):
    '''Exception meant to be raised when user tries to provide a string with '=+/', /*/, '\n', or '?=n' within it, which
    cannot be allowed as these strings are used as keywords within Billy/Shelf processes'''
    pass


class EmptyShelfNameException(Exception):
    '''Exception meant to be raised when user tries to provide an empty string to the user to be used as a Shelf name'''
    pass


# ROOT SET UP + MAINLOOP
if __name__ == "__main__":
    root = Billy_GUI()
    root.mainloop()

