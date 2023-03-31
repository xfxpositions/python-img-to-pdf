import os
from tkinter import *
from tkinter import filedialog
import locale
from main import hebele
from tkinter import messagebox
from tkinter import filedialog

root = Tk()


selected_files = []
# function to update selected file's index in the listbox
def move_up():
    global selected_files, listbox
    if not listbox.curselection():  # if no item selected, return
        return
    selected_value = listbox.get(listbox.curselection()[0])
    if selected_value in selected_files and selected_files.index(selected_value) > 0:  # if not already at top
        # move selected item up one position
        selected_index = selected_files.index(selected_value)
        selected_files[selected_index], selected_files[selected_index-1] = selected_files[selected_index-1], selected_files[selected_index]
        # update listbox
        listbox.delete(0, END)
        for file in selected_files:
            listbox.insert(END, file)
        # re-select item with same value as before
        new_selected_index = selected_files.index(selected_value)
        listbox.selection_clear(0, END)
        listbox.selection_set(new_selected_index)

def move_down():
    global selected_files, listbox
    if not listbox.curselection():  # if no item selected, return
        return
    selected_value = listbox.get(listbox.curselection()[0])
    if selected_value in selected_files and selected_files.index(selected_value) < len(selected_files)-1:  # if not already at bottom
        # move selected item down one position
        selected_index = selected_files.index(selected_value)
        selected_files[selected_index], selected_files[selected_index+1] = selected_files[selected_index+1], selected_files[selected_index]
        # update listbox
        listbox.delete(0, END)
        for file in selected_files:
            listbox.insert(END, file)
        # re-select item with same value as before
        new_selected_index = selected_files.index(selected_value)
        listbox.selection_clear(0, END)
        listbox.selection_set(new_selected_index)

def delete_files():
    global selected_files, listbox
    listbox.delete(0, END)
    selected_files.clear()

def delete_selected_element():
    selected_indices = listbox.curselection()
    if selected_indices:
        listbox.delete(selected_indices[0])

# function to open file dialog and add selected files to listbox
def open_files():
    global selected_files, listbox
    files = filedialog.askopenfilenames(initialdir="/", title="Select Files", filetypes=(("Image files", "*.jpg;*.png"), ("All files", "*.*")))
    for file in files:
        if file not in selected_files:  # avoid adding duplicates
            selected_files.append(file)
            listbox.insert(END, file)



title_label = Label(root, text="Python Image to Pdf", font=("Arial", 20))
title_label.pack(pady=20)

# create button to open file dialog
select_button = Button(root, text="Select Files", command=open_files)
select_button.pack()

# create listbox to display selected files
listbox = Listbox(root, width=50, selectmode=SINGLE)
listbox.pack()

# create buttons to update selected file's index in listbox
up_button = Button(root, text="Move Up", command=move_up)
up_button.pack()

down_button = Button(root, text="Move Down", command=move_down)
down_button.pack()

# create button to delete all selected files
delete_button = Button(root, text="Delete Files", command=delete_files)
delete_button.pack()

delete_one_button = Button(root, text="Delete File From List", command=delete_selected_element)
delete_one_button.pack()

# create the menu bar
menu_bar = Menu(root)

# create the language menu
language_menu = Menu(menu_bar, tearoff=0)
language_menu.add_command(label="Turkish", command=lambda: set_language("tr"))
language_menu.add_command(label="English", command=lambda: change_language("en"))

def set_language(lang_code):
    language = lang_code
    change_language(language)

# add the language menu to the menu bar
menu_bar.add_cascade(label="Language", menu=language_menu)
# set the menu bar as the root window's menu
root.config(menu=menu_bar)
finish_message = "DONE"
def start():
    file_path = filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF files", "*.pdf")])
    filename, ext = os.path.splitext(file_path)  # split filename and extension
    if len(filename.split(' '))>1:
        messagebox.showerror("Error", "Filename can't be words, (Dosya ismi iki kelime olamaz) use this: file-name")
    else:
        print(selected_files)
        print(file_path)
        hebele(selected_files,file_path)
        messagebox.showinfo("Message", f"{finish_message} {file_path}")
# create the button
start_button = Button(root, text="Start", width=20, height=5, command=start)

# add the button to the root window
start_button.pack()   
# function to change the app language
def change_language(lang):
    if lang == 'en':
        delete_button.config(text='Delete Files')
        down_button.config(text="Move Down")
        up_button.config(text="Move Up")
        select_button.config(text="Select Files")
        title_label.config(text="Python Image to Pdf")
        start_button.config(text="Start")
        delete_one_button.config(text="Delete Selected Element")
        finish_message = "Done"
    elif lang == 'tr':
        delete_button.config(text='Dosyaları Temizle')
        down_button.config(text="Dosyanın Sırasını Aşağı Çek")
        up_button.config(text="Dosyanın Sırasını Yukarı Çek")
        select_button.config(text="Dosyaları Seç")
        title_label.config(text="Python Resimleri Pdf'e Çevirme")
        start_button.config(text="Başlat")
        delete_one_button.config(text="Seçili elemanı sil")
        finish_message = "Bitti"

root.geometry("500x500")  # set window size
root.update_idletasks()  # update window dimensions before getting screen size
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # center window on screen

# get the user's default locale
user_locale, _ = locale.getdefaultlocale()

# extract the language code from the locale string
if user_locale:
    language = user_locale.split("_")[0]
else:
    # if the locale is not set, default to English
    language = "en"
print(language)
change_language(language)

# start the event loop
root.mainloop()
