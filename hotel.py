from tkinter import *
from PIL import Image, ImageTk
from customer import Customer_window
from rooms import RoomBooking
from details import RoomDetails


class HotelManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Management System")
        self.root.state("zoomed")  # Fullscreen window

        # === Top Image ===
        img1 = Image.open(r"C:\Users\91933\OneDrive\Desktop\Hotel management system\images\hotel9.jpeg")
        img1 = img1.resize((1550, 140), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE).place(x=0, y=0, width=1550, height=140)

        # === Logo ===
        img2 = Image.open(r"C:\Users\91933\OneDrive\Desktop\Hotel management system\images\logo1.png")
        img2 = img2.resize((230, 140), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE).place(x=0, y=0, width=230, height=140)

        # === Title ===
        Label(self.root, text="HOTEL MANAGEMENT SYSTEM", font=("times new roman", 35, "bold"),
              bg="black", fg="aqua", bd=4, relief=RIDGE).place(x=0, y=140, width=1550, height=50)

        # === Main Frame ===
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=620)

        # === Sidebar Menu ===
        Label(main_frame, text="MENU", font=("times new roman", 20, "bold"), bg="black", fg="aqua", bd=4,
              relief=RIDGE).place(x=0, y=0, width=230)

        btn_frame = Frame(main_frame, bd=4, relief=RIDGE)
        btn_frame.place(x=0, y=35, width=228, height=190)

        Button(btn_frame, text="CUSTOMER",command=self.cust_details,width=22, font=("times new roman", 14, "bold"),
               bg="black", fg="aqua", bd=0, cursor="hand2").grid(row=0, column=0, pady=1)
        Button(btn_frame, text="ROOM",command=self.open_room_window,width=22, font=("times new roman", 14, "bold"),
               bg="black", fg="aqua", bd=0, cursor="hand2").grid(row=1, column=0, pady=1)
        Button(btn_frame, text="DETAILS", command=self.open_details,width=22, font=("times new roman", 14, "bold"),
               bg="black", fg="aqua", bd=0, cursor="hand2").grid(row=2, column=0, pady=1)           

        Button(btn_frame, text="REPORT", width=22, font=("times new roman", 14, "bold"),
               bg="black", fg="aqua", bd=0, cursor="hand2").grid(row=3, column=0, pady=1)
        Button(btn_frame, text="LOGOUT", command=self.logout,width=22, font=("times new roman", 14, "bold"),
               bg="black", fg="aqua", bd=0, cursor="hand2").grid(row=4, column=0, pady=1)

        # === Right Image ===
        img3 = Image.open(r"C:\Users\91933\OneDrive\Desktop\Hotel management system\images\hotel5.jpeg")
        img3 = img3.resize((1310, 590), Image.Resampling.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        Label(main_frame, image=self.photoimg3, bd=4, relief=RIDGE).place(x=225, y=0, width=1310, height=590)

        # === Bottom Images ===
        img4 = Image.open(r"C:\Users\91933\OneDrive\Desktop\Hotel management system\images\dishes.jpg")
        img4 = img4.resize((230, 210), Image.Resampling.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)
        Label(main_frame, image=self.photoimg4, bd=4, relief=RIDGE).place(x=0, y=225, width=230, height=210)

        img5 = Image.open(r"C:\Users\91933\OneDrive\Desktop\Hotel management system\images\outside.jpg")
        img5 = img5.resize((230, 210), Image.Resampling.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)
        Label(main_frame, image=self.photoimg5, bd=4, relief=RIDGE).place(x=0, y=420, width=230, height=210)



    def cust_details(self):
         self.new_window = Toplevel(self.root)
         self.new_window.state("zoomed")
         self.app = Customer_window(self.new_window)




    def open_room_window(self):
        new_window = Toplevel(self.root)
        RoomBooking(new_window)


    def open_details(self):
        new_window = Toplevel(self.root)
        RoomDetails(new_window)


    
    def logout(self):
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = HotelManagementSystem(root)
    root.mainloop()



