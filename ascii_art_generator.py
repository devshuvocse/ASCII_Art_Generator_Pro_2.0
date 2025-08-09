import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageEnhance, ImageFilter, ImageTk, ImageOps
import numpy as np
import threading
import os

# --- ASCII Character Sets ---
# Using dictionaries for easier access and potential expansion
ASCII_SETS = {
    "Detailed": list("█▉▊▋▌▍▎▏ "),
    "Classic": list("@%#*+=-:. "),
    "Blocks": list("██▓▒░ "),
    "Lines": list("≡+=:-. "),
    "Dots": list("●◐◑◒◓○⚬⚪ "),
    "Braille": list("⣿⣾⣽⣻⣟⣯⣷⣶⣴⣲⣱⣰⣠⣀ "),
}

class ToolTip:
    """
    Create a tooltip for a given widget.
    """
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip_window = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)
        self.tooltip_window.wm_geometry(f"+{x}+{y}")

        label = tk.Label(self.tooltip_window, text=self.text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("Segoe UI", 8, "normal"), padx=5, pady=5)
        label.pack(ipadx=1)

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
        self.tooltip_window = None

class ASCIIArtGeneratorApp:
    """
    The main application class for the Super Realistic ASCII Art Generator Pro.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Super Realistic ASCII Art Generator Pro 2.0")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')

        # --- Instance Variables ---
        self.ascii_art_data = ""
        self.original_image = None
        self.processed_image_for_preview = None
        self.is_processing = False
        self.file_path = None
        self.canvas = None # To hold the scrollable canvas

        self._setup_styles()
        self._create_variables()
        self._create_widgets()
        self._display_welcome_message()

    def _setup_styles(self):
        """Configure styles for ttk widgets."""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#ecf0f1', borderwidth=0)
        style.configure('TNotebook.Tab', background='#bdc3c7', foreground='#2c3e50', padding=[10, 5], font=('Segoe UI', 10, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', '#3498db')], foreground=[('selected', 'white')])
        style.configure('Modern.TCombobox', fieldbackground='white', background='#3498db')
        style.configure('TProgressbar', thickness=20, background='#27ae60', troughcolor='#34495e')
        style.configure('Vertical.TScrollbar', background='#bdc3c7', troughcolor='#ecf0f1', arrowcolor='#2c3e50')


    def _create_variables(self):
        """Initialize all tk variables for settings."""
        self.width_var = tk.IntVar(value=120)
        self.brightness_var = tk.DoubleVar(value=1.0)
        self.contrast_var = tk.DoubleVar(value=1.0)
        self.sharpness_var = tk.DoubleVar(value=1.0)
        self.saturation_var = tk.DoubleVar(value=1.0)
        self.remove_bg_var = tk.BooleanVar(value=False)
        self.bg_threshold_var = tk.IntVar(value=240)
        self.bg_feather_var = tk.IntVar(value=5)
        self.effects_var = tk.StringVar(value='enhance')
        self.char_set_var = tk.StringVar(value='Detailed')
        self.adaptive_var = tk.BooleanVar(value=True)
        self.dithering_var = tk.BooleanVar(value=False)
        self.detail_var = tk.BooleanVar(value=True)
        self.aspect_var = tk.BooleanVar(value=True)
        self.color_mode_var = tk.StringVar(value='weighted')
        self.color_channel_var = tk.StringVar(value='red')
        self.double_width_var = tk.BooleanVar(value=False)
        self.spacing_var = tk.BooleanVar(value=False)
        self.reverse_var = tk.BooleanVar(value=False)
        self.smart_bg_var = tk.BooleanVar(value=True)
        self.border_var = tk.BooleanVar(value=False)
        self.border_char_var = tk.StringVar(value='█')
        self.theme_var = tk.StringVar(value='matrix')
        self.color_ascii_var = tk.BooleanVar(value=False)

    def _create_widgets(self):
        """Create and layout all the widgets for the application."""
        # --- Main Layout ---
        header_frame = tk.Frame(self.root, bg='#34495e', height=80)
        header_frame.pack(fill='x', side='top')
        header_frame.pack_propagate(False)

        main_container = tk.Frame(self.root, bg='#2c3e50')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)

        control_frame = tk.Frame(main_container, bg='#ecf0f1', width=380)
        control_frame.pack(side='left', fill='y', padx=(0, 5))
        control_frame.pack_propagate(False)

        content_frame = tk.Frame(main_container, bg='#ffffff')
        content_frame.pack(side='right', fill='both', expand=True, padx=(5, 0))

        status_frame = tk.Frame(self.root, bg='#34495e', height=40)
        status_frame.pack(fill='x', side='bottom')
        status_frame.pack_propagate(False)

        # --- Header ---
        tk.Label(header_frame, text="🎨 SUPER REALISTIC ASCII ART GENERATOR PRO 2.0", font=('Segoe UI', 20, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(10,0))
        tk.Label(header_frame, text="Now with AI-Powered Color Conversion and Advanced Image Processing", font=('Segoe UI', 11), fg='#bdc3c7', bg='#34495e').pack()

        # --- Scrollable Control Panel ---
        self.canvas = tk.Canvas(control_frame, bg='#ecf0f1', highlightthickness=0)
        scrollbar = ttk.Scrollbar(control_frame, orient="vertical", command=self.canvas.yview, style='Vertical.TScrollbar')
        scrollable_frame = tk.Frame(self.canvas, bg='#ecf0f1')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

        # --- Widgets inside the scrollable frame ---
        # File selection section
        file_frame = tk.Frame(scrollable_frame, bg='#ecf0f1')
        file_frame.pack(fill='x', pady=10, padx=15)
        tk.Label(file_frame, text="📁 File & Preview", font=('Segoe UI', 12, 'bold'), bg='#ecf0f1', fg='#2c3e50').pack(anchor='w')
        
        tk.Button(file_frame, text="📂 Select Image", command=self.open_file, relief='flat', bg='#3498db', fg='white', font=('Segoe UI', 10, 'bold'), cursor='hand2').pack(pady=5, fill='x')
        self.file_label = tk.Label(file_frame, text="No file selected", font=('Segoe UI', 9), bg='#ecf0f1', fg='#7f8c8d')
        self.file_label.pack(pady=2)
        self.info_label = tk.Label(file_frame, text="", font=('Segoe UI', 8), bg='#ecf0f1', fg='#95a5a6')
        self.info_label.pack(pady=2)
        
        self.preview_label = tk.Label(file_frame, text="Image Preview", bg='white', relief='sunken', bd=1)
        self.preview_label.pack(pady=10, fill='x', expand=True)

        # Settings organized into a Notebook (Tabs)
        notebook = ttk.Notebook(scrollable_frame)
        notebook.pack(fill='both', expand=True, padx=10, pady=5)

        self._create_settings_tabs(notebook)

        # --- Content Area (ASCII Output) ---
        output_frame = tk.Frame(content_frame, bg='#ffffff')
        output_frame.pack(fill='both', expand=True, padx=15, pady=15)

        tk.Label(output_frame, text="🎨 ASCII ART OUTPUT", font=('Segoe UI', 14, 'bold'), bg='#ffffff', fg='#2c3e50').pack(anchor='w', pady=(0, 10))

        self.text_area = scrolledtext.ScrolledText(output_frame, wrap=tk.NONE, font=('Consolas', 9), bg='#1e1e1e', fg='#00ff00', insertbackground='white', selectbackground='#3498db', relief='flat', bd=0)
        self.text_area.pack(fill='both', expand=True)

        # --- Status Bar ---
        self.status_label = tk.Label(status_frame, text="🚀 Ready to create!", font=('Segoe UI', 10), bg='#34495e', fg='#ecf0f1')
        self.status_label.pack(side='left', padx=15)
        self.stats_label = tk.Label(status_frame, text="", font=('Segoe UI', 9), bg='#34495e', fg='#bdc3c7')
        self.stats_label.pack(side='right', padx=15)
        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate', length=200, style='TProgressbar')
        self.progress_bar.pack(side='right', padx=15)

    def _on_mousewheel(self, event):
        """Cross-platform mouse wheel scrolling for the control panel."""
        if self.canvas.yview() == (0.0, 1.0):
            return
            
        # For Windows and macOS, event.delta is used.
        # For Linux, event.num is 4 for scroll up and 5 for scroll down.
        if hasattr(event, 'delta') and event.delta != 0:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif hasattr(event, 'num'):
            if event.num == 4:
                self.canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(1, "units")


    def _create_settings_tabs(self, notebook):
        """Create and populate the tabs for the settings panel."""
        tab_basic = ttk.Frame(notebook, style='TFrame')
        tab_enhance = ttk.Frame(notebook, style='TFrame')
        tab_advanced = ttk.Frame(notebook, style='TFrame')
        tab_style = ttk.Frame(notebook, style='TFrame')
        tab_actions = ttk.Frame(notebook, style='TFrame')

        notebook.add(tab_basic, text='Basic')
        notebook.add(tab_enhance, text='Enhance')
        notebook.add(tab_advanced, text='Advanced')
        notebook.add(tab_style, text='Style')
        notebook.add(tab_actions, text='Actions')

        # --- Basic Settings Tab ---
        self._create_control(tab_basic, "Width:", self.width_var, 50, 500, 'scale', "Width of the generated ASCII art in characters.")
        self._create_control(tab_basic, "Character Set:", self.char_set_var, list(ASCII_SETS.keys()), None, 'combo', "The set of characters used to render the image.")
        self._create_control(tab_basic, "Effects:", self.effects_var, ['none', 'enhance', 'smooth', 'edge', 'artistic', 'dramatic'], None, 'combo', "Apply a pre-processing effect to the image.")
        self._create_control(tab_basic, "🌈 Generate Color ASCII", self.color_ascii_var, None, None, 'check', "Generate ASCII art using the original image colors.")
        
        # --- Enhancement Tab ---
        self._create_control(tab_enhance, "Brightness:", self.brightness_var, 0.1, 3.0, 'scale', "Adjust image brightness.")
        self._create_control(tab_enhance, "Contrast:", self.contrast_var, 0.1, 3.0, 'scale', "Adjust image contrast.")
        self._create_control(tab_enhance, "Sharpness:", self.sharpness_var, 0.1, 3.0, 'scale', "Adjust image sharpness.")
        self._create_control(tab_enhance, "Saturation:", self.saturation_var, 0.1, 3.0, 'scale', "Adjust color saturation (for color ASCII).")

        # --- Advanced Tab ---
        self._create_control(tab_advanced, "Remove Background", self.remove_bg_var, None, None, 'check', "Intelligently remove the image background.")
        self._create_control(tab_advanced, "BG Threshold:", self.bg_threshold_var, 1, 255, 'scale', "Sensitivity for background detection.")
        self._create_control(tab_advanced, "BG Feather:", self.bg_feather_var, 0, 20, 'scale', "Smooth the edges of the background removal.")
        self._create_control(tab_advanced, "Adaptive Mapping", self.adaptive_var, None, None, 'check', "Use histogram equalization for better contrast.")
        self._create_control(tab_advanced, "Dithering", self.dithering_var, None, None, 'check', "Simulate more shades of gray for smoother gradients.")
        self._create_control(tab_advanced, "Preserve Detail", self.detail_var, None, None, 'check', "Apply sharpening before resizing to keep details.")
        self._create_control(tab_advanced, "Aspect Correction", self.aspect_var, None, None, 'check', "Correct for non-square character aspect ratio.")
        self._create_control(tab_advanced, "Smart Background", self.smart_bg_var, None, None, 'check', "Choose a contrasting background for transparent images.")

        # --- Style Tab ---
        self._create_control(tab_style, "Grayscale Mode:", self.color_mode_var, ['weighted', 'desaturate', 'channel'], None, 'combo', "Method for converting image to grayscale.")
        self._create_control(tab_style, "Color Channel:", self.color_channel_var, ['red', 'green', 'blue'], None, 'combo', "Which color channel to use in 'channel' mode.")
        self._create_control(tab_style, "Double Width", self.double_width_var, None, None, 'check', "Make each character twice as wide.")
        self._create_control(tab_style, "Add Spacing", self.spacing_var, None, None, 'check', "Add a space between each character.")
        self._create_control(tab_style, "Reverse Colors", self.reverse_var, None, None, 'check', "Invert the character brightness (light becomes dark).")
        self._create_control(tab_style, "Add Border", self.border_var, None, None, 'check', "Add a border around the ASCII art.")
        self._create_control(tab_style, "Border Char:", self.border_char_var, ['█', '▓', '▒', '░', '#', '*', '+', '-'], None, 'combo', "Character to use for the border.")
        self.html_theme_control = self._create_control(tab_style, "HTML Theme:", self.theme_var, ['matrix', 'terminal', 'retro', 'paper'], None, 'combo', "Theme for HTML export.")

        # --- Actions Tab ---
        tk.Button(tab_actions, text="🔄 Regenerate ASCII", command=self.process_with_progress, relief='flat', bg='#e74c3c', fg='white', font=('Segoe UI', 10, 'bold')).pack(pady=5, fill='x', padx=15)
        tk.Button(tab_actions, text="💾 Save to File", command=self.save_ascii, relief='flat', bg='#27ae60', fg='white', font=('Segoe UI', 10, 'bold')).pack(pady=5, fill='x', padx=15)
        self.copy_btn = tk.Button(tab_actions, text="📋 Copy to Clipboard", command=self.copy_to_clipboard, relief='flat', bg='#f39c12', fg='white', font=('Segoe UI', 10, 'bold'))
        self.copy_btn.pack(pady=5, fill='x', padx=15)
        tk.Button(tab_actions, text="🔄 Reset Settings", command=self.reset_settings, relief='flat', bg='#95a5a6', fg='white', font=('Segoe UI', 10, 'bold')).pack(pady=5, fill='x', padx=15)

    def _create_control(self, parent, label, var, val1, val2, ctype, tooltip_text):
        """Helper function to create a setting control."""
        frame = tk.Frame(parent, bg='#ecf0f1')
        frame.pack(fill='x', padx=15, pady=5)
        
        lbl = tk.Label(frame, text=label, bg='#ecf0f1', fg='#34495e')
        lbl.pack(anchor='w')
        ToolTip(lbl, tooltip_text)

        widget = None
        if ctype == 'scale':
            res = 0.1 if isinstance(var.get(), float) else 1
            widget = tk.Scale(frame, from_=val1, to=val2, resolution=res, orient='horizontal', variable=var, bg='#ecf0f1', highlightthickness=0)
        elif ctype == 'combo':
            widget = ttk.Combobox(frame, textvariable=var, values=val1, state='readonly', style='Modern.TCombobox')
        elif ctype == 'check':
            widget = tk.Checkbutton(frame, variable=var, bg='#ecf0f1', fg='#34495e', selectcolor='#3498db', activebackground='#ecf0f1')
        
        if widget:
            widget.pack(fill='x', pady=2)
            ToolTip(widget, tooltip_text)
        return widget

    def _get_current_settings(self):
        """Collect all current settings from the UI into a dictionary."""
        return {
            'width': self.width_var.get(),
            'brightness': self.brightness_var.get(),
            'contrast': self.contrast_var.get(),
            'sharpness': self.sharpness_var.get(),
            'saturation': self.saturation_var.get(),
            'remove_bg': self.remove_bg_var.get(),
            'bg_threshold': self.bg_threshold_var.get(),
            'bg_feather': self.bg_feather_var.get(),
            'effects': self.effects_var.get(),
            'char_set': self.char_set_var.get(),
            'adaptive': self.adaptive_var.get(),
            'dithering': self.dithering_var.get(),
            'preserve_detail': self.detail_var.get(),
            'aspect_correction': self.aspect_var.get(),
            'color_mode': self.color_mode_var.get(),
            'color_channel': self.color_channel_var.get(),
            'double_width': self.double_width_var.get(),
            'add_spacing': self.spacing_var.get(),
            'reverse_colors': self.reverse_var.get(),
            'smart_background': self.smart_bg_var.get(),
            'add_border': self.border_var.get(),
            'border_char': self.border_char_var.get(),
            'color_ascii': self.color_ascii_var.get(),
        }

    def open_file(self):
        """Open an image file, display a preview, and start processing."""
        file_path = filedialog.askopenfilename(
            title="Select Image for Super Realistic ASCII Conversion",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp"), ("All Files", "*.*")]
        )
        if not file_path:
            return

        self.file_path = file_path
        try:
            self.original_image = Image.open(file_path)
            filename = os.path.basename(file_path)
            self.file_label.config(text=f"{filename}")
            
            width, height = self.original_image.size
            mode = self.original_image.mode
            self.info_label.config(text=f"📐 {width}×{height} pixels, {mode} mode")
            
            self.update_preview(self.original_image)
            self.process_with_progress()
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")
            self.file_path = None

    def update_preview(self, image_to_preview):
        """Update the image preview panel."""
        if not image_to_preview:
            return
        preview_size = (340, 240)
        preview = image_to_preview.copy()
        preview.thumbnail(preview_size, Image.Resampling.LANCZOS)
        
        # Add a border for better visibility
        preview_with_border = ImageOps.expand(preview, border=2, fill='#3498db')
        
        self.processed_image_for_preview = ImageTk.PhotoImage(preview_with_border)
        self.preview_label.config(image=self.processed_image_for_preview, text="")

    def process_with_progress(self):
        """Process the image in a separate thread with a progress bar."""
        if not self.file_path:
            messagebox.showwarning("Warning", "Please select an image file first.")
            return
        if self.is_processing:
            return

        self.is_processing = True
        self.progress_bar.start(10)
        
        thread = threading.Thread(target=self._processing_thread, daemon=True)
        thread.start()

    def _processing_thread(self):
        """The actual image processing logic that runs in a background thread."""
        self.root.after(0, self.status_label.config, {'text': "🔄 Processing image..."})
        
        settings = self._get_current_settings()
        
        try:
            # --- Image Processing Pipeline ---
            image = Image.open(self.file_path)
            
            # Ensure image is in a workable mode (RGBA for transparency handling)
            if image.mode != 'RGBA':
                image = image.convert('RGBA')

            # 1. Background Removal
            if settings['remove_bg']:
                image = self._intelligent_background_removal(image, settings['bg_threshold'], settings['bg_feather'])

            # 2. Pre-processing Effects
            if settings["effects"] != "none":
                # Effects work on RGB, so convert, apply, then potentially convert back
                alpha = image.split()[-1]
                rgb_image = image.convert("RGB")
                processed_rgb = self._apply_effects(rgb_image, settings["effects"])
                processed_rgb.putalpha(alpha)
                image = processed_rgb

            # 3. Image Enhancements (Brightness, Contrast, etc.)
            rgb_image = image.convert("RGB") # Enhancements work on RGB
            enhancers = {
                'brightness': ImageEnhance.Brightness,
                'contrast': ImageEnhance.Contrast,
                'sharpness': ImageEnhance.Sharpness,
                'saturation': ImageEnhance.Color,
            }
            for key, enhancer_class in enhancers.items():
                if settings[key] != 1.0:
                    enhancer = enhancer_class(rgb_image)
                    rgb_image = enhancer.enhance(settings[key])
            
            alpha = image.split()[-1]
            rgb_image.putalpha(alpha)
            image = rgb_image

            # 4. Handle transparency
            if image.mode == 'RGBA':
                bg_color = (255, 255, 255) # Default white
                if settings['smart_background']:
                    # Simple smart bg: use inverted average color of non-transparent parts
                    non_transparent = np.array(image)[np.array(image)[:,:,3] > 128]
                    if len(non_transparent) > 0:
                        avg_color = np.mean(non_transparent[:, :3], axis=0)
                        bg_color = tuple(255 - int(c) for c in avg_color)

                background = Image.new('RGBA', image.size, bg_color + (255,))
                background.paste(image, mask=image)
                image = background.convert('RGB')
            else:
                image = image.convert('RGB')

            # 5. Resize
            resized_image = self._intelligent_resize(image, settings['width'], settings['preserve_detail'], settings['aspect_correction'])
            
            # --- ASCII Generation ---
            if settings['color_ascii']:
                self.ascii_art_data, colored_data = self._create_color_ascii(resized_image, settings)
                self.root.after(0, self._display_color_ascii, colored_data)
            else:
                # 6. Grayscale Conversion
                gray_image = self._convert_to_grayscale(resized_image, settings)
                
                # 7. ASCII Mapping
                ascii_str = self._map_pixels_to_ascii(gray_image, settings)
                
                # 8. Formatting
                self.ascii_art_data = self._format_ascii_output(ascii_str, gray_image.width, settings)
                self.root.after(0, self._display_mono_ascii, self.ascii_art_data)

            # --- Final UI Updates ---
            self.root.after(0, self.update_preview, image)
            self.root.after(0, self.status_label.config, {'text': "✅ Generation successful!"})
            lines = self.ascii_art_data.count('\n') + 1
            chars = len(self.ascii_art_data)
            self.root.after(0, self.stats_label.config, {'text': f"📊 {lines} lines, {chars} characters"})

        except Exception as e:
            self.root.after(0, messagebox.showerror, "Processing Error", f"An error occurred: {e}")
            self.root.after(0, self.status_label.config, {'text': "❌ Error during processing."})
        finally:
            self.is_processing = False
            self.root.after(0, self.progress_bar.stop)

    # --- Image Processing Sub-routines ---

    def _intelligent_background_removal(self, image, threshold, feather_radius):
        """Remove background from an RGBA image."""
        if image.mode != 'RGBA':
            return image
        
        img_array = np.array(image)
        # Use corners to guess background color
        corners = [img_array[0, 0], img_array[0, -1], img_array[-1, 0], img_array[-1, -1]]
        bg_color = np.mean([c for c in corners if c[3] > 0], axis=0)[:3] if any(c[3] > 0 for c in corners) else (255, 255, 255)
        
        distances = np.sqrt(np.sum((img_array[:, :, :3] - bg_color) ** 2, axis=2))
        alpha_mask = np.where(distances < threshold, 0, 255).astype(np.uint8)

        # Feathering using Pillow instead of Scipy
        if feather_radius > 0:
            mask_img = Image.fromarray(alpha_mask, 'L')
            feathered_mask = mask_img.filter(ImageFilter.GaussianBlur(radius=feather_radius))
            alpha_mask = np.array(feathered_mask)
            
        img_array[:, :, 3] = alpha_mask
        return Image.fromarray(img_array, 'RGBA')

    def _apply_effects(self, image, effect_type):
        """Apply pre-processing visual effects."""
        effects = {
            "enhance": lambda img: img.filter(ImageFilter.UnsharpMask(radius=1.5, percent=200, threshold=3)),
            "smooth": lambda img: img.filter(ImageFilter.GaussianBlur(radius=0.5)).filter(ImageFilter.EDGE_ENHANCE),
            "edge": lambda img: ImageOps.invert(img.filter(ImageFilter.FIND_EDGES)).filter(ImageFilter.SMOOTH),
            "artistic": lambda img: ImageOps.autocontrast(img.filter(ImageFilter.EMBOSS)),
            "dramatic": lambda img: ImageOps.autocontrast(img, cutoff=5).filter(ImageFilter.UnsharpMask(radius=2, percent=300, threshold=5))
        }
        if effect_type in effects:
            return effects[effect_type](image)
        return image

    def _intelligent_resize(self, image, target_width, preserve_detail, aspect_correction):
        """Resize image with detail preservation and aspect ratio correction."""
        width, height = image.size
        aspect_ratio = height / width
        char_aspect = 0.55 if aspect_correction else 1.0
        new_height = int(target_width * aspect_ratio * char_aspect)
        
        if preserve_detail and target_width < width:
            image = image.filter(ImageFilter.UnsharpMask(radius=0.5, percent=100, threshold=1))
            
        return image.resize((target_width, new_height), Image.Resampling.LANCZOS)

    def _convert_to_grayscale(self, image, settings):
        """Convert an RGB image to grayscale using the selected method."""
        mode = settings['color_mode']
        if mode == 'weighted':
            # This is the standard, perceptually-weighted conversion
            return image.convert('L')
        elif mode == 'desaturate':
            return ImageOps.grayscale(image)
        elif mode == 'channel':
            r, g, b = image.split()
            channel_map = {'red': r, 'green': g, 'blue': b}
            return channel_map.get(settings['color_channel'], r)
        return image.convert('L') # Default fallback

    def _map_pixels_to_ascii(self, image, settings):
        """Map grayscale pixel values to ASCII characters."""
        pixels = np.array(image.getdata())
        char_set = ASCII_SETS[settings['char_set']]
        
        if settings['adaptive']:
            # Histogram equalization for better contrast
            hist, bins = np.histogram(pixels, bins=256, range=(0, 255))
            cdf = hist.cumsum()
            cdf_normalized = cdf / cdf[-1]
            equalized_pixels = np.interp(pixels, bins[:-1], cdf_normalized * 255)
            pixels = equalized_pixels

        # Map pixels to characters
        indices = (pixels * (len(char_set) / 256)).astype(int)
        indices = np.clip(indices, 0, len(char_set) - 1)
        ascii_chars = [char_set[i] for i in indices]
        
        return "".join(ascii_chars)

    def _create_color_ascii(self, image, settings):
        """Generate ASCII art with color data."""
        pixels = np.array(image)
        gray_image = self._convert_to_grayscale(image, settings)
        ascii_str = self._map_pixels_to_ascii(gray_image, settings)
        
        img_width = image.width
        
        # Create a list of (char, color_tuple)
        colored_data = []
        for i, char in enumerate(ascii_str):
            y, x = divmod(i, img_width)
            color = tuple(pixels[y, x])
            colored_data.append((char, color))
            
        # Format for plain text copy/paste
        plain_text = self._format_ascii_output(ascii_str, img_width, settings)
        return plain_text, colored_data

    def _format_ascii_output(self, ascii_str, width, settings):
        """Apply final formatting like borders, spacing, etc."""
        lines = [ascii_str[i:i + width] for i in range(0, len(ascii_str), width)]
        
        formatted_lines = []
        for line in lines:
            if settings['double_width']:
                line = ''.join(c * 2 for c in line)
            if settings['add_spacing']:
                line = ' '.join(line)
            if settings['reverse_colors']:
                char_set = ASCII_SETS[settings['char_set']]
                reversed_set = char_set[::-1]
                line = ''.join(reversed_set[char_set.index(c)] if c in char_set else c for c in line)
            formatted_lines.append(line)
            
        if settings['add_border']:
            border_char = settings['border_char']
            max_len = max(len(line) for line in formatted_lines) if formatted_lines else 0
            border_line = border_char * (max_len + 4)
            formatted_lines = [border_line] + [f"{border_char} {line.ljust(max_len)} {border_char}" for line in formatted_lines] + [border_line]
            
        return '\n'.join(formatted_lines)

    # --- UI Display and Actions ---

    def _display_mono_ascii(self, ascii_data):
        """Display monochrome ASCII art in the text area."""
        self.text_area.config(fg='#00ff00') # Reset to default green
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, ascii_data)

    def _display_color_ascii(self, colored_data):
        """Display colored ASCII art using Tkinter tags."""
        self.text_area.delete(1.0, tk.END)
        
        # Configure a tag for each unique color
        color_tags = {}
        for char, color in colored_data:
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            if hex_color not in color_tags:
                tag_name = f"color_{hex_color.strip('#')}"
                self.text_area.tag_configure(tag_name, foreground=hex_color)
                color_tags[hex_color] = tag_name
        
        # Insert characters with their color tags
        width = self.width_var.get()
        settings = self._get_current_settings()
        
        for i, (char, color) in enumerate(colored_data):
            hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
            tag_name = color_tags[hex_color]
            
            # Handle formatting
            display_char = char
            if settings['double_width']:
                display_char *= 2
            if settings['add_spacing']:
                display_char += ' '
            
            self.text_area.insert(tk.END, display_char, (tag_name,))
            if (i + 1) % width == 0:
                self.text_area.insert(tk.END, '\n')

    def save_ascii(self):
        """Save the generated ASCII art to a file (TXT, HTML, MD)."""
        if not self.ascii_art_data:
            messagebox.showwarning("Warning", "Please generate ASCII art first.")
            return

        file_path = filedialog.asksaveasfilename(
            title="Save Super Realistic ASCII Art",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Markdown Files", "*.md")]
        )
        if not file_path:
            return

        try:
            if file_path.endswith('.html'):
                # Enhanced HTML export that supports color
                theme_name = self.theme_var.get()
                themes = {
                    'matrix': {'bg': '#000000', 'color': '#00ff00', 'font': 'Courier New'},
                    'terminal': {'bg': '#1e1e1e', 'color': '#ffffff', 'font': 'Consolas'},
                    'retro': {'bg': '#000080', 'color': '#ffff00', 'font': 'monospace'},
                    'paper': {'bg': '#f5f5f5', 'color': '#000000', 'font': 'Courier New'}
                }
                theme = themes.get(theme_name, themes['matrix'])
                
                # Build HTML content
                if self.color_ascii_var.get():
                    # Create colored spans
                    body_content = ""
                    width = self.width_var.get()
                    # Re-run a lightweight color generation for export
                    settings = self._get_current_settings()
                    resized_image = self._intelligent_resize(self.original_image.convert('RGB'), settings['width'], settings['preserve_detail'], settings['aspect_correction'])
                    _, colored_data = self._create_color_ascii(resized_image, settings)
                    
                    for i, (char, color) in enumerate(colored_data):
                        hex_color = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                        body_content += f'<span style="color:{hex_color};">{char.replace(" ", "&nbsp;")}</span>'
                        if (i + 1) % width == 0:
                            body_content += '<br>'
                else:
                    # Plain text in a <pre> tag
                    body_content = f'<pre>{self.ascii_art_data}</pre>'

                html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ASCII Art</title>
    <style>
        body {{ background: {theme['bg']}; color: {theme['color']}; font-family: '{theme['font']}', monospace; white-space: pre; line-height: 1; font-size: 10px; }}
    </style>
</head>
<body>{body_content}</body>
</html>"""
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
            else: # For TXT and MD
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.ascii_art_data)
            
            messagebox.showinfo("Success", f"ASCII art saved to {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {e}")

    def copy_to_clipboard(self):
        """Copy the ASCII art plain text to the clipboard."""
        if self.ascii_art_data:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.ascii_art_data)
            self.status_label.config(text="📋 Copied to clipboard!")
            original_bg = self.copy_btn.cget('bg')
            self.copy_btn.config(bg='#2ecc71')
            self.root.after(1000, lambda: self.copy_btn.config(bg=original_bg))
        else:
            messagebox.showwarning("Warning", "No ASCII art to copy.")

    def reset_settings(self):
        """Reset all settings to their default values."""
        self.width_var.set(120)
        self.brightness_var.set(1.0)
        self.contrast_var.set(1.0)
        self.sharpness_var.set(1.0)
        self.saturation_var.set(1.0)
        self.remove_bg_var.set(False)
        self.bg_threshold_var.set(240)
        self.bg_feather_var.set(5)
        self.effects_var.set('enhance')
        self.char_set_var.set('Detailed')
        self.adaptive_var.set(True)
        self.dithering_var.set(False)
        self.detail_var.set(True)
        self.aspect_var.set(True)
        self.color_mode_var.set('weighted')
        self.color_channel_var.set('red')
        self.double_width_var.set(False)
        self.spacing_var.set(False)
        self.reverse_var.set(False)
        self.smart_bg_var.set(True)
        self.border_var.set(False)
        self.border_char_var.set('█')
        self.theme_var.set('matrix')
        self.color_ascii_var.set(False)
        self.status_label.config(text="🔄 Settings reset to defaults.")

    def _display_welcome_message(self):
        """Show a welcome and guide message on startup."""
        welcome_message = """
🎨 WELCOME TO SUPER REALISTIC ASCII ART GENERATOR PRO 2.0! 🎨

🌟 NEW IN VERSION 2.0:
• 🌈 Full Color ASCII Art Generation!
• 🗂️ Cleaner tabbed interface for settings.
• 📦 No more external dependencies like Scipy!
• 🐛 Bug fixes for more accurate conversions.

🚀 GETTING STARTED:
1. Click "📂 Select Image" to choose your image.
2. Check "🌈 Generate Color ASCII" for a colorful result.
3. Explore the settings tabs to fine-tune the output.
4. Click "🔄 Regenerate ASCII" in the Actions tab.
5. Save or copy your masterpiece!
"""
        self.text_area.insert(tk.END, welcome_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = ASCIIArtGeneratorApp(root)
    root.mainloop()
