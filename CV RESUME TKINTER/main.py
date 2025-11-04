import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk 
import os 
import random 

# --- New Tooltip Class for Hover Effects ---
class Tooltip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(500, self.showtip) # Show after 500ms

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        if self.tip_window or not self.text:
            return
        
        # Get widget position
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        
        # Create tooltip window
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True) # Remove window decorations
        self.tip_window.wm_geometry(f"+{x}+{y}")
        
        label = tk.Label(self.tip_window, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tip_window
        self.tip_window = None
        if tw:
            tw.destroy()


class ResumeApp:
    def __init__(self, master):
        self.master = master
        master.title("Curriculum Vitae")
        master.resizable(True, True) 

        self.experience_images = {} 

        # --- Styling & Colors (Deep Teal Theme) ---
        s = ttk.Style()
        s.theme_use('clam') 
        
        # General colors
        self.bg_color = "#f8f9fa"       
        self.primary_color = "#008080"  # DEEP TEAL
        self.text_color = "#000000"     # BLACK
        self.light_text_color = "#444444" 
        self.border_color = "#dddddd"   
        self.tag_bg_light = "#e9ecef"   
        self.button_bg_light = "#e0ffff" 
        self.button_fg_dark = "#004040"  

        # --- List of Pastel Colors for Hover Effect ---
        self.pastel_colors = [
            "#FFC0CB",  # Pastel Pink
            "#FFA07A",  # Light Salmon/Pastel Orange
            "#F08080",  # Light Coral/Pastel Red
            "#FFFACD",  # LemonChiffon/Pastel Yellow
            "#90EE90",  # Light Green/Pastel Green
            "#ADD8E6",  # Light Blue/Pastel Blue
            "#DDA0DD",  # Plum/Pastel Purple
        ]

        master.configure(bg=self.bg_color)
        s.configure('TFrame', background=self.bg_color)
        s.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        
        # --- Custom Font Styles ---
        s.configure('Title.TLabel', font=('Arial', 14, 'bold'), foreground=self.text_color)
        s.configure('Header.TLabel', font=('Arial', 15, 'bold'), foreground=self.text_color) 
        s.configure('Subtitle.TLabel', font=('Arial', 10), foreground=self.primary_color)
        s.configure('Body.TLabel', font=('Arial', 9), foreground=self.text_color)
        s.configure('LightBody.TLabel', font=('Arial', 9), foreground=self.light_text_color)


        s.configure('WhiteBackground.TFrame', background='white', relief='flat', borderwidth=0)
        s.configure('WhiteBackground.TLabel', background='white', foreground=self.text_color)
        
        # --- Project Card Styling (CLEAN LOOK) ---
        s.configure('ProjectContainer.TFrame', background='white', borderwidth=0, relief='flat', padding=0) 
        s.configure('Project.TFrame', background='white', borderwidth=0, relief='flat', padding=(0, 15)) 
        s.configure('LastProject.TFrame', background='white', borderwidth=0, relief='flat', padding=(0, 15)) 

        s.configure('Project.TLabel', background='white', foreground=self.text_color)
        s.configure('TechUsed.TLabel', font=('Arial', 9, 'italic'), foreground=self.primary_color, background='white')
        
        # --- Skills Tag Styling (Default) ---
        s.configure('Tag.TLabel', 
                    background=self.tag_bg_light, 
                    foreground=self.text_color, 
                    font=('Arial', 9), 
                    padding=(8, 4), 
                    relief='solid', 
                    borderwidth=1, 
                    bordercolor=self.border_color 
                   )
        
        # --- Skills Tag Styling (Generic Hover Style for consistent border) ---
        s.configure('TagHover.TLabel', 
                    foreground=self.text_color, 
                    font=('Arial', 9), 
                    padding=(8, 4), 
                    relief='solid', 
                    borderwidth=1, 
                    bordercolor=self.primary_color 
                   )

        # Style for Experience Image Container 
        s.configure('ExperienceImage.TFrame', background='#f0f0f0', borderwidth=1, relief='solid', padding=10) 
        s.configure('ExperienceImage.TLabel', background='#f0f0f0') 
        
        # --- Table/Grid Styling for Activities ---
        s.configure('ActivityHeader.TLabel', font=('Arial', 9, 'bold'), foreground='black', background='white')
        s.configure('ActivityBody.TLabel', font=('Arial', 9), foreground='black', background='white')


        # --- Main Button Styling (IMPROVED RESPONSIVENESS) ---
        s.configure('TButton', font=('Arial', 10, 'bold'), foreground='white', background=self.primary_color,
                    padding=10, relief='flat', borderwidth=0)
        s.map('TButton', 
              background=[('active', '#006666'), ('pressed', '#004040')], 
              foreground=[('pressed', 'white')]
             ) 

        # Secondary button (GitHub) 
        s.configure('Secondary.TButton', font=('Arial', 10), foreground=self.primary_color, background=self.tag_bg_light,
                    padding=10, relief='flat', borderwidth=0)
        s.map('Secondary.TButton', 
              background=[('active', self.border_color), ('pressed', '#c0c0c0')], 
              foreground=[('pressed', self.primary_color)]
             )


        # Project button style
        s.configure('Project.TButton', font=('Arial', 9), foreground=self.button_fg_dark, background=self.button_bg_light,
                    relief='flat', borderwidth=0, padding=(5, 5))
        s.map('Project.TButton', 
              background=[('active', '#c0fafa'), ('pressed', '#a0e8e8')]
             )


        # --- Tab button styling (Ensuring consistency) ---
        s.configure('Tab.TButton', background='white', foreground=self.text_color, font=('Arial', 10),
                    relief='flat', padding=(10, 5))
        s.map('Tab.TButton',
              background=[('pressed', self.primary_color), ('active', self.border_color)],
              foreground=[('pressed', 'white'), ('active', self.primary_color)], 
              font=[('pressed', ('Arial', 10, 'bold')), ('active', ('Arial', 10, 'bold'))]
             )
        
        self.create_widgets()


    # --- Utility function to open links ---
    def open_link(self, url):
        webbrowser.open_new(url)

    # --- Load and Prepare Profile Photo (100x100) ---
    def load_photo(self):
        try:
            # Assuming 'my_photo.png' is available in the run directory
            original_image = Image.open("my_photo.png") 
            size = (100, 100) 
            resized_image = original_image.resize(size, Image.Resampling.LANCZOS)
            self.photo_img = ImageTk.PhotoImage(resized_image)
            return self.photo_img
        except FileNotFoundError:
            # Create a placeholder image if the file is not found
            placeholder = Image.new('RGB', (100, 100), color=self.primary_color)
            from PIL import ImageDraw, ImageFont # Local import for placeholder
            d = ImageDraw.Draw(placeholder)
            try:
                # Use a system font or default font
                font = ImageFont.truetype("arial.ttf", 40)
            except IOError:
                font = ImageFont.load_default()
            d.text((15, 20), "AP", fill="white", font=font)
            self.photo_img = ImageTk.PhotoImage(placeholder)
            return self.photo_img
        except Exception:
            return None
            
    # --- Load and Prepare Experience Images (INCREASED SIZE) ---
    def load_experience_image(self, file_name, width=400, height=300): 
        try:
            if not os.path.exists(file_name):
                 return ImageTk.PhotoImage(Image.new('RGB', (width, height), color='lightgray'))
                 
            original_image = Image.open(file_name) 
            original_width, original_height = original_image.size
            ratio = min(width / original_width, height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_image.size[1] * ratio) 
            
            resized_image = original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            final_image = Image.new('RGB', (width, height), color='#f0f0f0') 
            paste_x = (width - new_width) // 2
            paste_y = (height - new_height) // 2
            final_image.paste(resized_image, (paste_x, paste_y))

            self.experience_images[file_name] = ImageTk.PhotoImage(final_image)
            return self.experience_images[file_name]
            
        except Exception:
            return None
            
    # --- New method to dynamically set the wraplength ---
    def on_info_frame_resize(self, event):
        new_wraplength = event.width - 10 
        if new_wraplength > 1:
             self.profile_summary_label.config(wraplength=new_wraplength)

    def on_canvas_configure(self, event):
        # Update the canvas window size to match the canvas width
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)


    def create_widgets(self):
        # --- CV Download Link (UPDATED with the user's provided link) ---
        self.cv_download_url = "https://github.com/misuuwu/Tkinter_Project1"
        
        # --- SCROLLABLE SETUP START ---
        
        self.canvas = tk.Canvas(self.master, bg=self.bg_color, highlightthickness=0)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.main_content_frame = ttk.Frame(self.canvas, style='TFrame', width=400) 
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.main_content_frame, anchor="nw")

        self.main_content_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        ))
        self.canvas.bind('<Configure>', self.on_canvas_configure) 

        # --- SCROLLABLE CONTENT START ---
        
        # --- Top Bar Frame ---
        top_bar_frame = ttk.Frame(self.main_content_frame, padding=(20, 10))
        top_bar_frame.pack(fill='x')
        
        # Container for Title and Button (left-aligned title, right-aligned button)
        title_button_frame = ttk.Frame(top_bar_frame, style='TFrame')
        title_button_frame.pack(fill='x')
        
        # Title Label
        ttk.Label(title_button_frame, text="Curriculum Vitae", style='Title.TLabel').pack(side='left')
        
        # --- Download CV Button ---
        download_button = ttk.Button(
            title_button_frame, 
            text="⬇ Download CV", 
            style='TButton',
            command=lambda: self.open_link(self.cv_download_url)
        )
        download_button.pack(side='right')
        Tooltip(download_button, "Open the linked GitHub repository in a new window.")

        # --- Profile Header Frame (The White Card) ---
        header_frame = ttk.Frame(self.main_content_frame, padding=(20, 15), style='WhiteBackground.TFrame')
        header_frame.pack(fill='x', pady=(0, 10), padx=20) 
        
        header_frame.grid_columnconfigure(0, weight=0) 
        header_frame.grid_columnconfigure(1, weight=1) 

        # --- PHOTO INTEGRATION / FALLBACK ---
        photo = self.load_photo()
        if photo:
            photo_label = ttk.Label(header_frame, image=photo, background='white')
            photo_label.grid(row=0, column=0, rowspan=3, padx=(0, 15), sticky='n')
            photo_label.image = photo 
        else:
            jd_label = ttk.Label(header_frame, text="AP", background=self.primary_color, foreground="white",
                                 font=("Arial", 20, "bold"), anchor="center")
            jd_label.grid(row=0, column=0, rowspan=3, padx=(0, 15), ipady=10, sticky='n')
            jd_label.configure(width=1) 


        # --- Info Frame (Text container) ---
        info_frame = ttk.Frame(header_frame, style='WhiteBackground.TFrame')
        info_frame.grid(row=0, column=1, rowspan=3, sticky='nsew')
        
        # Name 
        ttk.Label(info_frame, text="Aiko Lindsay J. Pahuyo", style='Header.TLabel', background='white').pack(anchor='w')
        
        ttk.Label(info_frame, text="Computer Science Student", style='Subtitle.TLabel', background='white').pack(anchor='w')

        # --- Combined Bio and Objective ---
        combined_text = """Passionate student developer seeking opportunities to apply foundational knowledge in full-stack development. Proficient in modern programming languages and collaborative development tools. I aim to explore different work environments to gain hands-on experience and learn new skills. By doing so, I hope to enhance my professional growth and shape my future career path. I want to help my team and company by taking on new challenges, learning new things, and working together with my colleagues to reach our goals."""
        
        self.profile_summary_label = ttk.Label(
            info_frame, 
            text=combined_text, 
            style='LightBody.TLabel', 
            background='white', 
            justify='left'
        )
        self.profile_summary_label.pack(anchor='w', fill='x', pady=(5, 10))

        info_frame.bind('<Configure>', self.on_info_frame_resize)


        # --- Connect buttons Frame (CENTERED) ---
        button_frame = ttk.Frame(self.main_content_frame, style='TFrame')
        button_frame.pack(pady=(0, 15), padx=20, fill='x') 
        
        inner_button_frame = ttk.Frame(button_frame, style='TFrame')
        inner_button_frame.pack(anchor='center') 

        # 1. LinkedIn Button (Primary)
        linkedin_button = ttk.Button(
            inner_button_frame, 
            text="Connect on LinkedIn", 
            style='TButton',
            command=lambda: self.open_link("https://www.linkedin.com/in/aiko-pahuyo-196191373/") 
        )
        linkedin_button.pack(side='left', padx=(0, 10)) 
        Tooltip(linkedin_button, "View Aiko's professional network and experience.")


        # 2. GitHub Button (Secondary)
        github_button = ttk.Button(
            inner_button_frame, 
            text="GitHub", 
            style='Secondary.TButton',
            command=lambda: self.open_link("https://github.com/misuuwu") 
        )
        github_button.pack(side='left') 
        Tooltip(github_button, "Explore Aiko's code repositories and projects.")


        # --- Tab Navigation Frame ---
        tab_nav_frame = ttk.Frame(self.main_content_frame, padding=(20, 0), style='WhiteBackground.TFrame')
        tab_nav_frame.pack(fill='x', pady=(0, 10), padx=20) 

        self.tab_buttons = []
        tab_names = ["Experience", "Projects", "Skills", "Education"]

        for tab_name in tab_names:
            btn = ttk.Button(tab_nav_frame, text=tab_name, style='Tab.TButton',
                             command=lambda name=tab_name: self.show_tab(name))
            btn.pack(side='left', expand=True, fill='x', padx=2, pady=5)
            self.tab_buttons.append(btn)


        # --- Content Area ---
        # This container holds the active tab content
        self.content_container_frame = ttk.Frame(self.main_content_frame, padding=(20, 0), style='TFrame')
        self.content_container_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20)) 

        self.experience_frame = self.create_experience_tab(self.content_container_frame)
        self.projects_frame = self.create_projects_tab(self.content_container_frame) 
        self.skills_frame = self.create_skills_tab(self.content_container_frame)
        self.education_frame = self.create_education_tab(self.content_container_frame)

        self.show_tab("Experience")
        
        # --- SCROLLABLE SETUP END ---
        

    def show_tab(self, tab_name):
        # Hide all tab frames
        for frame in [self.experience_frame, self.projects_frame, self.skills_frame, self.education_frame]:
            frame.pack_forget()

        # Show the selected tab frame
        if tab_name == "Experience":
            self.experience_frame.pack(fill='both', expand=True)
        elif tab_name == "Projects":
            self.projects_frame.pack(fill='both', expand=True)
        elif tab_name == "Skills":
            self.skills_frame.pack(fill='both', expand=True)
        elif tab_name == "Education":
            self.education_frame.pack(fill='both', expand=True)

        # Update button styles
        for btn in self.tab_buttons:
            if btn.cget('text') == tab_name:
                btn.state(['pressed', '!active']) 
                btn.configure(style='Tab.TButton')
            else:
                btn.state(['!pressed'])
                
        # Reconfigure scroll region after changing tab content
        self.master.update_idletasks() 
        self.canvas.config(scrollregion=self.canvas.bbox("all"))


    # --- Project Card Creation Helper ---
    def create_project_card(self, parent_frame, title, description, tech_used, repo_link, is_last=False):
        # Determine the style based on whether it is the last card
        style_name = 'LastProject.TFrame' if is_last else 'Project.TFrame'
        
        # Card frame for the whole project entry
        card_frame = ttk.Frame(parent_frame, style=style_name)
        card_frame.pack(fill='x', expand=True, pady=0) 

        # Content Frame to hold all the text and button, and apply inner left/right padding
        content_frame = ttk.Frame(card_frame, style='WhiteBackground.TFrame') 
        # MODIFICATION: Increased padding for a cleaner look
        content_frame.pack(fill='x', padx=20, pady=(15, 0)) 

        content_frame.columnconfigure(0, weight=1) 
        
        # Row 0: Title 
        ttk.Label(content_frame, text=title, font=('Arial', 11, 'bold'), style='Project.TLabel').grid(row=0, column=0, sticky='w', pady=(0, 2))
        # Row 1: Tech Used
        ttk.Label(content_frame, text=tech_used, style='TechUsed.TLabel').grid(row=1, column=0, sticky='w', pady=(0, 8))
        
        # Row 2: Description 
        ttk.Label(content_frame, text=description, wraplength=550, style='Body.TLabel', background='white', justify='left').grid(row=2, column=0, sticky='w', pady=(0, 10))

        # Row 3: Button (Centered button text)
        ttk.Button(content_frame, text="<> View Repository", style='Project.TButton', 
                   command=lambda: self.open_link(repo_link)).grid(row=3, column=0, sticky='w') # kept left aligned for consistency with text
        
        # If not the last card, apply a separator widget
        if not is_last:
            separator = ttk.Separator(card_frame, orient='horizontal')
            # Place it at the very bottom of the card, filling the width
            separator.pack(fill='x', side='bottom', pady=(15, 0), padx=20) # Apply horizontal padding to separator

        return card_frame

    # --- Experience Tab Content ---
    def create_experience_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        ttk.Label(frame, text="Project Visuals", style='Subtitle.TLabel', foreground=self.primary_color, background='white').pack(anchor='w', pady=(10, 5))
        
        # Container for the three image cards 
        all_images_wrapper_frame = ttk.Frame(frame, style='WhiteBackground.TFrame')
        all_images_wrapper_frame.pack(fill='x', pady=(0, 10))
        
        all_images_wrapper_frame.columnconfigure(0, weight=1)
        all_images_wrapper_frame.columnconfigure(1, weight=1)
        all_images_wrapper_frame.columnconfigure(2, weight=1)
        
        
        # 1. E-commerce Image Card (Column 0)
        ecommerce_card_frame = ttk.Frame(all_images_wrapper_frame, style='ExperienceImage.TFrame')
        ecommerce_card_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        
        ecommerce_img = self.load_experience_image("ecommerce_project.png") 
        if ecommerce_img:
            ttk.Label(ecommerce_card_frame, image=ecommerce_img, style='ExperienceImage.TLabel').pack()


        # 2. Flutter Image Card (Column 1)
        flutter_card_frame = ttk.Frame(all_images_wrapper_frame, style='ExperienceImage.TFrame')
        flutter_card_frame.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        
        flutter_img = self.load_experience_image("flutter_project.png") 
        if flutter_img:
            ttk.Label(flutter_card_frame, image=flutter_img, style='ExperienceImage.TLabel').pack()


        # 3. Blender Image Card (Column 2)
        blender_card_frame = ttk.Frame(all_images_wrapper_frame, style='ExperienceImage.TFrame')
        blender_card_frame.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
        
        blender_img = self.load_experience_image("blender_project.png") 
        if blender_img:
            ttk.Label(blender_card_frame, image=blender_img, style='ExperienceImage.TLabel').pack()

        return frame

    # --- Projects Tab Content ---
    def create_projects_tab(self, parent_frame):
        # Use WhiteBackground.TFrame for the whole tab content area
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame') 
        
        # Project Title
        ttk.Label(frame, text="My Featured Projects", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,10))

        # --- Projects Container Frame (Fixed: No hard border, just a clean wrapper) ---
        projects_container = ttk.Frame(frame, style='ProjectContainer.TFrame')
        projects_container.pack(fill='x', pady=0) 
        
        # E-Commerce Platform
        self.create_project_card(
            projects_container,
            title="E-Commerce Platform (Mobile & Web)",
            description="A fully functional mobile-first e-commerce application demonstrating robust front-end architecture, product catalog viewing, and dynamic cart management. Focus was placed on clean, reusable UI components and accessibility. This project was a key capstone experience.",
            tech_used="React, Node.js, MongoDB (MERN Stack), Tailwind CSS",
            repo_link="https://github.com/misuuwu/Ecommerce-API"
        )
        
        # Expense-Tracker
        self.create_project_card(
            projects_container,
            title="Expense-Tracker",
            description="A modern personal finance tool built to help users monitor and categorize daily expenditures. Features include real-time data visualization, local storage integration for persistence, and robust input validation using TypeScript.",
            tech_used="React, TypeScript, Modern Hooks, Chart.js",
            repo_link="https://github.com/Pragmatyst/Expense-Tracker"
        )
        
        # Flashwise V1 (LAST CARD)
        self.create_project_card(
            projects_container,
            title="Flashwise V1 (Study Companion)",
            description="An interactive study application designed to gamify the learning process using flashcards and spaced repetition logic. The desktop application aims to increase knowledge retention and engagement for various subjects.",
            tech_used="Python, Tkinter, Data Persistence (JSON)",
            repo_link="https://github.com/misuuwu/Flashwise_V1",
            is_last=True 
        )
        
        return frame


    # --- Skills Tab Content (FINAL REFINED with Multi-Color Hover) ---
    def create_skills_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        # --- Dynamic Hover Functions ---
        def on_enter(event):
            # Select a random pastel color
            random_color = random.choice(self.pastel_colors)
            # Apply the generic hover style and set the specific background color
            event.widget.configure(style='TagHover.TLabel', background=random_color)
        
        def on_leave(event):
            # Revert to the default tag style
            event.widget.configure(style='Tag.TLabel')

        # Helper to create a skill tag and bind hover events
        def create_hover_tag(parent, text):
            tag_label = ttk.Label(parent, text=text, style='Tag.TLabel')
            tag_label.pack(side='left', padx=(0, 5))
            tag_label.bind("<Enter>", on_enter)
            tag_label.bind("<Leave>", on_leave)
            return tag_label


        # --- Technical Skills Section ---
        ttk.Label(frame, text="<> Technical Skills", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,5))
        
        # Languages Group 
        ttk.Label(frame, text="Languages:", style='Subtitle.TLabel', background='white', foreground=self.light_text_color).pack(anchor='w', pady=(5, 5))

        # Skill Tags Frame 1 (Languages)
        skill_tag_frame_1 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        skill_tag_frame_1.pack(fill='x', anchor='w', pady=(0, 10))
        
        create_hover_tag(skill_tag_frame_1, "Python (Advanced)")
        create_hover_tag(skill_tag_frame_1, "JavaScript (ES6+)")
        create_hover_tag(skill_tag_frame_1, "Java")
        create_hover_tag(skill_tag_frame_1, "C++")
        create_hover_tag(skill_tag_frame_1, "SQL / MySQL")
        
        skill_tag_frame_1_b = ttk.Frame(frame, style='WhiteBackground.TFrame')
        skill_tag_frame_1_b.pack(fill='x', anchor='w', pady=(0, 10))
        
        create_hover_tag(skill_tag_frame_1_b, "Filipino (Native)")
        create_hover_tag(skill_tag_frame_1_b, "English (Proficient)")


        # Frameworks/Tools Group 
        ttk.Label(frame, text="Frameworks & Tools:", style='Subtitle.TLabel', background='white', foreground=self.light_text_color).pack(anchor='w', pady=(5, 5))

        # Frontend Tags Frame 2
        frontend_tag_frame_1 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        frontend_tag_frame_1.pack(fill='x', anchor='w', pady=(0, 10))
        
        create_hover_tag(frontend_tag_frame_1, "React")
        create_hover_tag(frontend_tag_frame_1, "Node.js")
        create_hover_tag(frontend_tag_frame_1, "Tailwind CSS")
        create_hover_tag(frontend_tag_frame_1, "MongoDB")
        
        frontend_tag_frame_2 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        frontend_tag_frame_2.pack(fill='x', anchor='w', pady=(0, 15))
        
        create_hover_tag(frontend_tag_frame_2, "Git/GitHub")
        create_hover_tag(frontend_tag_frame_2, "REST APIs")
        create_hover_tag(frontend_tag_frame_2, "TypeScript")
        create_hover_tag(frontend_tag_frame_2, "C# (Advanced)")
        create_hover_tag(frontend_tag_frame_2, "Web Development (Intermediate)")

        
        # --- Separator for Soft Skills ---
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)


        # --- Soft Skills Section (UPDATED with Hover) ---
        ttk.Label(frame, text="🤝 Soft Skills", style='Title.TLabel', background='white').pack(anchor='w', pady=(10, 5))

        # Soft Skills Tags Frame
        soft_skill_tag_frame = ttk.Frame(frame, style='WhiteBackground.TFrame')
        soft_skill_tag_frame.pack(fill='x', anchor='w', pady=(0, 10))
        
        create_hover_tag(soft_skill_tag_frame, "Team Collaboration")
        create_hover_tag(soft_skill_tag_frame, "Problem Solving")
        create_hover_tag(soft_skill_tag_frame, "Adaptability")
        create_hover_tag(soft_skill_tag_frame, "Time Management")

        soft_skill_tag_frame_2 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        soft_skill_tag_frame_2.pack(fill='x', anchor='w', pady=(0, 10))
        
        create_hover_tag(soft_skill_tag_frame_2, "Communication")
        create_hover_tag(soft_skill_tag_frame_2, "Organized")
        
        return frame


    # --- Education Tab Content ---
    def create_education_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        # --- 1. Current/Highest Education Header Frame ---
        degree_frame = ttk.Frame(frame, style='WhiteBackground.TFrame')
        degree_frame.pack(fill='x', pady=(0, 5))
        
        degree_frame.columnconfigure(0, weight=1) 
        degree_frame.columnconfigure(1, weight=0) 
        
        # Course Title
        ttk.Label(
            degree_frame, 
            text="Technical Vocation Major in Computer Harwdare Servicing", 
            style='Title.TLabel', 
            background='white'
        ).grid(row=0, column=0, sticky='w')
        
        # GPA box 
        tk.Label(
            degree_frame, 
            text="3.9 GPA", 
            font=("Arial", 9, "bold"), 
            background=self.primary_color, 
            foreground="white",
            padx=5, 
            pady=3
        ).grid(row=0, column=1, sticky='e') 

        # School
        ttk.Label(frame, text="Technological University of the Philippines", style='Body.TLabel', background='white').pack(anchor='w')
        ttk.Label(frame, text="Major in Software Development | Expected May 2026", style='LightBody.TLabel', background='white').pack(anchor='w', pady=(0,15))

        # Key Coursework
        ttk.Label(frame, text="Key Coursework:", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,5))
        
        # Coursework Tags (Use Tag.TLabel style)
        course_tag_frame_1 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        course_tag_frame_1.pack(fill='x', anchor='w', pady=(0, 5))
        
        ttk.Label(course_tag_frame_1, text="Data Structures", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(course_tag_frame_1, text="Algorithms & Analysis", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        course_tag_frame_2 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        course_tag_frame_2.pack(fill='x', anchor='w', pady=(0, 5))
        
        ttk.Label(course_tag_frame_2, text="Operating Systems", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(course_tag_frame_2, text="Database Systems", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        course_tag_frame_3 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        course_tag_frame_3.pack(fill='x', anchor='w', pady=(0, 15))
        ttk.Label(course_tag_frame_3, text="Full-Stack Web Dev", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        
        # --- Separator before Activities ---
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=15)
        
        
        # --- 2. Extra-Curricular Activities ---
        ttk.Label(frame, text="⭐ Extra-Curricular Activities", style='Title.TLabel', background='white').pack(anchor='w', pady=(0, 10))
        
        # Container for the activities table structure
        activities_frame = ttk.Frame(frame, style='WhiteBackground.TFrame')
        activities_frame.pack(fill='x', padx=5, pady=(0, 20)) 
        
        activities_frame.columnconfigure(0, weight=0) # Dates column
        activities_frame.columnconfigure(1, weight=1) # Organization column
        activities_frame.columnconfigure(2, weight=1) # Position column
        
        # --- Headers ---
        ttk.Label(activities_frame, text="Inclusive Dates:", style='ActivityHeader.TLabel', anchor='w').grid(row=0, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(activities_frame, text="Name of Organization:", style='ActivityHeader.TLabel', anchor='w').grid(row=0, column=1, padx=5, pady=5, sticky='w')
        ttk.Label(activities_frame, text="Position:", style='ActivityHeader.TLabel', anchor='w').grid(row=0, column=2, padx=5, pady=5, sticky='w')
        
        # Separator Line
        ttk.Separator(activities_frame, orient='horizontal').grid(row=1, column=0, columnspan=3, sticky='ew')
        
        # --- Activity 1 ---
        ttk.Label(activities_frame, text="2023 - 2024", style='ActivityBody.TLabel', anchor='w').grid(row=2, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(activities_frame, text="Alliance of Arts and Design Club", style='ActivityBody.TLabel', anchor='w').grid(row=2, column=1, padx=5, pady=5, sticky='w')
        ttk.Label(activities_frame, text="Seargent of Arms", style='ActivityBody.TLabel', anchor='w').grid(row=2, column=2, padx=5, pady=5, sticky='w')

        # Separator Line
        ttk.Separator(activities_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='ew')

        # --- Activity 2 ---
        ttk.Label(activities_frame, text="2023 - 2024", style='ActivityBody.TLabel', anchor='w').grid(row=4, column=0, padx=5, pady=5, sticky='w')
        ttk.Label(activities_frame, text="SeaUniversity", style='ActivityBody.TLabel', anchor='w').grid(row=4, column=1, padx=5, pady=5, sticky='w')
        ttk.Label(activities_frame, text="Game Developer", style='ActivityBody.TLabel', anchor='w').grid(row=4, column=2, padx=5, pady=5, sticky='w')


        # --- Separator before Academic Achievements ---
        ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=15)

        
        # --- 3. Academic Achievements ---
        ttk.Label(frame, text="🥇 Academic Achievements", style='Title.TLabel', background='white').pack(anchor='w', pady=(0, 10))
        
        # STI College Pasay-EDSA Section
        ttk.Label(frame, text="STI College Pasay-EDSA:", style='Subtitle.TLabel', background='white', foreground=self.light_text_color).pack(anchor='w')
        ttk.Label(frame, text="• **With Honor** (2022 - 2024)", style='Body.TLabel', justify='left', background='white').pack(anchor='w', padx=10)
        
        # Pasay City East High School Section
        ttk.Label(frame, text="Pasay City East High School:", style='Subtitle.TLabel', background='white', foreground=self.light_text_color).pack(anchor='w', pady=(10, 0))
        ttk.Label(frame, text="• **With High Honors** (2018 - 2022)", style='Body.TLabel', justify='left', background='white').pack(anchor='w', padx=10, pady=(0, 10))

        return frame


if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeApp(root)
    root.mainloop()