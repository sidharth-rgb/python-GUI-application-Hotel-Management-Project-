from tkinter import *
from tkinter import ttk, messagebox
import random
import mysql.connector

class Customer_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Details")
        self.root.state("zoomed")

        # ===== Variables =====
        self.var_ref = StringVar()
        x = random.randint(1000, 9999)
        self.var_ref.set(str(x))

        self.var_name = StringVar()
        self.var_mother = StringVar()
        self.var_gender = StringVar(value="Male")
        self.var_post = StringVar()
        self.var_mobile = StringVar()
        self.var_email = StringVar()
        self.var_nationality = StringVar(value="Indian")
        self.var_id_proof = StringVar(value="AadharCard")
        self.var_id_number = StringVar()
        self.var_address = StringVar()

        # ===== Title =====
        title = Label(self.root, text="ADD CUSTOMER DETAILS", font=("times new roman", 30, "bold"),
                      bg="black", fg="yellow", bd=4, relief=RIDGE)
        title.place(x=0, y=0, width=1550, height=50)

        # ===== Main Frame =====
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=10, y=60, width=1500, height=650)

        # ===== Left Frame =====
        left_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="Customer Details",
                                font=("times new roman", 16, "bold"))
        left_frame.place(x=10, y=10, width=600, height=620)

        # ===== Entry Fields =====
        labels = ["Customer Ref", "Customer Name", "Mother Name", "Gender", "PostCode",
                  "Mobile", "Email", "Nationality", "Id Proof Type", "Id Number", "Address"]
        for i, text in enumerate(labels):
            Label(left_frame, text=text + ":", font=("times new roman", 13, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky=W)

        Entry(left_frame, textvariable=self.var_ref, width=30, font=("arial", 13)).grid(row=0, column=1)
        Entry(left_frame, textvariable=self.var_name, width=30, font=("arial", 13)).grid(row=1, column=1)
        Entry(left_frame, textvariable=self.var_mother, width=30, font=("arial", 13)).grid(row=2, column=1)

        gender_cb = ttk.Combobox(left_frame, textvariable=self.var_gender, font=("arial", 13), state="readonly", width=28)
        gender_cb["values"] = ("Male", "Female", "Other")
        gender_cb.grid(row=3, column=1)

        Entry(left_frame, textvariable=self.var_post, width=30, font=("arial", 13)).grid(row=4, column=1)
        Entry(left_frame, textvariable=self.var_mobile, width=30, font=("arial", 13)).grid(row=5, column=1)
        Entry(left_frame, textvariable=self.var_email, width=30, font=("arial", 13)).grid(row=6, column=1)

        nationality_cb = ttk.Combobox(left_frame, textvariable=self.var_nationality, font=("arial", 13), state="readonly", width=28)
        nationality_cb["values"] = ("Indian", "American", "British", "Other")
        nationality_cb.grid(row=7, column=1)

        id_cb = ttk.Combobox(left_frame, textvariable=self.var_id_proof, font=("arial", 13), state="readonly", width=28)
        id_cb["values"] = ("AadharCard", "Passport", "Driving License")
        id_cb.grid(row=8, column=1)

        Entry(left_frame, textvariable=self.var_id_number, width=30, font=("arial", 13)).grid(row=9, column=1)
        Entry(left_frame, textvariable=self.var_address, width=30, font=("arial", 13)).grid(row=10, column=1)

        # ===== Buttons =====
        btn_frame = Frame(left_frame, bd=0, relief=RIDGE)
        btn_frame.place(x=0, y=500, width=580, height=40)

        Button(btn_frame, text="Add", width=13, font=("arial", 12, "bold"), bg="black", fg="white", command=self.add_data).grid(row=0, column=0, padx=5)
        Button(btn_frame, text="Update", width=13, font=("arial", 12, "bold"), bg="black", fg="white", command=self.update_data).grid(row=0, column=1, padx=5)
        Button(btn_frame, text="Delete", width=13, font=("arial", 12, "bold"), bg="black", fg="white", command=self.delete_data).grid(row=0, column=2, padx=5)
        Button(btn_frame, text="Reset", width=13, font=("arial", 12, "bold"), bg="black", fg="white", command=self.reset_fields).grid(row=0, column=3, padx=5)

        # ===== Right Frame =====
        right_frame = LabelFrame(main_frame, bd=2, relief=RIDGE, text="View Details And Search System",
                                 font=("times new roman", 12, "bold"))
        right_frame.place(x=620, y=10, width=860, height=620)

        lbl_search = Label(right_frame, text="Search By:", font=("times new roman", 12, "bold"), bg="red", fg="white")
        lbl_search.grid(row=0, column=0, sticky=W, padx=10, pady=5)

        self.var_search = StringVar()
        combo_search = ttk.Combobox(right_frame, textvariable=self.var_search, font=("arial", 13), state="readonly", width=20)
        combo_search["values"] = ("Mobile", "Ref")
        combo_search.grid(row=0, column=1, padx=10, pady=5)

        self.txt_search = StringVar()
        Entry(right_frame, textvariable=self.txt_search, font=("arial", 13), width=20).grid(row=0, column=2, padx=10)

        
        Button(right_frame, text="Search", font=("arial", 12, "bold"), width=12, bg="black", fg="white", command=self.search_data).grid(row=0, column=3, padx=10)
        Button(right_frame, text="Show All", font=("arial", 12, "bold"), width=12, bg="black", fg="white", command=self.show_all_data).grid(row=0, column=4, padx=10)


        table_frame = Frame(right_frame, bd=2, relief=RIDGE)
        table_frame.place(x=5, y=50, width=840, height=550)

        scroll_x = Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(table_frame, orient=VERTICAL)

        self.customer_table = ttk.Treeview(table_frame, columns=("ref", "name", "mother", "gender", "post", "mobile", "email",
                                                                 "nationality", "id_proof", "id_number", "address"),
                                           xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        scroll_x.config(command=self.customer_table.xview)
        scroll_y.config(command=self.customer_table.yview)

        for col in self.customer_table["columns"]:
            self.customer_table.heading(col, text=col.title())
            self.customer_table.column(col, width=100)

        self.customer_table["show"] = "headings"
        self.customer_table.pack(fill=BOTH, expand=1)
        self.customer_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()
    # ======add button functionality=========
    def add_data(self):
        if self.var_mobile.get() == "" or self.var_mother.get() == "":
            messagebox.showerror("Error", "All fields are required")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO customer (ref, name, mother, gender, postcode, mobile, email, nationality, idproof, idnumber, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                    self.var_ref.get(),
                    self.var_name.get(),
                    self.var_mother.get(),
                    self.var_gender.get(),
                    self.var_post.get(),
                    self.var_mobile.get(),
                    self.var_email.get(),
                    self.var_nationality.get(),
                    self.var_id_proof.get(),
                    self.var_id_number.get(),
                    self.var_address.get()
                ))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Customer has been added", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM customer")
        rows = my_cursor.fetchall()
        if rows:
            self.customer_table.delete(*self.customer_table.get_children())
            for row in rows:
                self.customer_table.insert("", END, values=row)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.customer_table.focus()
        content = self.customer_table.item(cursor_row)
        row = content["values"]
        self.var_ref.set(row[0])
        self.var_name.set(row[1])
        self.var_mother.set(row[2])
        self.var_gender.set(row[3])
        self.var_post.set(row[4])
        self.var_mobile.set(row[5])
        self.var_email.set(row[6])
        self.var_nationality.set(row[7])
        self.var_id_proof.set(row[8])
        self.var_id_number.set(row[9])
        self.var_address.set(row[10])
  #============== update button functionality==================   
    def update_data(self):
        if self.var_mobile.get() == "":
            messagebox.showerror("Error", "Please select a customer to update")
        else:
            conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
            my_cursor = conn.cursor()
            my_cursor.execute("""UPDATE customer SET 
                name=%s, mother=%s, gender=%s, postcode=%s, mobile=%s, email=%s,
                nationality=%s, idproof=%s, idnumber=%s, address=%s
                WHERE ref=%s""", (
                self.var_name.get(),
                self.var_mother.get(),
                self.var_gender.get(),
                self.var_post.get(),
                self.var_mobile.get(),
                self.var_email.get(),
                self.var_nationality.get(),
                self.var_id_proof.get(),
                self.var_id_number.get(),
                self.var_address.get(),
                self.var_ref.get()
            ))
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Updated", "Customer details updated successfully", parent=self.root)
    # ================= delete button functionality================
    def delete_data(self):
        if self.var_ref.get() == "":
            messagebox.showerror("Error", "Please select a customer to delete")
        else:
            confirm = messagebox.askyesno("Confirm Delete", "Do you really want to delete?", parent=self.root)
            if confirm:
                conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
                my_cursor = conn.cursor()
                my_cursor.execute("DELETE FROM customer WHERE ref=%s", (self.var_ref.get(),))
                conn.commit()
                conn.close()
                self.fetch_data()
                self.reset_fields()
                messagebox.showinfo("Deleted", "Customer record deleted", parent=self.root)
#   ==================reset button functionality========================
    def reset_fields(self):
        x = random.randint(1000, 9999)
        self.var_ref.set(str(x))
        self.var_name.set("")
        self.var_mother.set("")
        self.var_gender.set("Male")
        self.var_post.set("")
        self.var_mobile.set("")
        self.var_email.set("")
        self.var_nationality.set("Indian")
        self.var_id_proof.set("AadharCard")
        self.var_id_number.set("")
        self.var_address.set("")
    
    def search_data(self):
        if self.var_search.get() == "" or self.txt_search.get() == "":
              messagebox.showerror("Error", "Please select a search category and enter text")
        else:
          try:
            conn = mysql.connector.connect(host="localhost", user="root", password="susi", database="management")
            my_cursor = conn.cursor()
            query = f"SELECT * FROM customer WHERE {self.var_search.get()} LIKE %s"
            my_cursor.execute(query, (f"%{self.txt_search.get()}%",))
            rows = my_cursor.fetchall()
            if len(rows) != 0:
                self.customer_table.delete(*self.customer_table.get_children())
                for row in rows:
                    self.customer_table.insert("", END, values=row)
            else:
                messagebox.showinfo("Info", "No matching records found.")
            conn.close()
          except Exception as e:
            messagebox.showerror("Error", f"Search failed: {str(e)}", parent=self.root)

    def show_all_data(self):
           self.fetch_data()





    

if __name__ == "__main__":
       root = Tk()
       obj =  Customer_window(root)
       root.mainloop()







































































































































































































































































































































































































































































































































