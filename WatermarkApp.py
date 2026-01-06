from tkinter import *
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watermarking App")
        self.root.config(padx=20, pady=20)
        self.root.resizable(False, False)

        # -------------------- Estado --------------------
        self.original_image = None
        self.watermarked_image = None
        self.tk_image = None

        # -------------------- GUI --------------------
        self.create_widgets()

    # -------------------- Funções da GUI --------------------
    def create_widgets(self):
        # Top frame
        top_frame = Frame(self.root)
        top_frame.pack(pady=10)

        self.upload_btn = Button(
            top_frame, text="Upload Image", width=20, command=self.upload_image
        )
        self.upload_btn.pack()

        # Middle frame (canvas)
        middle_frame = Frame(self.root)
        middle_frame.pack(pady=10)

        self.canvas = Canvas(
            middle_frame, width=500, height=400, bg="lightgray",
            highlightthickness=1, highlightbackground="black"
        )
        self.canvas.pack()

        # Bottom frame (inputs e botões)
        bottom_frame = Frame(self.root)
        bottom_frame.pack(pady=10)

        Label(bottom_frame, text="Watermark Text:").grid(row=0, column=0, padx=5, pady=5)
        self.watermark_entry = Entry(bottom_frame, width=30)
        self.watermark_entry.grid(row=0, column=1, padx=5, pady=5)

        self.apply_btn = Button(
            bottom_frame, text="Apply Watermark", width=18, command=self.apply_watermark
        )
        self.apply_btn.grid(row=2, column=0, padx=5, pady=10)

        self.save_btn = Button(
            bottom_frame, text="Save Image", width=18, command=self.save_image
        )
        self.save_btn.grid(row=2, column=1, padx=5, pady=10)

        Label(bottom_frame, text="Opacity:").grid(row=1, column=0, padx=5, pady=5)

        # Slider de opacidade de 0 a 255
        self.opacity_slider = Scale(bottom_frame, from_=0, to=255, orient=HORIZONTAL)
        self.opacity_slider.set(120)  # valor inicial
        self.opacity_slider.grid(row=1, column=1, padx=5, pady=5)

    # -------------------- Funções de ação --------------------
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )

        if not file_path:
            return

        self.original_image = Image.open(file_path)
        display_image = self.original_image.copy()
        display_image.thumbnail((500, 400))
        self.tk_image = ImageTk.PhotoImage(display_image)
        self.canvas.delete("all")
        self.canvas.create_image(250, 200, image=self.tk_image)

    def apply_watermark(self):
        if self.original_image is None:
            messagebox.showwarning("Warning", "Upload an image first.")
            return

        text = self.watermark_entry.get()
        if not text:
            messagebox.showwarning("Warning", "Enter watermark text.")
            return

        # Convert image to RGBA
        base = self.original_image.convert("RGBA")

        # Transparent overlay
        txt_layer = Image.new("RGBA", base.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_layer)

        # Font
        try:
            font = ImageFont.truetype("arial.ttf", 36)
        except:
            font = ImageFont.load_default()

        # Correct Pillow >=10 way to get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        # Position (bottom-right)
        x = base.width - text_width - 20
        y = base.height - text_height - 20

        # Draw text with opacity
        opacity = self.opacity_slider.get()  # pega valor do slider
        draw.text((x, y), text, fill=(255, 255, 255, opacity), font=font)

        # Merge layers
        self.watermarked_image = Image.alpha_composite(base, txt_layer)

        # Resize for preview
        display_img = self.watermarked_image.copy()
        display_img.thumbnail((500, 400))
        self.tk_image = ImageTk.PhotoImage(display_img)
        self.canvas.delete("all")
        self.canvas.create_image(250, 200, image=self.tk_image)

    def save_image(self):
        if self.watermarked_image is None:
            messagebox.showwarning("Warning", "Apply watermark first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")]
        )

        if not file_path:
            return

        # Convert back if saving JPG
        img_to_save = self.watermarked_image
        if file_path.lower().endswith(".jpg"):
            img_to_save = self.watermarked_image.convert("RGB")

        img_to_save.save(file_path)
        messagebox.showinfo("Success", "Image saved successfully.")

# -------------------- MAIN --------------------
if __name__ == "__main__":
    root = Tk()
    app = WatermarkApp(root)
    root.mainloop()