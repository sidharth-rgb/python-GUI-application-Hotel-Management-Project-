from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from datetime import datetime

class RoomBooking:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Booking")
        # self.root.geometry("1550x800+0+0")
        self.root.geometry("1300x550+226+220")

        # ===== Variables =====
        self.var_contact = StringVar()
        self.var_checkin = StringVar()
        self.var_checkout = StringVar()
        self.var_roomtype = StringVar()
        self.var_roomavailable = StringVar()
        self.var_meal = StringVar()
        self.var_noofdays = StringVar()
        self.var_paidtax = StringVar()
        self.var_subtotal = StringVar()
        self.var_totalcost = StringVar()
        self.search_var = StringVar()
        self.txt_search = StringVar()

        # ===== Title =====
        title = Label(self.root, text="ROOM BOOKING", font=("times new roman", 20, "bold"), bg="black", fg="yellow")
        title.place(x=0, y=0, width=1550, height=40)

        # ===== Contact Frame =====
        Label(self.root, text="Customer Phone No", font=("arial", 12, "bold")).place(x=10, y=50)
        Entry(self.root, textvariable=self.var_contact, width=20, font=("arial", 12, "bold")).place(x=180, y=50)
        Button(self.root, text="Fetch Data", command=self.fetch_contact_data, font=("arial", 10, "bold"), bg="black", fg="yellow").place(x=370, y=50)

        # ===== Left Frame =====
        room_frame = LabelFrame(self.root, text="Room Booking Details", font=("times new roman", 14, "bold"), padx=2, relief=RIDGE)
        room_frame.place(x=10, y=90, width=500, height=400)

        labels = ["Check-in Date", "Check-out Date", "Room Type", "Available Room", "Meal", "No Of Days", "Paid Tax", "Sub Total", "Total Cost"]
        for idx, text in enumerate(labels):
            Label(room_frame, text=text, font=("arial", 12, "bold")).grid(row=idx, column=0, sticky=W, padx=10, pady=5)

        Entry(room_frame, textvariable=self.var_checkin, font=("arial", 12)).grid(row=0, column=1)
        Entry(room_frame, textvariable=self.var_checkout, font=("arial", 12)).grid(row=1, column=1)

        combo_room = ttk.Combobox(room_frame, textvariable=self.var_roomtype, state="readonly", font=("arial", 12), width=18)
        combo_room['value'] = ("Single", "Double", "Luxury")
        combo_room.grid(row=2, column=1)
        combo_room.current(0)

        Entry(room_frame, textvariable=self.var_roomavailable, font=("arial", 12)).grid(row=3, column=1)
        Entry(room_frame, textvariable=self.var_meal, font=("arial", 12)).grid(row=4, column=1)
        Entry(room_frame, textvariable=self.var_noofdays, font=("arial", 12)).grid(row=5, column=1)
        Entry(room_frame, textvariable=self.var_paidtax, font=("arial", 12)).grid(row=6, column=1)
        Entry(room_frame, textvariable=self.var_subtotal, font=("arial", 12)).grid(row=7, column=1)
        Entry(room_frame, textvariable=self.var_totalcost, font=("arial", 12)).grid(row=8, column=1)

        btn_frame = Frame(room_frame, relief=RIDGE)
        btn_frame.place(x=10, y=320, width=450, height=35)

        Button(btn_frame, text="Save", command=self.add_data, width=10, bg="black", fg="yellow").grid(row=0, column=0)
        Button(btn_frame, text="Update", command=self.update_data, width=10, bg="black", fg="yellow").grid(row=0, column=1)
        Button(btn_frame, text="Delete", command=self.delete_data, width=10, bg="black", fg="yellow").grid(row=0, column=2)
        Button(btn_frame, text="Reset", command=self.reset_data, width=10, bg="black", fg="yellow").grid(row=0, column=3)
        Button(btn_frame, text="Bill", command=self.calculate_bill, width=10, bg="black", fg="yellow").grid(row=0, column=4)

        # ===== Right Frame (Customer Info) =====
        self.info_frame = LabelFrame(self.root, text="Customer Details", font=("times new roman", 14, "bold"), padx=2, relief=RIDGE)
        self.info_frame.place(x=520, y=90, width=400, height=200)

        self.label_info = Label(self.info_frame, font=("arial", 12), justify=LEFT)
        self.label_info.place(x=0, y=0)

        # ===== Image =====
        img = Image.open(r"C:\Users\91933\OneDrive\Desktop\Hotel management system\images\hotel5.jpeg")
        img = img.resize((300, 200))
        self.room_photo = ImageTk.PhotoImage(img)
        Label(self.root, image=self.room_photo, bd=2, relief=RIDGE).place(x=980, y=90, width=300, height=200)

        # ===== Search Frame =====
        search_frame = LabelFrame(self.root, text="Search System", font=("times new roman", 14, "bold"), padx=2, relief=RIDGE)
        search_frame.place(x=520, y=300, width=910, height=190)

        Label(search_frame, text="Search By", bg="red", fg="white", font=("arial", 12, "bold")).grid(row=0, column=0, padx=2, pady=5)
        combo_search = ttk.Combobox(search_frame, textvariable=self.search_var, state="readonly", font=("arial", 12), width=15)
        combo_search['value'] = ("Contact", "Roomavailable")
        combo_search.grid(row=0, column=1, padx=5)
        combo_search.current(0)

        Entry(search_frame, textvariable=self.txt_search, font=("arial", 12)).grid(row=0, column=2, padx=5)
        Button(search_frame, text="SEARCH", command=self.search_data, width=10, bg="green", fg="white").grid(row=0, column=3, padx=5)
        Button(search_frame, text="SHOW ALL", command=self.fetch_data, width=10, bg="green", fg="white").grid(row=0, column=4, padx=5)

        # ===== Data Table =====
        table_frame = Frame(search_frame, bd=2, relief=RIDGE)
        table_frame.place(x=0, y=40, width=900, height=140)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)
        self.room_table = ttk.Treeview(table_frame, columns=("contact", "checkin", "checkout", "roomtype", "roomavailable", "meal", "days"),
                                       xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)

        for col in self.room_table["columns"]:
            self.room_table.heading(col, text=col.capitalize())
            self.room_table.column(col, width=100)

        self.room_table["show"] = "headings"
        self.room_table.pack(fill=BOTH, expand=1)
        self.room_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    def fetch_contact_data(self):
        if self.var_contact.get() == "":
            messagebox.showerror("Error", "Enter contact number")
            return
        conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
        cursor = conn.cursor()
        cursor.execute("SELECT name, gender, email, nationality, address FROM customer WHERE mobile=%s", (self.var_contact.get(),))
        row = cursor.fetchone()
        if row:
            info = f"Name: {row[0]}\nGender: {row[1]}\nEmail: {row[2]}\nNationality: {row[3]}\nAddress: {row[4]}"
            self.label_info.config(text=info)
        else:
            messagebox.showerror("Error", "Customer not found")
        conn.close()

    def add_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO room (contact, checkin, checkout, roomtype, roomavailable, meal, days) VALUES (%s, %s, %s, %s, %s, %s, %s)", (
            self.var_contact.get(), self.var_checkin.get(), self.var_checkout.get(),
            self.var_roomtype.get(), self.var_roomavailable.get(), self.var_meal.get(), self.var_noofdays.get()
        ))
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Success", "Booking Added")

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM room")
        rows = cursor.fetchall()
        self.room_table.delete(*self.room_table.get_children())
        for row in rows:
            self.room_table.insert("", END, values=row)
        conn.close()

    def get_cursor(self, event=""):
        row = self.room_table.focus()
        content = self.room_table.item(row)
        data = content["values"]
        if data:
            self.var_contact.set(data[0])
            self.var_checkin.set(data[1])
            self.var_checkout.set(data[2])
            self.var_roomtype.set(data[3])
            self.var_roomavailable.set(data[4])
            self.var_meal.set(data[5])
            self.var_noofdays.set(data[6])

    def update_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
        cursor = conn.cursor()
        cursor.execute("""UPDATE room SET checkin=%s, checkout=%s, roomtype=%s, roomavailable=%s,
                          meal=%s, days=%s WHERE contact=%s""", (
            self.var_checkin.get(), self.var_checkout.get(), self.var_roomtype.get(),
            self.var_roomavailable.get(), self.var_meal.get(), self.var_noofdays.get(), self.var_contact.get()
        ))
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Updated", "Record updated")

    def delete_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM room WHERE contact=%s", (self.var_contact.get(),))
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Deleted", "Record deleted")

    def reset_data(self):
        for var in [self.var_contact, self.var_checkin, self.var_checkout, self.var_roomavailable, self.var_meal,
                    self.var_noofdays, self.var_paidtax, self.var_subtotal, self.var_totalcost]:
            var.set("")
        self.var_roomtype.set("Single")
        self.label_info.config(text="")

    def search_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
        cursor = conn.cursor()
        query = f"SELECT * FROM room WHERE {self.search_var.get()} LIKE %s"
        cursor.execute(query, ('%' + self.txt_search.get() + '%',))
        rows = cursor.fetchall()
        self.room_table.delete(*self.room_table.get_children())
        for row in rows:
            self.room_table.insert("", END, values=row)
        conn.close()

    def calculate_bill(self):
        in_date = datetime.strptime(self.var_checkin.get(), "%d/%m/%Y")
        out_date = datetime.strptime(self.var_checkout.get(), "%d/%m/%Y")
        days = (out_date - in_date).days
        self.var_noofdays.set(str(days))

        meal = self.var_meal.get().lower()
        room = self.var_roomtype.get().lower()

        price = 0
        if meal == "breakfast" and room == "single":
            price = 300
        elif meal == "lunch" and room == "single":
            price = 500
        elif meal == "dinner" and room == "single":
            price = 700
        elif meal == "breakfast" and room == "double":
            price = 500
        elif meal == "lunch" and room == "double":
            price = 800
        elif meal == "dinner" and room == "double":
            price = 1000
        elif meal == "breakfast" and room == "luxury":
            price = 1000
        elif meal == "lunch" and room == "luxury":
            price = 1500
        elif meal == "dinner" and room == "luxury":
            price = 2000

        subtotal = days * price
        tax = subtotal * 0.18
        total = subtotal + tax

        self.var_paidtax.set(f"{tax:.2f}")
        self.var_subtotal.set(f"{subtotal:.2f}")
        self.var_totalcost.set(f"{total:.2f}")

if __name__ == "__main__":
    root = Tk()
    obj = RoomBooking(root)
    root.mainloop()





