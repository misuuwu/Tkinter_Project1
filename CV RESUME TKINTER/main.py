import tkinter as tk
from tkinter import ttk
import webbrowser

class ResumeApp:
    def __init__(self, master):
        self.master = master
        master.title("Curriculum Vitae")
        master.geometry("400x700") 
        # Allows both horizontal and vertical resizing
        master.resizable(True, True) 

        # --- Styling & Colors ---
        s = ttk.Style()
        s.theme_use('clam') 

        # General colors
        self.bg_color = "#f8f9fa"       
        self.primary_color = "#800000"  # MAROON
        self.text_color = "#000000"     # BLACK
        self.light_text_color = "#444444" 
        self.border_color = "#dddddd"   
        self.tag_bg = "#f0f0f0"         

        master.configure(bg=self.bg_color)
        s.configure('TFrame', background=self.bg_color)
        s.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        
        # --- Custom Font Styles ---
        s.configure('Title.TLabel', font=('Arial', 14, 'bold'), foreground=self.text_color)
        # Optimized font size for the name
        s.configure('Header.TLabel', font=('Arial', 15, 'bold'), foreground=self.text_color) 
        s.configure('Subtitle.TLabel', font=('Arial', 10), foreground=self.primary_color)
        s.configure('Body.TLabel', font=('Arial', 9), foreground=self.text_color)
        s.configure('LightBody.TLabel', font=('Arial', 9), foreground=self.light_text_color)


        # Custom style for the white "card" background
        s.configure('WhiteBackground.TFrame', background='white', relief='flat', borderwidth=0)
        s.configure('WhiteBackground.TLabel', background='white', foreground=self.text_color)

        # Connect button styling 
        s.configure('TButton', font=('Arial', 10, 'bold'), foreground='white', background=self.primary_color,
                    padding=10, relief='flat', borderwidth=0)
        s.map('TButton', background=[('active', '#660000')]) 

        # Tab Button Styling
        s.configure('Tab.TButton', background=self.bg_color, foreground=self.text_color, font=('Arial', 10),
                    relief='flat', padding=(10, 5))
        s.map('Tab.TButton',
              background=[('pressed', self.primary_color), ('active', self.border_color)],
              foreground=[('pressed', 'white'), ('active', self.text_color)],
              font=[('pressed', ('Arial', 10, 'bold'))]) 
        
        # Tag style
        s.configure('Tag.TLabel', background=self.tag_bg, foreground=self.text_color, font=('Arial', 8), padding=5)

        self.create_widgets()

    def create_widgets(self):
        # --- Top Bar Frame ---
        top_bar_frame = ttk.Frame(self.master, padding=(20, 10))
        top_bar_frame.pack(fill='x')

        ttk.Label(top_bar_frame, text="Curriculum Vitae", style='Title.TLabel').pack(side='left')
        ttk.Label(top_bar_frame, text="⬇", font=("Arial", 14), foreground=self.light_text_color).pack(side='right')

        # --- Profile Header Frame (The White Card) ---
        header_frame = ttk.Frame(self.master, padding=(20, 15), style='WhiteBackground.TFrame')
        header_frame.pack(fill='x', pady=(0, 10), padx=20) 

        # Initials Icon
        jd_label = ttk.Label(header_frame, text="AP", background=self.primary_color, foreground="white",
                             font=("Arial", 20, "bold"), anchor="center")
        jd_label.pack(side='left', padx=(0, 15), ipadx=10, ipady=10)
        jd_label.configure(width=1) 

        info_frame = ttk.Frame(header_frame, style='WhiteBackground.TFrame')
        # info_frame expands to fill the remaining space 
        info_frame.pack(side='left', fill='x', expand=True) 

        # Name 
        ttk.Label(info_frame, text="Aiko Lindsay J. Pahuyo", style='Header.TLabel', background='white').pack(anchor='w')
        
        ttk.Label(info_frame, text="Computer Science Student", style='Subtitle.TLabel', background='white').pack(anchor='w')

        bio_text = """Passionate student developer seeking opportunities to apply foundational knowledge in full-stack development. Proficient in modern programming languages and collaborative development tools."""
        # Text block remains correctly left-justified
        ttk.Label(info_frame, text=bio_text, wraplength=320, style='LightBody.TLabel', background='white', justify='left').pack(anchor='w', pady=(5, 10))

        # --- Connect button ---
        linkedin_button = ttk.Button(self.master, text="Connect on LinkedIn", command=self.open_linkedin)
        linkedin_button.pack(pady=(0, 15), padx=20, fill='x')

        # --- Tab Navigation Frame ---
        tab_nav_frame = ttk.Frame(self.master, padding=(20, 0), style='WhiteBackground.TFrame')
        tab_nav_frame.pack(fill='x', pady=(0, 10), padx=20) 

        self.tab_buttons = []
        tab_names = ["Experience", "Skills", "Education"]

        for tab_name in tab_names:
            btn = ttk.Button(tab_nav_frame, text=tab_name, style='Tab.TButton',
                             command=lambda name=tab_name: self.show_tab(name))
            btn.pack(side='left', expand=True, fill='x', padx=2, pady=5)
            self.tab_buttons.append(btn)


        # --- Content Area ---
        self.content_container_frame = ttk.Frame(self.master, padding=20, style='WhiteBackground.TFrame')
        self.content_container_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20)) 

        self.experience_frame = self.create_experience_tab(self.content_container_frame)
        self.skills_frame = self.create_skills_tab(self.content_container_frame)
        self.education_frame = self.create_education_tab(self.content_container_frame)

        self.show_tab("Experience")

    def show_tab(self, tab_name):
        # Hide all tab frames
        for frame in [self.experience_frame, self.skills_frame, self.education_frame]:
            frame.pack_forget()

        # Show the selected tab frame
        if tab_name == "Experience":
            self.experience_frame.pack(fill='both', expand=True)
        elif tab_name == "Skills":
            self.skills_frame.pack(fill='both', expand=True)
        elif tab_name == "Education":
            self.education_frame.pack(fill='both', expand=True)

        # Update button styles
        for btn in self.tab_buttons:
            if btn.cget('text') == tab_name:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])


    def create_experience_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        ttk.Label(frame, text="Full-Stack E-commerce Platform", style='Title.TLabel', background='white').pack(anchor='w')
        ttk.Label(frame, text="Personal Project / Capstone | Sept 2023 - Present", style='LightBody.TLabel', background='white').pack(anchor='w', pady=(0,5))
        
        # Bullet Points are Left-Justified
        ttk.Label(frame, text="• Developed a responsive e-commerce site using \"React, Node.js, and MongoDB\"", style='Body.TLabel', background='white', wraplength=320, justify='left').pack(anchor='w', pady=(2,0))
        ttk.Label(frame, text="• Implemented user authentication, product catalog management, and secure payment processing.", style='Body.TLabel', background='white', wraplength=320, justify='left').pack(anchor='w', pady=(2,0))
        ttk.Label(frame, text="• Utilized \"Tailwind CSS\" for modern UI/UX design.", style='Body.TLabel', background='white', wraplength=320, justify='left').pack(anchor='w', pady=(2,10))
        return frame

    def create_skills_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        # --- Programming Languages Section ---
        ttk.Label(frame, text="<> Programming Languages", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,5))
        
        # Skill Tags Frame
        skill_tag_frame_1 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        skill_tag_frame_1.pack(fill='x', anchor='w', pady=(0, 5))
        
        # Skill tags use the 'Tag.TLabel' style for a boxed look
        ttk.Label(skill_tag_frame_1, text="Python (Advanced)", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(skill_tag_frame_1, text="JavaScript (ES6+)", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(skill_tag_frame_1, text="Java", style='Tag.TLabel').pack(side='left', padx=(0, 5))

        skill_tag_frame_2 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        skill_tag_frame_2.pack(fill='x', anchor='w', pady=(0, 15))
        ttk.Label(skill_tag_frame_2, text="C++", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(skill_tag_frame_2, text="SQL / MySQL", style='Tag.TLabel').pack(side='left', padx=(0, 5))


        # --- Frontend Development Section ---
        ttk.Label(frame, text=" Frontend Development", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,5))

        # Frontend Tags Frame
        frontend_tag_frame_1 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        frontend_tag_frame_1.pack(fill='x', anchor='w', pady=(0, 5))
        
        ttk.Label(frontend_tag_frame_1, text="React", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(frontend_tag_frame_1, text="Next.js (Basics)", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(frontend_tag_frame_1, text="Tailwind CSS", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        ttk.Label(frame, text="Responsive Design", style='Tag.TLabel').pack(anchor='w', pady=(0, 5))

        return frame

    def create_education_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        # Degree/GPA
        degree_frame = ttk.Frame(frame, style='WhiteBackground.TFrame')
        degree_frame.pack(fill='x', pady=(0, 5))
        
        # --- COURSE CHANGE APPLIED HERE ---
        ttk.Label(degree_frame, text="Technical Vocation Major in Computer Harwdare Servicing", style='Title.TLabel', background='white').pack(side='left', anchor='w')
        # GPA box uses Maroon background
        ttk.Label(degree_frame, text="3.9 GPA", font=("Arial", 9, "bold"), background=self.primary_color, foreground="white").pack(side='right', padx=5, ipady=3) 

        # --- SCHOOL CHANGE APPLIED HERE ---
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
        course_tag_frame_3.pack(fill='x', anchor='w', pady=(0, 5))
        ttk.Label(course_tag_frame_3, text="Full-Stack Web Dev", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        return frame

    def open_linkedin(self):
        webbrowser.open_new("https://www.linkedin.com/in/aikopahuyo") 

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeApp(root)
    root.mainloop()