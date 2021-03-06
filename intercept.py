import xlrd
import time
import ntpath
import pyautogui
import pyperclip
from tkinter import *
from tkinter import font
from tkinter import ttk, filedialog, messagebox


class App:

    def __init__(self, parent):
        self.parent = parent
        self.frame = Frame(parent)
        self.frame.place(relwidth=1, relheight=1)
        self.upload_label = Label(
            self.frame, text="Upload Excel file.", font=("Helvetica", 13))
        self.upload_label.place(x=10, y=10)
        self.upload_button = Button(self.frame, text="Upload", font=(
            "Helvetica", 13), command=self.destroy_widget)
        self.upload_button.place(width=180, height=50, x=10, y=60)

    def searchAll(self, position):
        # will go to find searchAll
        searchall = pyautogui.locateCenterOnScreen('images/searchall.png')
        if searchall is not None:
            pyautogui.moveTo(searchall[0], searchall[1])
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(screen_width/2, screen_height/2)  # Needs recheck
            pyautogui.click()
            pyautogui.hotkey('ctrl', 'z')
            time.sleep(1)
            bom = pyautogui.locateCenterOnScreen('images/bom.png')
            # list to store current missing bom
            current_values = []
            if bom is not None:
                pyperclip.copy('')
                pyautogui.moveTo(bom[0], bom[1])
                pyautogui.moveRel(150, 0)
                pyautogui.click()
                # check if there is any position already
                pyautogui.hotkey('ctrl', 'a')
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(.01)
                existing = str(pyperclip.paste())
                time.sleep(.01)
                # For empty field value
                if len(existing) == 0:
                    # check if incoming value has no decimal point
                    if position[0].count('.') == 0:
                        pyautogui.press('backspace')
                        pyautogui.write(position[0])
                        pyautogui.moveRel(-150, 0)
                        pyautogui.click()
                    else:
                        pyautogui.press('backspace')
                        pyautogui.write(position[0])
                        pyautogui.moveRel(-150, 0)
                        pyautogui.click()
                        # Child with no parent
                        current_values.append(position[0])
                        current_values.append(position[1])
                        manual_errors.append(
                            'Positions require manual assignment/check up')
                        manual_errors.append(current_values)

                # For fields with data
                else:
                    if existing.count('.') == 0:
                        # check if both field value and incoming value has no decimal point
                        if position[0].count('.') == 0:
                            if existing == position[0]:
                                pyautogui.press('backspace')
                                pyautogui.write(position[0])
                                pyautogui.moveRel(-150, 0)
                                pyautogui.click()
                            else:
                                pyautogui.moveRel(-150, 0)
                                pyautogui.click()
                                # Existing value is different from incoming value.
                                current_values.append(position[0])
                                current_values.append(position[1])
                                manual_errors.append(
                                    'Positions require manual assignment/check up')
                                manual_errors.append(current_values)

                        else:
                            # check if field value has no decimal point but incoming value has
                            if existing == position[0][0]:
                                pyautogui.press('backspace')
                                pyautogui.write(position[0])
                                pyautogui.moveRel(-150, 0)
                                pyautogui.click()
                            else:
                                pyautogui.moveRel(-150, 0)
                                pyautogui.click()
                                # parent not found
                                current_values.append(position[0])
                                current_values.append(position[1])
                                manual_errors.append(
                                    'Positions require manual assignment/check up')
                                manual_errors.append(current_values)

                    else:
                        # check if field value has decimal point but incoming value doesn't
                        # never overwrite any child *
                        if position[0].count('.') == 0:
                            pyautogui.moveRel(-150, 0)
                            pyautogui.click()
                            # Could not overwrite child by parent.
                            current_values.append(position[0])
                            current_values.append(position[1])
                            manual_errors.append(
                                'Positions require manual assignment/check up')
                            manual_errors.append(current_values)

                        else:
                            # check if both field value and incoming value has decimal point
                            if existing == position[0]:
                                pyautogui.press('backspace')
                                pyautogui.write(position[0])
                                pyautogui.moveRel(-150, 0)
                                pyautogui.click()
                            else:
                                pyautogui.moveRel(-150, 0)
                                pyautogui.click()
                                # Could not overwrite child by a different child.
                                current_values.append(position[0])
                                current_values.append(position[1])
                                manual_errors.append(
                                    'Positions require manual assignment/check up')
                                manual_errors.append(current_values)

            else:
                current_values.append(position[0])
                current_values.append(position[1])
                manual_errors.append(
                    'Positions require manual assignment/check up')
                manual_errors.append(current_values)

        else:
            if messagebox.askretrycancel('Error', "Can't see 'search all'."):
                time.sleep(1)
                self.searchAll(position)
            else:
                app.destroy()

    def errors(self):
        new_notice_label.destroy()
        new_notice_message.destroy()
        new_notice_progressBar.destroy()
        new_notice_progressPercent.destroy()
        new_notice_progressText.destroy()
        # put all errors together
        total_errors = [empty_values, beyond_scope, manual_errors]
        # list for displayed errors
        displayed_errors = []
        for error in total_errors:
            if len(error) != 0:
                displayed_errors.append(error)

        # expand window depending on the number of error types
        if len(displayed_errors) <= 2:
            self.parent.geometry("650x500")
            new_error_button.place(relx=0.1, rely=0.88)
            new_notice_button.place(relx=0.8, rely=0.88)
        elif len(displayed_errors) == 3:
            self.parent.geometry("650x700")
            new_error_button.place(relx=0.1, rely=0.88)
            new_notice_button.place(relx=0.8, rely=0.88)
        else:
            self.parent.geometry('650x900')
            new_error_button.place(relx=0.1, rely=0.88)
            new_notice_button.place(relx=0.8, rely=0.88)

        # display the errors
        y_heading = 0
        y_tree = 50
        third_tree = 0
        for error in displayed_errors:
            # Create scrollbar in case there are many errors
            error_frame = Frame(self.frame)
            scrollbar = Scrollbar(error_frame)
            scrollbar.pack(side=RIGHT, fill=Y)
            # Create tree to display the errors
            error_view = ttk.Treeview(self.frame)
            error_view.configure(yscrollcommand=scrollbar.set)
            # configure scrollbar
            scrollbar.configure(command=error_view.yview)
            error_view['columns'] = ('Position', 'PartCode')  # define columns
            # 0 column is created by default
            error_view.column('#0', width=0, stretch=NO)
            error_view.column("Position", width=120)  # properties of columns
            error_view.column("PartCode", width=120)  # properties of columns
            error_view.heading('#0', text='')
            error_view.heading('Position', text='Position',
                               anchor=CENTER)  # heading names
            error_view.heading('PartCode', text='PartCode',
                               anchor=CENTER)  # heading names
            # How many errors of the current type
            number = error.count(error[0])
            displayed_error_label = Label(
                self.frame, text=f'{error[0]} ({number})', font=("Helvetica", 13))
            displayed_error_label.place(x=10, y=y_heading + 10)
            f = font.Font(displayed_error_label, displayed_error_label.cget(
                "font"))  # get underline functionality
            f.configure(underline=True)
            displayed_error_label.configure(font=f)
            # modify styles of treeview
            style = ttk.Style()
            style.configure("Treeview.Heading", font=("Helvetica", 13))
            style.theme_use('default')  # useful to display the styles below
            style.configure("Treeview", background='white',
                            fieldbackground='white', rowheight=30)
            style.map('Treeview', background=[('selected', "#557A95")])
            error_view.tag_configure('evenrow', font=(
                "Helvetica", 12), background='light blue')  # change styles of data
            error_view.tag_configure('oddrow', font=(
                "Helvetica", 12), background="white")  # change styles of data
            count = 0
            for error_item in error:
                if type(error_item) == list:  # Remove the titles eg empty value found
                    if count % 2 == 0:
                        error_view.insert(parent='', index='end', iid=count, text='', tags=("evenrow",), values=(
                            error_item[0] if len(error_item[0]) != 0 else 'Empty', error_item[1] if len(error_item[1]) != 0 else 'Empty'))
                    else:
                        error_view.insert(parent='', index='end', iid=count, text='', tags=("oddrow",), values=(
                            error_item[0] if len(error_item[0]) != 0 else 'Empty', error_item[1] if len(error_item[1]) != 0 else 'Empty'))
                    count += 1
            # vary the height of tree based on available errors
            if len(displayed_errors) <= 2:
                variable_height = (count + 1) * \
                    30 if (count + 1) * 30 < 150 else 150
                if len(displayed_errors) == 1:
                    variable_height = (count + 1) * \
                        30 if (count + 1) * 30 < 330 else 330
                error_frame.place(x=20, y=y_tree, relwidth=0.83,
                                  height=variable_height)
                error_view.place(x=20, y=y_tree, relwidth=0.8,
                                 height=variable_height)
                y_heading += (variable_height + 50)
                y_tree = y_heading + 50 if y_heading + 50 < 280 else 280
            elif len(displayed_errors) == 3:
                variable_height = (count + 1) * \
                    30 if (count + 1) * 30 < 150 else 150
                error_frame.place(x=20, y=y_tree if third_tree == 0 else third_tree, relwidth=0.83,
                                  height=variable_height)
                error_view.place(x=20, y=y_tree if third_tree == 0 else third_tree, relwidth=0.8,
                                 height=variable_height)
                y_heading += (variable_height + 50)
                y_tree = y_heading + 50 if y_heading + 50 < 280 else 280
                if y_tree == 280:
                    third_tree = y_heading + 50 if y_heading + 50 < 490 else 490
                else:
                    third_tree = y_heading + 50 if y_heading + \
                        50 < 490 else 490  # in case second tree doesnt reach 280

    def completed(self):
        message = "Process completed.\n- Found Errors." if error_number != 0 else 'Completed successfully.\n- No errors found'
        messagebox.showinfo(
            'Message', message)

    def searchPartcode(self):
        global error_number
        global empty_values
        global beyond_scope
        global manual_errors
        data = all_data
        # remove partcode and pos text in first list
        data.pop(0)
        new_percent = 100/len(data)
        # will store empty positions and partcode pairs
        empty_values = []
        # will store positions beyond scope
        beyond_scope = []
        # list to store all manual errors from searchall function
        manual_errors = []
        # keep track of number of errors
        error_number = 0
        # set initial value of progress bar
        new_notice_progressBar['value'] = 0
        # search for partcodes
        for item in data:
            # will store current empty position or partcodes
            current_values = []
            # update progress bar & percent
            new_notice_progressBar['value'] += 100 / len(data)
            new_notice_progressPercent.config(text=str(round(new_percent))+'%')
            # change state of error button depending on number of errors
            if round(new_percent) == 100:
                new_notice_progressText.config(text='Completed', fg="green")
                new_notice_label.config(text='Process Completed', fg="green")
                new_notice_button.config(
                    text='Exit', command=lambda: self.onClosing())
                new_notice_message.config(
                    text="- Check if there are any Errors listed below.\n- Remember to save the file before continuing any further.")

            self.parent.update_idletasks()
            new_percent += 100/len(data)
            time.sleep(0.01)
            # Check if values are not empty
            if item[0] != '' and item[1] != '':
                # will store curent position beyond scope
                failed_position = []
                # Check if given position 1st or 2nd generation only
                if item[0].count('.') <= 1:
                    # will go to find search
                    searchy = pyautogui.locateCenterOnScreen(
                        'images/searchy.png')
                    if searchy is not None:
                        pyautogui.moveTo(searchy[0], searchy[1])
                        pyautogui.click()
                        pyautogui.moveRel(100, 0)
                        pyautogui.click()
                        pyautogui.hotkey('ctrl', 'a')
                        time.sleep(0.01)
                        pyautogui.press('backspace')
                        pyautogui.write(item[1])
                        self.searchAll(item)
                    else:
                        pyautogui.moveTo(screen_width/2, screen_height/2)
                        pyautogui.click()
                        pyautogui.hotkey('ctrl', 'f')
                        pyautogui.hotkey('ctrl', 'a')
                        time.sleep(0.01)
                        pyautogui.press('backspace')
                        pyautogui.write(item[1])
                        self.searchAll(item)

                else:
                    failed_position.append(item[0])
                    failed_position.append(item[1])
                    beyond_scope.append('Positions beyond scope found')
                    beyond_scope.append(failed_position)

            else:
                current_values.append(item[0])
                current_values.append(item[1])
                empty_values.append('Empty values found')
                empty_values.append(current_values)

        # put all errors together
        total_errors = [empty_values, beyond_scope, manual_errors]
        # list for displayed errors
        displayed_errors = []
        for error in total_errors:
            if len(error) != 0:
                displayed_errors.append(error)
        # keep track of number of errors
        for error in displayed_errors:
            for error_item in error:
                if type(error_item) == list:
                    error_number += 1
        new_error_button.config(
            state=NORMAL if error_number != 0 else DISABLED, text=f'Errors ({error_number})')
        self.parent.after(500, lambda: self.completed())

    def retryCatia(self):
        thumb = pyautogui.locateCenterOnScreen('images/thumb.png')
        thumbnail = pyautogui.locateCenterOnScreen('images/thumbnail.png')
        if thumb or thumbnail is not None:
            pyautogui.moveTo(thumb[0], thumb[1])
            pyautogui.moveTo(thumbnail[0], thumbnail[1])
            pyautogui.moveRel(0, 100)
            pyautogui.click()
            self.catiaOpen()
        else:
            if messagebox.askretrycancel("Failed", 'Catia/3D is either blocked or not opened.\n Place this program\'s window near top center.'):
                # will go to find search
                searchy = pyautogui.locateCenterOnScreen('images/searchy.png')
                if searchy is not None:
                    pyautogui.moveTo(searchy[0], searchy[1])
                    pyautogui.click()
                    self.catiaOpen()
                else:
                    # Needs recheck
                    pyautogui.moveTo(screen_width/2, screen_height/2)
                    pyautogui.click()
                    self.catiaOpen()
            else:
                self.interfere()

    def catiaOpen(self):
        catia = pyautogui.locateCenterOnScreen('images/catia.png')
        if catia is not None:
            # check if catia document is opened.
            thumb = pyautogui.locateCenterOnScreen('images/thumb.png')
            thumbnail = pyautogui.locateCenterOnScreen('images/thumbnail.png')
            if thumb or thumbnail is not None:
                self.searchPartcode()
            else:
                if messagebox.askretrycancel("Failed!", '3D is either blocked or not opened.\n Check it before retrying.'):
                    # will go to find search
                    searchy = pyautogui.locateCenterOnScreen(
                        'images/searchy.png')
                    if searchy is not None:
                        pyautogui.moveTo(searchy[0], searchy[1])
                        pyautogui.click()
                        self.catiaOpen()
                    else:
                        pyautogui.moveTo(catia[0], catia[1])
                        pyautogui.click()
                        pyautogui.moveRel(200, 0)
                        pyautogui.click()
                        self.catiaOpen()
                else:
                    new_notice_button.destroy()
                    new_notice_label.destroy()
                    new_notice_message.destroy()
                    new_error_button.destroy()
                    new_notice_progressPercent.destroy()
                    self.notice()
        else:
            self.retryCatia()

    def toCatia(self):
        global cancel_id
        global new_notice_button
        global new_notice_label
        global new_notice_message
        global new_error_button
        global new_notice_progressBar
        global new_notice_progressPercent
        global new_notice_progressText
        notice.destroy()
        notice_button.destroy()
        self.parent.geometry("650x250")
        new_notice_label = Label(
            self.frame, text="Program running...", fg="red", font=("Helvetica", 13))
        new_notice_label.place(x=10, y=10)
        new_notice_message = Message(
            self.frame, width=650, font=("Helvetica", 13), text="- Don't use the mouse/keyboard during this operation.\n- Make sure Catia is opened in full screen.\n")
        new_notice_message.place(x=10, y=50)
        new_error_button = Button(
            self.frame, text='Errors', state=DISABLED, font=("Helvetica", 13), command=self.errors)
        new_error_button.place(relx=0.1, rely=0.81)
        new_notice_button = Button(
            self.frame, text='Cancel', font=("Helvetica", 13), command=self.haltProgram)
        new_notice_button.place(relx=0.8, rely=0.81)
        new_notice_progressText = Label(
            self.frame, text="Status", font=("Helvetica", 13))
        new_notice_progressText.place(x=10, y=125)
        new_notice_progressBar = ttk.Progressbar(
            self.frame, orient=HORIZONTAL, length=300, mode="determinate")
        new_notice_progressBar.place(x=130, y=130)
        new_notice_progressPercent = Label(
            self.frame, text="", font=("Helvetica", 13))
        new_notice_progressPercent.place(x=450, y=125)
        cancel_id = self.parent.after(2000, lambda: self.catiaOpen())

    def notice(self):
        global notice
        global notice_button
        upload_progress.destroy()
        self.parent.geometry("650x250")
        notice = Message(
            self.frame, width=600, font=("Helvetica", 13), text="IMPORTANT NOTICE.\n\n- Make sure the required 3D is open in Catia Composer.\n- Make sure no other apps block Catia Composer's screen.\n- Make sure Catia is opened in full screen.\n- Click 'OK' to continue.")
        notice.place(x=10, y=10)
        notice_button = Button(self.frame, text='Ok', font=(
            "Helvetica", 13), command=self.toCatia)
        notice_button.place(x=450, y=200)

    def destroy_widget(self):
        global file_label
        self.upload_label.destroy()
        self.upload_button.destroy()
        file_label = Label(self.frame, anchor='w', width=600, height=120,
                           text="Select an excel file from your computer.", font=("Helvetica", 13))
        file_label.pack(side='left', padx=10)
        self.excel_file(file_label)

    def excel_file(self, label):
        filepath = filedialog.askopenfilename(
            initialdir="/Desktop", title='Select File', filetypes=[("Excel files", ".xlsx .xls .csv")])
        if not filepath:
            label.destroy()
            App(app)
        else:
            label.destroy()
            filename = ntpath.basename(filepath)
            if filename.lower().endswith(('.xlsx', '.xls', '.csv')):
                global upload_progress
                upload_progress = Label(
                    self.frame, text="File uploading", font=("Helvetica", 13))
                row_progress = ttk.Progressbar(
                    self.frame, orient=HORIZONTAL, length=300, mode="determinate")
                # open excel and sheet
                workbook = xlrd.open_workbook(filepath)
                sheet = workbook.sheet_by_index(0)

                # Stores Position and Partcode value pairs from all rows.
                global all_data
                all_data = []

                # loop over rows and columns to extract Position and Partcode pairs
                for row in range(sheet.nrows):
                    current_row = []
                    upload_progress.pack(side='left')
                    row_progress.pack(side='left')
                    row_progress['value'] += 100 / sheet.nrows
                    self.parent.update_idletasks()
                    time.sleep(0.01)
                    for col in range(sheet.ncols):
                        if col == 1 or col == 3:
                            data = sheet.cell_value(row, col)
                            # useful when searching in Catia Composer
                            try:
                                new_data = data.replace('/', "_")
                                current_row.append(new_data)
                            except AttributeError:
                                pass
                    all_data.append(current_row)
                if not len(all_data):
                    empty_label = Label(
                        self.frame, text="This file is empty.", fg='red', font=("Helvetica", 13))
                    empty_label.pack(side='left', padx=10)
                    response = messagebox.showerror(
                        'Error!', f"{filename} is empty.")
                    if response == 'ok':
                        empty_label.destroy()
                        different_file_label = Label(
                            self.frame, text="Try a different excel file.", font=("Helvetica", 13))
                        different_file_label.pack(side='left', padx=10)
                        self.excel_file(different_file_label)
                else:
                    row_progress.destroy()
                    upload_progress.config(
                        text="File uploaded successfully.", fg='green')
                    messagebox.showinfo(
                        'Success', 'FILE UPLOADED\n\nClick "OK" to continue.')
                    self.notice()

            else:
                not_excel_label = Label(
                    self.frame, text="Upload Excel files only.", fg='red', font=("Helvetica", 13))
                not_excel_label.pack(side='left', padx=10)
                not_excel = messagebox.showerror(
                    'Error!', f"{filename} is not an Excel file.")
                if not_excel == 'ok':
                    not_excel_label.destroy()
                    different_file_label = Label(
                        self.frame, text="Try a different excel file.", font=("Helvetica", 13))
                    different_file_label.pack(side='left', padx=10)
                    self.excel_file(different_file_label)
    # from Cancel Button when app is running

    def haltProgram(self):
        global cancel_id
        self.parent.after_cancel(cancel_id)
        self.onClosing()
        cancel_id = self.parent.after(1000, lambda: self.catiaOpen())
    # to interfere when 3d is not open

    def interfere(self):
        global cancel_id
        self.onClosing()
        cancel_id = self.parent.after(1000, lambda: self.catiaOpen())
    # close the window prompt

    def onClosing(self):
        if messagebox.askokcancel("Exit", "Do you really wish to Exit?"):
            app.destroy()


def main():
    global app
    global x
    global y
    global screen_height
    global screen_width
    app = Tk()
    # Place window slightly above the center of screen on start up
    width_window = 600
    height_window = 120
    screen_width = app.winfo_screenwidth()  # width of the screen
    screen_height = app.winfo_screenheight()  # height of the screen
    x_center = (screen_width/2)-(width_window/2)
    y_center = (screen_height/2)-(height_window/2)
    x = x_center
    y = (y_center/8)
    app.resizable(False, False)
    app.wm_iconbitmap('images/intercept.ico')
    app.wm_title('INTERCEPT')
    app.geometry('%dx%d+%d+%d' % (width_window, height_window, x, y))
    application = App(app)
    app.wm_protocol("WM_DELETE_WINDOW", lambda: application.onClosing())
    app.mainloop()


if __name__ == "__main__":
    main()
