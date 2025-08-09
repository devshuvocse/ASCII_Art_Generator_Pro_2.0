# 🎨 Super Realistic ASCII Art Generator Pro 2.0

[![GitHub Repo](https://img.shields.io/badge/GitHub-View%20Repository-blue?logo=github)](https://github.com/devshuvocse/ASCII_Art_Generator_Pro_2.0.git)

An advanced, feature-rich desktop application for converting images into high-quality ASCII art, now with full color support. This tool provides a wide array of customization options, from intelligent background removal to multiple character sets and image enhancement filters, giving you complete control over the final output.

---

## ✨ Key Features

- **🌈 Full Color ASCII Art:** Generate ASCII art that retains the original colors of the source image.
- **🖼️ Real-time Preview:** See a live preview of your image as you adjust the settings.
- **🤖 AI-Powered Background Removal:** Intelligently detect and remove the background from your images.
- **🗂️ Tabbed & Scrollable UI:** A clean, organized, and user-friendly interface.
- **🎨 Advanced Image Processing:**
  - Adjust brightness, contrast, sharpness, and saturation.
  - Apply pre-processing effects like Enhance, Smooth, Edge Detection, and more.
  - Utilize adaptive mapping and dithering for superior gradient representation.
- **🔧 Extensive Customization:**
  - Multiple character sets: Detailed, Classic, Blocks, Lines, Dots, Braille.
  - Options for double-width characters, spacing, color reversal, and borders.
- **💾 Multiple Export Options:** Save as plain text (.txt), HTML (.html), or Markdown (.md).
- **📋 Clipboard Support:** Instantly copy your ASCII art to the clipboard.
- **📦 Zero Heavy Dependencies:** Built with standard Python libraries and Pillow.

---

## ⚙️ Requirements

- **Python 3**
- **Pillow:** The Python Imaging Library (Fork) for image manipulation.
- **NumPy:** A library for numerical operations.

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/devshuvocse/ASCII_Art_Generator_Pro_2.0.git
cd ASCII_Art_Generator_Pro_2.0
```

### Install Dependencies

If you need to add a virtual environment, you can use:
'''bash
python3 -m venv venv
source venv/bin/activate
'''
Install dependencies with:

```bash
pip install Pillow numpy
```

---

## 🚀 How to Run

1. Make sure you have Python 3 and the required libraries installed.
2. Save the code as a Python file (e.g., `ascii_art_generator.py`).
3. Run the file from your terminal:

```bash
python ascii_art_generator.py
```

---

![Screenshot of the UI](image.png)

---

## 📖 How to Use: A Detailed Guide

### 1. Loading Your Image
- Click the 📂 **Select Image** button.
- Choose any common image format (PNG, JPG, BMP, etc.).
- Preview and image info will be displayed.

### 2. Basic Settings Tab
- **Width:** Controls ASCII art width in characters.
- **Character Set:** Select from various sets for different aesthetics.
- **Effects:** Apply pre-processing filters (e.g., edge for outlines).
- **🌈 Generate Color ASCII:** Toggle color output.

### 3. Enhance Tab
- **Brightness, Contrast, Sharpness, Saturation:** Fine-tune image properties.

### 4. Advanced Tab
- **Remove Background:** Intelligent background removal.
- **BG Threshold & Feather:** Control sensitivity and smoothness.
- **Adaptive Mapping:** Histogram equalization for better contrast.
- **Dithering:** Smoother gradients.
- **Aspect Correction:** Prevents stretched output.
- **Smart Background:** Auto background for transparent images.

### 5. Style Tab
- **Grayscale Mode:** Weighted is most accurate.
- **Double Width, Add Spacing, Reverse Colors, Add Border:** Formatting options.
- **HTML Theme:** Choose background/text color for HTML export.

### 6. Actions Tab
- **🔄 Regenerate ASCII:** Update result after changing settings.
- **💾 Save to File:** Export as `.txt`, `.html`, or `.md`.
- **📋 Copy to Clipboard:** Copy plain text art.
- **🔄 Reset Settings:** Restore defaults.

---

## 📝 Character Sets

| Name     | Characters                                      |
|----------|-------------------------------------------------|
| Detailed | █▉▊▋▌▍▎▏                                      |
| Classic  | @%#*+=-:.                                      |
| Blocks   | ██▓▒░                                          |
| Lines    | ≡+=:-.                                         |
| Dots     | ●◐◑◒◓○⚬⚪                                      |
| Braille  | ⣿⣾⣽⣻⣟⣯⣷⣶⣴⣲⣱⣰⣠⣀              |

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

