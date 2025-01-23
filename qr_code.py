from tkinter import *
from tkinter import ttk, Toplevel
from tkinter.messagebox import showerror, askyesno
from tkinter import filedialog as fd
import qrcode
import cv2

def open_qr_code_menu():
    window = Toplevel()
    window.title('QR Code Generator and Scanner')
    window.geometry('500x480+440+180')
    window.resizable(height=FALSE, width=FALSE) # Creates the window for the QR code menu

    tab_control = ttk.Notebook(window) # Notebook allows the menu to be displayed in two separate tabs

    # Assigns two tabs to the frame and then names them
    first_tab = ttk.Frame(tab_control)
    second_tab = ttk.Frame(tab_control)

    tab_control.add(first_tab, text='QR Code Generator')
    tab_control.add(second_tab, text='QR Code Scanner')
    tab_control.pack(expand=1, fill="both")

    first_canvas = Canvas(first_tab, width=500, height=480)
    first_canvas.pack()

    second_canvas = Canvas(second_tab, width=500, height=480)
    second_canvas.pack()

    # Creates an image label for the QR code
    image_label1 = Label(window)
    first_canvas.create_window(250, 150, window=image_label1)

    # Creates a label and an entry for QR code data
    qrdata_label = ttk.Label(window, text='QRcode Data', style='TLabel')
    data_entry = ttk.Entry(window, width=40, style='TEntry')
    first_canvas.create_window(70, 330, window=qrdata_label)
    first_canvas.create_window(300, 330, window=data_entry)

    # Creates a label and an entry filename data
    filename_label = ttk.Label(window, text='Filename', style='TLabel')
    filename_entry = ttk.Entry(window, width=40, style='TEntry')
    first_canvas.create_window(84, 360, window=filename_label)
    first_canvas.create_window(300, 360, window=filename_entry)

    def generate_qrcode():
        qrcode_data = str(data_entry.get())
        qrcode_name = str(filename_entry.get())
        print(qrcode_name)
        if qrcode_name == '':
            showerror(title='Error', message='An error occurred' \
                                             '\nThe following is ' \
                                             'the cause:\n->Empty filename entry field\n' \
                                             'Make sure the filename entry field is filled when generating the QRCode') # Displays an error message when filename is invalid
        else:
            if askyesno(title='Confirmation', message=f'Do you want to create a QRCode with the provided information?'):
                try:
                    qr = qrcode.QRCode(version=1, box_size=6, border=4)
                    qr.add_data(qrcode_data)
                    qr.make(fit=True)
                    name = qrcode_name + '.png'
                    qrcode_image = qr.make_image(fill_colour='black', back_colour='white')
                    qrcode_image.save(f"{name}")
                    global Image
                    Image = PhotoImage(file=f'{name}')
                    image_label1.config(image=Image)
                    reset_button.config(state=NORMAL, command=reset) # Creates QR code, saves it as a png and displays the image inside the image label
                except:
                    showerror(title='Error', message='Please provide a valid filename')

    # Function which resets the image label
    def reset():
        if askyesno(title='Reset', message='Are you sure you want to reset?'):
            image_label1.config(image='')
            reset_button.config(state=DISABLED)

    # Creates reset and generate buttons
    reset_button = ttk.Button(window, text='Reset', style='TButton', state=DISABLED)
    generate_button = ttk.Button(window, text='Generate QRCode', style='TButton', command=generate_qrcode)
    first_canvas.create_window(390, 410, window=generate_button)
    first_canvas.create_window(260, 410, window=reset_button)

    # Creates image and data labels for QR code and its data
    image_label2 = Label(window)
    data_label = ttk.Label(window)
    second_canvas.create_window(250, 150, window=image_label2)
    second_canvas.create_window(250, 300, window=data_label)

    # Creates a function for opening a file from file explorer
    def open_dialog():
        name = fd.askopenfilename()
        file_entry.delete(0, END)
        file_entry.insert(0, name)

    # Creates a file entry and browse button which opens a file from file explorer
    file_entry = ttk.Entry(window, width=40, style='TEntry')
    browse_button = ttk.Button(window, text='Browse', style='TButton', command=open_dialog)
    second_canvas.create_window(200, 350, window=file_entry)
    second_canvas.create_window(400, 350, window=browse_button)

    def scan_qrcode():
        image_file = file_entry.get()
        print(f"image_file: {image_file}")
        if image_file == '':
            showerror(title='Error', message='Please provide a QR Code image file to detect')
        else:
            try:
                qr_img = cv2.imread(f'{image_file}')
                qr_detector = cv2.QRCodeDetector()
                global qrcode_image
                qrcode_image = PhotoImage(file=f'{image_file}')
                image_label2.config(image=qrcode_image)
                data, pts, st_code = qr_detector.detectAndDecode(qr_img)
                data_label.config(text=data) # Detects QR code and decodes it
            except:
                showerror(title='Error', message='An error occurred while detecting data from the provided file' \
                   '\nThe following could be ' \
                    'the cause:\n->Wrong image file\n' \
                    'Make sure the image file is a valid QRCode') # Error message for if the image is not a valid QR code

    # Creates a button for scanning a QR code
    scan_button = ttk.Button(window, text='Scan QRCode', style='TButton', command=scan_qrcode)
    second_canvas.create_window(95, 385, window=scan_button)


    window.mainloop()