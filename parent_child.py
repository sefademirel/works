import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk

class FileBrowserApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("File and Folder Browser")
        self.geometry("800x600")

        # Create folder and file icons
        self.folder_image = self.create_folder_icon()
        self.file_image = self.create_file_icon()

        # Create a frame for the TreeView and controls
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a Treeview widget
        self.tree = ttk.Treeview(frame, columns=("Type", "Path"), show="tree")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a vertical scrollbar
        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Bind the tree to handle the open event
        self.tree.bind("<ButtonRelease-1>", self.on_click)

        # Create a frame for controls
        control_frame = tk.Frame(self)
        control_frame.pack(pady=10, fill=tk.X)

        # Create a button to open a directory
        button = tk.Button(control_frame, text="Open Directory", command=self.open_directory)
        button.pack(side=tk.LEFT, padx=5)

        # Create a button to open the selected file
        self.open_file_button = tk.Button(control_frame, text="Open Selected File", command=self.open_selected_file, state=tk.DISABLED)
        self.open_file_button.pack(side=tk.LEFT, padx=5)

        self.selected_file = None  # Variable to keep track of the selected file

    def create_folder_icon(self):
        """Create a simple folder icon using Pillow."""
        width, height = 24, 24
        image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Draw folder shape
        draw.rectangle([4, 8, 20, 18], fill=(255, 215, 0), outline=(0, 0, 0))
        draw.polygon([4, 8, 10, 4, 20, 8], fill=(255, 215, 0), outline=(0, 0, 0))

        return ImageTk.PhotoImage(image)

    def create_file_icon(self):
        """Create a simple file icon using Pillow."""
        width, height = 24, 24
        image = Image.new("RGBA", (width, height), (255, 255, 255, 0))
        draw = ImageDraw.Draw(image)

        # Draw file shape
        draw.rectangle([4, 4, 20, 20], fill=(173, 216, 230), outline=(0, 0, 0))
        draw.line([4, 4, 20, 4], fill=(0, 0, 0), width=2)  # Top line
        draw.line([20, 4, 20, 20], fill=(0, 0, 0), width=2)  # Right line

        return ImageTk.PhotoImage(image)

    def open_directory(self):
        # Ask the user for a directory
        directory = filedialog.askdirectory()
        if directory:
            self.populate_tree(directory)

    def populate_tree(self, base_dir):
        # Clear the current tree
        self.tree.delete(*self.tree.get_children())

        # Insert the base directory
        base_node = self.tree.insert("", "end", text=os.path.basename(base_dir), values=("Folder", base_dir), open=True, image=self.folder_image)
        # Add folders and files for demonstration
        self._add_items(base_dir, base_node)

    def _add_items(self, base_dir, parent):
        # Add directories and files for a given base directory
        try:
            for root, dirs, files in os.walk(base_dir):
                for dir_name in sorted(dirs):  # Sort directories alphabetically
                    full_path = os.path.join(root, dir_name)
                    dir_node = self.tree.insert(parent, "end", text=dir_name, values=("Folder", full_path), image=self.folder_image)
                    # Add a placeholder item to allow expanding
                    self.tree.insert(dir_node, "end", text="...", values=("Placeholder", ""), image=self.folder_image)
                
                for file_name in sorted(files):  # Sort files alphabetically
                    full_path = os.path.join(root, file_name)
                    self.tree.insert(parent, "end", text=file_name, values=("File", full_path), image=self.file_image)

                # Stop recursion after adding the immediate children
                break  # Remove this break if you want to include all subdirectories at once
        except PermissionError:
            pass  # Handle permission errors, if any

    def on_click(self, event):
        # Get the clicked item
        item = self.tree.identify_row(event.y)
        if not item:
            return
        
        item_type = self.tree.item(item, "values")[0]
        item_path = self.tree.item(item, "values")[1]
        
        if item_type == "File":
            # Set the selected file
            self.selected_file = item_path
            self.open_file_button.config(state=tk.NORMAL)
        elif item_type == "Folder":
            # Expand or collapse the folder
            if not self.tree.item(item, "open"):
                self.tree.item(item, open=True)
                self._load_children(item)
            else:
                self.tree.item(item, open=False)

    def _load_children(self, parent):
        # Load children if they are placeholders
        if self.tree.get_children(parent):
            first_child = self.tree.get_children(parent)[0]
            if self.tree.item(first_child, "values")[0] == "Placeholder":
                # Remove placeholder
                self.tree.delete(first_child)
                # Populate the folder
                dir_path = self.tree.item(parent, "values")[1]
                self._add_items(dir_path, parent)

    def open_selected_file(self):
        if not self.selected_file:
            messagebox.showwarning("No File Selected", "Please select a file to open.")
            return
        
        # Open the file with the default application
        try:
            os.startfile(self.selected_file)
        except Exception as e:
            print(f"Error opening file: {e}")

        # Disable the button after opening the file
        self.open_file_button.config(state=tk.DISABLED)
        self.selected_file = None

if __name__ == "__main__":
    app = FileBrowserApp()
    app.mainloop()
