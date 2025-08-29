import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class RoomDetails:
    def __init__(self, root):
        self.root = root
        self.root.title("Room Booking Details")
        self.root.geometry("1300x550+226+220")

        # Variables
        self.var_floor = tk.StringVar()
        self.var_room_no = tk.StringVar()
        self.var_room_type = tk.StringVar()

        # Title
        title = tk.Label(self.root, text="ROOMBOOKING DETAILS", font=("times new roman", 20, "bold"), bg="black", fg="yellow")
        title.pack(side="top", fill="x")

        # Left frame (form)
        left_frame = tk.LabelFrame(self.root, bd=2, relief=tk.RIDGE, text="New Room Add", padx=2, font=("arial", 12, "bold"))
        left_frame.place(x=10, y=50, width=400, height=250)

        # Floor
        lbl_floor = tk.Label(left_frame, text="Floor", font=("arial", 12, "bold"))
        lbl_floor.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        entry_floor = ttk.Entry(left_frame, textvariable=self.var_floor, width=20, font=("arial", 12))
        entry_floor.grid(row=0, column=1, padx=10, pady=5)

        # Room No
        lbl_room_no = tk.Label(left_frame, text="Room No", font=("arial", 12, "bold"))
        lbl_room_no.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        entry_room_no = ttk.Entry(left_frame, textvariable=self.var_room_no, width=20, font=("arial", 12))
        entry_room_no.grid(row=1, column=1, padx=10, pady=5)

        # Room Type
        lbl_room_type = tk.Label(left_frame, text="Room Type", font=("arial", 12, "bold"))
        lbl_room_type.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_room_type = ttk.Entry(left_frame, textvariable=self.var_room_type, width=20, font=("arial", 12))
        entry_room_type.grid(row=2, column=1, padx=10, pady=5)

        # Button Frame
        btn_frame = tk.Frame(left_frame, bd=0, relief=tk.RIDGE)
        btn_frame.place(x=0, y=140, width=370, height=40)

        btn_add = tk.Button(btn_frame, text="Add", command=self.add_data, font=("arial", 11, "bold"), bg="black", fg="yellow", width=8)
        btn_add.grid(row=0, column=0, padx=2)

        btn_update = tk.Button(btn_frame, text="Update", command=self.update_data, font=("arial", 11, "bold"), bg="black", fg="yellow", width=8)
        btn_update.grid(row=0, column=1, padx=2)

        btn_delete = tk.Button(btn_frame, text="Delete", command=self.delete_data, font=("arial", 11, "bold"), bg="black", fg="yellow", width=8)
        btn_delete.grid(row=0, column=2, padx=2)

        btn_reset = tk.Button(btn_frame, text="Reset", command=self.reset_data, font=("arial", 11, "bold"), bg="black", fg="yellow", width=8)
        btn_reset.grid(row=0, column=3, padx=2)

        # Right frame (Table)
        table_frame = tk.LabelFrame(self.root, bd=2, relief=tk.RIDGE, text="Show Room Details", padx=2, font=("arial", 12, "bold"))
        table_frame.place(x=420, y=50, width=560, height=350)

        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        self.room_table = ttk.Treeview(table_frame, columns=("floor", "roomno", "roomtype"),
                                       xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)

        scroll_x.config(command=self.room_table.xview)
        scroll_y.config(command=self.room_table.yview)

        self.room_table.heading("floor", text="Floor")
        self.room_table.heading("roomno", text="Room No")
        self.room_table.heading("roomtype", text="Room Type")

        self.room_table["show"] = "headings"
        self.room_table.column("floor", width=100)
        self.room_table.column("roomno", width=100)
        self.room_table.column("roomtype", width=100)

        self.room_table.pack(fill=tk.BOTH, expand=1)
        self.room_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    # ========== DATABASE FUNCTIONS ==========

    def add_data(self):
        if self.var_floor.get() == "" or self.var_room_no.get() == "":
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="susi", database="management")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO details (floor, room_no, room_type) VALUES (%s, %s, %s)",
                           (self.var_floor.get(), self.var_room_no.get(), self.var_room_type.get()))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Room added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {str(e)}")

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="susi", database="management")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM details")
            rows = cursor.fetchall()
            if rows:
                self.room_table.delete(*self.room_table.get_children())
                for row in rows:
                    self.room_table.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Fetch failed: {str(e)}")

    def get_cursor(self, event=""):
        row = self.room_table.focus()
        content = self.room_table.item(row)
        data = content["values"]
        if data:
            self.var_floor.set(data[0])
            self.var_room_no.set(data[1])
            self.var_room_type.set(data[2])

    def update_data(self):
        if self.var_floor.get() == "" or self.var_room_no.get() == "":
            messagebox.showerror("Error", "All fields are required.")
            return
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="susi", database="management")
            cursor = conn.cursor()
            cursor.execute("UPDATE details SET floor=%s, room_type=%s WHERE room_no=%s",
                           (self.var_floor.get(), self.var_room_type.get(), self.var_room_no.get()))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Room updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")

    def delete_data(self):
        confirm = messagebox.askyesno("Delete", "Are you sure you want to delete this room?")
        if confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="1234", database="hotel")
                cursor = conn.cursor()
                cursor.execute("DELETE FROM details WHERE room_no=%s", (self.var_room_no.get(),))
                conn.commit()
                self.fetch_data()
                conn.close()
                self.reset_data()
                messagebox.showinfo("Deleted", "Room deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Delete failed: {str(e)}")

    def reset_data(self):
        self.var_floor.set("")
        self.var_room_no.set("")
        self.var_room_type.set("")


# Run
if __name__ == "__main__":
    root = tk.Tk()
    obj = RoomDetails(root)
    root.mainloop()
