import cv2
import tkinter as tk
from tkinter import filedialog, Label, Button, Frame
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Visioncraft")
root.geometry("950x620")
root.configure(bg="beige")

original_image = None
processed_image = None
img_frame = Frame(root, bg="beige")
img_frame.pack(pady=20)

control_frame = Frame(root, bg="beige")
control_frame.pack(pady=10)

Label(img_frame, text="Original", font=("Arial", 12, "bold"), bg="beige").grid(row=0, column=0)
Label(img_frame, text="Edited", font=("Arial", 12, "bold"), bg="beige").grid(row=0, column=1)

original_label = Label(img_frame, bg="beige")
original_label.grid(row=1, column=0, padx=20)

edited_label = Label(img_frame, bg="beige")
edited_label.grid(row=1, column=1, padx=20)

def display_images():
    if original_image is not None:
        img = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img).resize((300, 300))
        img = ImageTk.PhotoImage(img)
        original_label.config(image=img)
        original_label.image = img

    if processed_image is not None:
        img = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img).resize((300, 300))
        img = ImageTk.PhotoImage(img)
        edited_label.config(image=img)
        edited_label.image = img

def open_image():
    global original_image, processed_image
    path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png *.jpeg")])
    if path:
        original_image = cv2.imread(path)
        processed_image = original_image.copy()
        display_images()


def apply_filter():
    global processed_image

    if original_image is None:
        return

    choice = filter_var.get()

    if choice == "Cartoonify":
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 5)
        edges = cv2.adaptiveThreshold(gray, 255,
                                      cv2.ADAPTIVE_THRESH_MEAN_C,
                                      cv2.THRESH_BINARY, 9, 9)
        color = cv2.bilateralFilter(original_image, 9, 300, 300)
        processed_image = cv2.bitwise_and(color, color, mask=edges)

    elif choice == "Grayscale":
        processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)

    elif choice == "Black & White":
        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        _, processed_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)

    elif choice == "Flip":
        processed_image = cv2.flip(original_image, 1)

    elif choice == "Rotate":
        processed_image = cv2.rotate(original_image, cv2.ROTATE_90_CLOCKWISE)

    elif choice == "Blur":
        processed_image = cv2.GaussianBlur(original_image, (15, 15), 0)

    display_images()

Button(control_frame, text="Open Image", command=open_image,
       font=("Arial", 12), bg="light pink", width=18).grid(row=0, column=0, padx=10)

Label(control_frame, text="Choose Filter:", font=("Arial", 11),
      bg="beige").grid(row=0, column=1)

filter_var = tk.StringVar()
filters = [
    "Cartoonify",
    "Grayscale",
    "Black & White",
    "Flip",
    "Rotate",
    "Blur"
]

filter_menu = ttk.Combobox(control_frame, textvariable=filter_var,
                            values=filters, state="readonly", width=18)
filter_menu.grid(row=0, column=2, padx=10)
filter_menu.current(0)

Button(control_frame, text="Apply Filter", command=apply_filter,
       font=("Arial", 12), bg="light blue", width=18).grid(row=0, column=3, padx=10)

root.mainloop()
