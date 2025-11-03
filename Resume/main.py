import tkinter as tk
from tkinter import ttk
# If you want to use actual images for the JD icon or download icon, 
# you will need to install Pillow: pip install Pillow
# from PIL import Image, ImageTk 
import webbrowser

class ResumeApp:
    def __init__(self, master):
        self.master = master
        master.title("Curriculum Vitae")
        master.geometry("400x700") # Mobile-like dimensions
        master.resizable(False, False) # Prevent resizing for a consistent look

        # --- Styling & Colors ---
        s = ttk.Style()
        s.theme_use('clam') # 'clam' or 'alt' often give more modern bases

        # General colors
        self.bg_color = "#f8f9fa"
        self.primary_color = "#3366ff"
        self.text_color = "#343a40"
        self.light_text_color = "#6c757d"
        self.border_color = "#e9ecef"

        master.configure(bg=self.bg_color)
        s.configure('TFrame', background=self.bg_color)
        s.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        
        # Custom styles for text
        s.configure('Bold.TLabel', font=('Arial', 12, 'bold'))
        s.configure('LargeBold.TLabel', font=('Arial', 18, 'bold'))
        s.configure('Primary.TLabel', foreground=self.primary_color)
        s.configure('Light.TLabel', foreground=self.light_text_color)
        s.configure('Small.TLabel', font=('Arial', 9))

        # Custom style for the white "card" background
        s.configure('WhiteBackground.TFrame', background='white', relief='flat', borderwidth=0)
        s.configure('WhiteBackground.TLabel', background='white')

        # Connect button styling
        s.configure('TButton', font=('Arial', 10, 'bold'), foreground='white', background=self.primary_color,
                    padding=10, relief='flat', borderwidth=0)
        s.map('TButton', background=[('active', '#2858cc')]) 

        # Tab Button Styling
        s.configure('Tab.TButton', background=self.bg_color, foreground=self.text_color, font=('Arial', 10),
                    relief='flat', padding=(10, 5))
        s.map('Tab.TButton',
              background=[('pressed', self.primary_color), ('active', self.border_color)],
              foreground=[('pressed', 'white'), ('active', self.text_color)],
              font=[('pressed', ('Arial', 10, 'bold'))]) 
        
        self.create_widgets() # Line 48

    def create_widgets(self):
        # --- Top Bar Frame ---
        top_bar_frame = ttk.Frame(self.master, padding=(20, 10))
        top_bar_frame.pack(fill='x')

        ttk.Label(top_bar_frame, text="Curriculum Vitae", font=("Arial", 14, "bold"), style='Bold.TLabel').pack(side='left')
        ttk.Label(top_bar_frame, text="⬇", font=("Arial", 14), foreground=self.light_text_color).pack(side='right')

        # --- Profile Header Frame (The White Card) ---
        header_frame = ttk.Frame(self.master, padding=(20, 15), style='WhiteBackground.TFrame')
        header_frame.pack(fill='x', pady=(0, 10), padx=20) 

        # JD Icon Placeholder (Line 94 was near here in the original code)
        jd_label = ttk.Label(header_frame, text="JD", background=self.primary_color, foreground="white",
                             font=("Arial", 20, "bold"), anchor="center")
        jd_label.pack(side='left', padx=(0, 15), ipadx=10, ipady=10)
        jd_label.configure(width=4) 

        info_frame = ttk.Frame(header_frame, style='WhiteBackground.TFrame')
        info_frame.pack(side='left', fill='x', expand=True)

        ttk.Label(info_frame, text="Alex Johnson", style='LargeBold.TLabel', background='white').pack(anchor='w')
        ttk.Label(info_frame, text="Computer Science Student", style='Primary.TLabel', background='white', font=("Arial", 10)).pack(anchor='w')

        bio_text = """Passionate student developer seeking opportunities to apply foundational knowledge in full-stack development. Proficient in modern programming languages and collaborative development tools."""
        ttk.Label(info_frame, text=bio_text, wraplength=250, font=("Arial", 9), background='white').pack(anchor='w', pady=(5, 10))

        # --- Stats Frame (6 Courses, 8 Projects, 3 Certs) ---
        stats_frame = ttk.Frame(header_frame, style='WhiteBackground.TFrame')
        stats_frame.pack(side='right', anchor='n')

        # 6 Courses
        ttk.Label(stats_frame, text="6", font=("Arial", 12, "bold"), style='WhiteBackground.TLabel').pack(anchor='e', pady=1)
        ttk.Label(stats_frame, text="Courses", font=("Arial", 8), style='WhiteBackground.TLabel', foreground=self.light_text_color).pack(anchor='e')

        # 8 Projects (HERE IS THE FIX: replaced pt=5 with pady=(5, 1))
        ttk.Label(stats_frame, text="8", font=("Arial", 12, "bold"), style='WhiteBackground.TLabel').pack(anchor='e', pady=(5, 1)) 
        ttk.Label(stats_frame, text="Projects", font=("Arial", 8), style='WhiteBackground.TLabel', foreground=self.light_text_color).pack(anchor='e')

        # 3 Certs
        ttk.Label(stats_frame, text="3", font=("Arial", 12, "bold"), style='WhiteBackground.TLabel').pack(anchor='e', pady=(5, 1))
        ttk.Label(stats_frame, text="Certs", font=("Arial", 8), style='WhiteBackground.TLabel', foreground=self.light_text_color).pack(anchor='e')

        # Connect on LinkedIn button
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
        ttk.Label(frame, text="Full-Stack E-commerce Platform", style='Bold.TLabel', background='white').pack(anchor='w')
        ttk.Label(frame, text="Personal Project / Capstone | Sept 2023 - Present", font=("Arial", 9), style='Light.TLabel', background='white').pack(anchor='w', pady=(0,5))
        ttk.Label(frame, text="• Developed a responsive e-commerce site using \"React, Node.js, and MongoDB\"", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w', pady=(2,0))
        ttk.Label(frame, text="• Implemented user authentication, product catalog management, and secure payment processing.", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w', pady=(2,0))
        ttk.Label(frame, text="• Utilized \"Tailwind CSS\" for modern UI/UX design.", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w', pady=(2,10))
        return frame

    def create_skills_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        ttk.Label(frame, text="Programming Languages", style='Bold.TLabel', background='white').pack(anchor='w', pady=(0,5))
        ttk.Label(frame, text="Python (Advanced)   JavaScript (ES6+)   Java", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w')
        ttk.Label(frame, text="C++   SQL / MySQL", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w', pady=(0, 10))

        ttk.Label(frame, text="Frontend Development", style='Bold.TLabel', background='white').pack(anchor='w', pady=(0,5))
        ttk.Label(frame, text="React   Next.js (Basics)   Tailwind CSS", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w')
        ttk.Label(frame, text="Responsive Design", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w')
        return frame

    def create_education_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        ttk.Label(frame, text="B.S. Computer Science", style='Bold.TLabel', background='white').pack(anchor='w')
        ttk.Label(frame, text="State University, School of Engineering", font=("Arial", 9), background='white').pack(anchor='w')
        ttk.Label(frame, text="Major in Software Development | Expected May 2026", font=("Arial", 9), style='Light.TLabel', background='white').pack(anchor='w', pady=(0,10))

        ttk.Label(frame, text="Key Coursework:", style='Bold.TLabel', background='white').pack(anchor='w', pady=(0,5))
        ttk.Label(frame, text="Data Structures    Algorithms & Analysis", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w')
        ttk.Label(frame, text="Operating Systems    Database Systems", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w')
        ttk.Label(frame, text="Full-Stack Web Dev", font=("Arial", 9), background='white', wraplength=320).pack(anchor='w')
        return frame

    def open_linkedin(self):
        # This function requires your system to have a web browser installed
        webbrowser.open_new("https://www.linkedin.com/in/alexjohnson") 

if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeApp(root)
    root.mainloop()