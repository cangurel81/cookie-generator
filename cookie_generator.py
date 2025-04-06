import random
import datetime
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from tkinter import filedialog

# Realistic domain list
popular_domains = [
    "google.com", "youtube.com", "facebook.com", "twitter.com", "instagram.com",
    "amazon.com", "netflix.com", "microsoft.com", "apple.com", "linkedin.com",
    "github.com", "stackoverflow.com", "medium.com", "wikipedia.org", "reddit.com",
    "pinterest.com", "tumblr.com", "wordpress.com", "blogger.com", "mozilla.org",
    "whatsapp.com", "telegram.org", "spotify.com", "twitch.tv", "tiktok.com",
    "yahoo.com", "bing.com", "baidu.com", "yandex.com", "duckduckgo.com"
]

def get_random_domain(custom_domain=None):
    """Return a random domain or use custom domain"""
    if custom_domain and custom_domain.strip():
        return custom_domain.strip()
    return random.choice(popular_domains)

def generate_session_cookie(custom_domain=None):
    """Generate a random session cookie"""
    # Generate a random session ID
    session_id = ''.join(random.choice('0123456789abcdef') for _ in range(32))
    # Set random expiration date (1-2 days from now)
    random_days = random.uniform(1.0, 2.0)
    expiry = datetime.datetime.now() + datetime.timedelta(days=random_days)
    expiry_timestamp = int(expiry.timestamp())
    
    return {
        "domain": get_random_domain(custom_domain),
        "path": "/",
        "name": "session_id",
        "value": session_id,
        "secure": False,
        "httpOnly": True,
        "expirationDate": expiry_timestamp
    }

def generate_preference_cookie(custom_domain=None):
    """Generate a cookie with random user preferences"""
    # Random theme preference
    themes = ['light', 'dark', 'blue', 'green', 'high-contrast']
    theme = random.choice(themes)
    
    # Random language preference
    languages = ['tr', 'en', 'de', 'fr', 'es']
    language = random.choice(languages)
    
    # Set random expiration date (15-45 days from now)
    random_days = random.randint(15, 45)
    expiry = datetime.datetime.now() + datetime.timedelta(days=random_days)
    expiry_timestamp = int(expiry.timestamp())
    
    return {
        "domain": get_random_domain(custom_domain),
        "path": "/",
        "name": "preferences",
        "value": f"theme={theme}; language={language}",
        "secure": False,
        "httpOnly": False,
        "expirationDate": expiry_timestamp
    }

def generate_tracking_cookie(selected_sources=None, custom_domain=None):
    """Generate a tracking cookie with random user ID and selected sources"""
    # Generate a random user ID
    user_id = ''.join(random.choice('0123456789') for _ in range(10))
    
    # Source selection
    all_sources = ['direct', 'google', 'facebook', 'twitter', 'email', 'instagram', 'youtube', 'tiktok', 'linkedin', 'bing', 'yandex', 'duckduckgo', 'baidu', 'yahoo', 'referral']
    
    # If selected sources are specified and not empty, choose one or more randomly from them, otherwise choose a random source
    if selected_sources and len(selected_sources) > 0:
        # Choose 1-3 random sources from selected sources
        num_sources = random.randint(1, min(3, len(selected_sources)))
        random_selected = random.sample(selected_sources, num_sources)
        source = ','.join(random_selected)
    else:
        source = random.choice(all_sources)
    
    # Set random expiration date (20-60 days from now - more realistic period)
    random_days = random.randint(20, 60)
    expiry = datetime.datetime.now() + datetime.timedelta(days=random_days)
    expiry_timestamp = int(expiry.timestamp())
    
    # Suitable JSON format for Browser Automation Studio
    domain = get_random_domain(custom_domain)
    # Add dot at the beginning of domain for tracking cookies
    if not domain.startswith('.'):
        domain = '.' + domain
    
    # Create unique cookie name
    cookie_name = f"tracking_uid_{user_id}"
    
    return {
        "domain": domain,
        "path": "/",
        "name": cookie_name,
        "value": f"uid:{user_id},source:{source}",
        "secure": True,
        "httpOnly": False,
        "sameSite": "None",
        "expirationDate": expiry_timestamp
    }

import json

def save_cookies_to_file(cookies, filename='cookies.json'):
    """Save the generated cookies to a JSON file"""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(cookies, file, indent=2, ensure_ascii=False)
    
    return filename

class CookieGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cookie Generator")
        self.root.iconbitmap('cookie.ico')
        self.root.geometry("600x600")
        self.root.resizable(True, True)
        self.root.configure(padx=10, pady=10)
        
        # Create frame
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section frame (cookie type, numbers)
        top_frame = ttk.Frame(self.main_frame)
        top_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Cookie type selection
        self.cookie_type_frame = ttk.LabelFrame(top_frame, text="Cookie Type")
        self.cookie_type_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.cookie_type = tk.IntVar(value=1)
        cookie_types = [("Session Cookie", 1), ("Preference Cookie", 2), ("Tracking Cookie", 3), ("Mixed Cookies", 4)]
        
        for i, (text, value) in enumerate(cookie_types):
            ttk.Radiobutton(self.cookie_type_frame, text=text, variable=self.cookie_type, value=value).pack(side=tk.LEFT, padx=5, pady=5)
        
        # Empty frame for cookie type selection
        empty_frame = ttk.Frame(top_frame)
        empty_frame.pack(side=tk.RIGHT, fill=tk.X, padx=5)
        
        # Custom domain entry
        self.domain_frame = ttk.LabelFrame(self.main_frame, text="Custom Domains (separate multiple domains with commas)")
        self.domain_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.domain_var = tk.StringVar(value="")
        self.domain_entry = ttk.Entry(self.domain_frame, textvariable=self.domain_var)
        self.domain_entry.pack(fill=tk.X, padx=5, pady=5)
        
        # Source selection frame
        self.sources_frame = ttk.LabelFrame(self.main_frame, text="Source Selection (For Tracking Cookies)")
        self.sources_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # All sources list
        self.all_sources = ['direct', 'google', 'facebook', 'twitter', 'email', 'instagram', 'youtube', 'tiktok', 'linkedin',
                          'bing', 'yandex', 'duckduckgo', 'baidu', 'yahoo', 'referral', 'pinterest', 'reddit', 'medium',
                          'quora', 'stackoverflow', 'microsoft', 'organic']
        
        # Source selection variables
        self.source_vars = {}
        
        # Source selection checkboxes
        source_frame_inner = ttk.Frame(self.sources_frame)
        source_frame_inner.pack(fill=tk.X, padx=5, pady=5)
        
        # Create checkbox for each source (in 4 columns)
        for i, source in enumerate(self.all_sources):
            self.source_vars[source] = tk.BooleanVar(value=False)
            cb = ttk.Checkbutton(source_frame_inner, text=source, variable=self.source_vars[source])
            cb.grid(row=i//4, column=i%4, sticky=tk.W, padx=10, pady=2)
        
        # Select all/clear buttons
        select_buttons_frame = ttk.Frame(self.sources_frame)
        select_buttons_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(select_buttons_frame, text="Select All", command=self.select_all_sources).pack(side=tk.LEFT, padx=5)
        ttk.Button(select_buttons_frame, text="Clear All", command=self.clear_all_sources).pack(side=tk.LEFT, padx=5)
        
        # Enable/disable source selection when cookie type changes
        self.cookie_type.trace_add("write", lambda *args: self.toggle_source_selection())
        self.toggle_source_selection()  # Set initial state
        
        # Buttons
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, padx=5, pady=10)
        
        self.folder_button = ttk.Button(self.button_frame, text="Select Folder", command=self.select_folder)
        self.folder_button.pack(side=tk.LEFT, padx=5)
        
        self.generate_button = ttk.Button(self.button_frame, text="Generate Cookies", command=self.generate_cookies)
        self.generate_button.pack(side=tk.LEFT, padx=5)
        
        
        self.open_file_button = ttk.Button(self.button_frame, text="Open File", command=self.open_file, state=tk.DISABLED)
        self.open_file_button.pack(side=tk.LEFT, padx=5)
        
        # Numbers frame
        numbers_frame = ttk.Frame(self.main_frame)
        numbers_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Cookie count entry
        count_label_frame = ttk.LabelFrame(numbers_frame, text="Cookie Count")
        count_label_frame.pack(side=tk.LEFT, padx=5)
        
        self.count_var = tk.StringVar(value="5")
        self.count_entry = ttk.Spinbox(count_label_frame, from_=1, to=1000000, textvariable=self.count_var, width=5)
        self.count_entry.pack(padx=5, pady=2)
        
        # File count entry
        file_count_label_frame = ttk.LabelFrame(numbers_frame, text="File Count")
        file_count_label_frame.pack(side=tk.LEFT, padx=5)
        
        self.file_count_var = tk.StringVar(value="1")
        self.file_count_entry = ttk.Spinbox(file_count_label_frame, from_=1, to=1000000, textvariable=self.file_count_var, width=5)
        self.file_count_entry.pack(padx=5, pady=2)
        
        # WebAdHere Software label
        self.software_label = ttk.Label(root, text="WebAdHere Software", font=("Arial", 8), foreground="gray")
        self.software_label.pack(side=tk.BOTTOM, fill=tk.X, pady=(0, 2))
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.current_filename = None
        self.selected_folder = None
        self.set_status("Ready")
    
    def set_status(self, message):
        self.status_var.set(message)
    
    def toggle_source_selection(self):
        """Enable/disable source selection based on cookie type"""
        cookie_type = self.cookie_type.get()
        # Enable source selection if tracking cookie or mixed cookies are selected
        state = tk.NORMAL if cookie_type == 3 or cookie_type == 4 else tk.DISABLED
        
        # Only enable/disable control elements (Checkbutton)
        for source in self.all_sources:
            for widget in self.sources_frame.winfo_children():
                if isinstance(widget, ttk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Checkbutton):
                            child.configure(state=state)
                elif isinstance(widget, ttk.Button):
                    widget.configure(state=state)
    
    def select_all_sources(self):
        """Select all sources"""
        for source in self.all_sources:
            self.source_vars[source].set(True)
    
    def clear_all_sources(self):
        """Clear all source selections"""
        for source in self.all_sources:
            self.source_vars[source].set(False)
    
    def get_selected_sources(self):
        """Return selected sources as a list"""
        return [source for source in self.all_sources if self.source_vars[source].get()]
    
    def select_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.selected_folder = folder
            self.set_status(f"Selected folder: {folder}")
    
    def generate_cookies(self):
        try:
            count = int(self.count_var.get())
            file_count = int(self.file_count_var.get())
            
            if count <= 0:
                messagebox.showerror("Error", "Cookie count must be at least 1!")
                return
            
            if file_count <= 0:
                messagebox.showerror("Error", "File count must be at least 1!")
                return
            
            cookie_type = self.cookie_type.get()
            custom_domain = self.domain_var.get()
            selected_sources = self.get_selected_sources()
            
            for file_index in range(file_count):
                cookies = []
                if cookie_type == 1:  # Session cookie
                    cookies = [generate_session_cookie(custom_domain) for _ in range(count)]
                elif cookie_type == 2:  # Preference cookie
                    cookies = [generate_preference_cookie(custom_domain) for _ in range(count)]
                elif cookie_type == 3:  # Tracking cookie
                    cookies = [generate_tracking_cookie(selected_sources, custom_domain) for _ in range(count)]
                elif cookie_type == 4:  # Mixed cookies
                    for _ in range(count):
                        cookie_type_random = random.randint(1, 3)
                        if cookie_type_random == 1:
                            cookies.append(generate_session_cookie(custom_domain))
                        elif cookie_type_random == 2:
                            cookies.append(generate_preference_cookie(custom_domain))
                        else:
                            cookies.append(generate_tracking_cookie(selected_sources, custom_domain))
                
                # Create a unique name for each file and save to selected folder
                filename = f"cookies_{file_index + 1}.json"
                if self.selected_folder:
                    filename = os.path.join(self.selected_folder, filename)
                self.current_filename = save_cookies_to_file(cookies, filename)
            
            self.open_file_button.config(state=tk.NORMAL)
            self.set_status(f"{file_count} file(s) successfully created.")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")
    
    
    def open_file(self):
        if self.current_filename and os.path.exists(self.current_filename):
            os.startfile(self.current_filename)
            self.set_status(f"File '{self.current_filename}' opened.")
        else:
            messagebox.showerror("Error", "File not found!")
            self.open_file_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = CookieGeneratorApp(root)
    root.mainloop()
