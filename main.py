from flask import Flask, render_template, request, send_file

import io
import pickle
import random
import qrcode
from fpdf import FPDF
from PIL import Image

app = Flask(__name__)


class Train:
    def __init__(self):
        self.trainno = 0
        self.nofafseat = 0
        self.nofasseat = 0
        self.noffsseat = 0
        self.nofacseat = 0
        self.nofssseat = 0
        self.trainname = ""
        self.startingpoint = ""
        self.destination = ""

    def input(self):
        self.trainno = int(input("ENTER THE TRAIN NUMBER: "))
        self.nofafseat = int(input("ENTER THE NUMBER OF A/C FIRST CLASS SEATS: "))
        self.nofasseat = int(input("ENTER THE NUMBER OF A/C SECOND CLASS SEATS: "))
        self.noffsseat = int(input("ENTER THE NUMBER OF FIRST CLASS SLEEPER SEATS: "))
        self.nofacseat = int(input("ENTER THE NUMBER OF A/C CHAIR CAR SEATS: "))
        self.nofssseat = int(input("ENTER THE NUMBER OF SECOND CLASS SLEEPER SEATS: "))
        self.trainname = input("ENTER THE TRAIN NAME: ")
        self.startingpoint = input("ENTER THE STARTING POINT: ")
        self.destination = input("ENTER THE DESTINATION: ")

    def display(self):
        print(f"TRAIN NUMBER: {self.trainno}")
        print(f"TRAIN NAME: {self.trainname}")
        print(f"NO OF A/C FIRST CLASS SEATS: {self.nofafseat}")
        print(f"NO OF A/C SECOND CLASS SEATS: {self.nofasseat}")
        print(f"NO OF FIRST CLASS SLEEPER SEATS: {self.noffsseat}")
        print(f"NO OF A/C CHAIR CLASS SEATS: {self.nofacseat}")
        print(f"NO OF SECOND CLASS SLEEPER SEATS: {self.nofssseat}")
        print(f"STARTING POINT: {self.startingpoint}")
        print(f"DESTINATION: {self.destination}")
        input("PRESS ANY KEY TO CONTINUE ")

class Tickets:
    def __init__(self):
        self.resno = 0
        self.toaf = 0
        self.nofaf = 0
        self.toas = 0
        self.nofas = 0
        self.tofs = 0
        self.noffs = 0
        self.toac = 0
        self.nofac = 0
        self.toss = 0
        self.nofss = 0
        self.age = 0
        self.status = ""
        self.name = ""

    def generate_receipt(self, train):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Reservation Receipt", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Reservation Number: {self.resno}", ln=True)
        pdf.cell(200, 10, txt=f"Name: {self.name}", ln=True)
        pdf.cell(200, 10, txt=f"Age: {self.age}", ln=True)
        pdf.cell(200, 10, txt=f"Status: {self.status}", ln=True)
        pdf.cell(200, 10, txt=f"Train Number: {train.trainno}", ln=True)
        pdf.cell(200, 10, txt=f"Train Name: {train.trainname}", ln=True)
        pdf.cell(200, 10, txt=f"Starting Point: {train.startingpoint}", ln=True)
        pdf.cell(200, 10, txt=f"Destination: {train.destination}", ln=True)

# Generate QR code
        qr_data = f"Reservation Number: {self.resno}\nName: {self.name}\nAge: {self.age}\nStatus: {self.status}\nTrain Number: {train.trainno}\nTrain Name: {train.trainname}\nStarting Point: {train.startingpoint}\nDestination: {train.destination}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill='black', back_color='white')
        img_path = f"qr_{self.resno}.png"
        img.save(img_path)
        
        # Ensure image is in RGB mode
        img = Image.open(img_path).convert('RGB')
        img.save(img_path)
        
        # Embed QR code in PDF
        pdf.image(img_path, x=10, y=100, w=50)
        pdf.output(f"Reservation_{self.resno}.pdf")
        print(f"Receipt generated: Reservation_{self.resno}.pdf")

    def display(self):
        try:
            with open("Ticket1.dat", "rb") as file:
                tickets = pickle.load(file)
        except (FileNotFoundError, EOFError):
            print("ERROR IN THE FILE")
            return

        n = int(input("ENTER THE RESERVATION NO: "))
        found = False

        for ticket in tickets:
            if ticket.resno == n:
                found = True
                print(f"NAME: {ticket.name}")
                print(f"AGE: {ticket.age}")
                print(f"PRESENT STATUS: {ticket.status}")
                print(f"RESERVATION NUMBER: {ticket.resno}")
                break

        if not found:
            a = input("UNRECOGNIZED RESERVATION NO !!! WANNA RETRY? (Y/N): ")
            if a.lower() == 'y':
                self.display()

    def reservation(self):
        tno = int(input("ENTER THE TRAIN NO: "))
        found = False

        try:
            with open("Train1.dat", "rb") as file:
                trains = pickle.load(file)
        except (FileNotFoundError, EOFError):
            print("ERROR IN THE FILE")
            return

        # Find the train based on train number (tno)
        for train in trains:
            if train.trainno == tno:
                found = True
                # Store train details in a variable
                selected_train = train
                # Set tickets count based on selected train
                self.nofaf = train.nofafseat
                self.nofas = train.nofasseat
                self.noffs = train.noffsseat
                self.nofac = train.nofacseat
                self.nofss = train.nofssseat
                break

        if not found:
            print("ERROR IN THE TRAIN NUMBER ENTERED!!!")
            return

        tickets = []
        try:
            with open("Ticket1.dat", "rb") as file:
                tickets = pickle.load(file)
        except (FileNotFoundError, EOFError):
            pass

        while True:
            self.name = input("NAME: ")
            self.age = int(input("AGE: "))
            print("SELECT THE CLASS WHICH YOU WISH TO TRAVEL")
            print("1. A/C FIRST CLASS")
            print("2. A/C SECOND CLASS")
            print("3. FIRST CLASS SLEEPER")
            print("4. A/C CHAIR CAR")
            print("5. SECOND CLASS SLEEPER")
            c = int(input("ENTER YOUR CHOICE: "))

            if c == 1:
                self.toaf += 1
                self.resno = random.randint(100000, 999999)
                self.status = "confirmed" if (self.nofaf - self.toaf) > 0 else "pending"
            elif c == 2:
                self.toas += 1
                self.resno = random.randint(100000, 999999)
                self.status = "confirmed" if (self.nofas - self.toas) > 0 else "pending"
            elif c == 3:
                self.tofs += 1
                self.resno = random.randint(100000, 999999)
                self.status = "confirmed" if (self.noffs - self.tofs) > 0 else "pending"
            elif c == 4:
                self.toac += 1
                self.resno = random.randint(109900, 999999)
                self.status = "confirmed" if (self.nofac - self.toac) > 0 else "pending"
            elif c == 5:
                self.toss += 1
                self.resno = random.randint(100000, 999999)
                self.status = "confirmed" if (self.nofss - self.toss) > 0 else "pending"
            else:
                print("Invalid choice!")
                continue

            print(f"STATUS: {self.status}")
            print(f"RESERVATION NO: {self.resno}")
            tickets.append(self)
            
            # Generate receipt with both ticket and train details
            self.generate_receipt(selected_train)

            n = input("DO YOU WISH TO CONTINUE BOOKING TICKETS (Y/N)? ")
            if n.lower() != 'y':
                break

        with open("Ticket1.dat", "wb") as file:
            pickle.dump(tickets, file)

    def cancellation(self):
        try:
            with open("Ticket1.dat", "rb") as file:
                tickets = pickle.load(file)
        except (FileNotFoundError, EOFError):
            print("ERROR IN THE FILE!!!")
            return

        r = int(input("ENTER THE RESERVATION NO: "))
        found = False
        updated_tickets = []

        for ticket in tickets:
            if ticket.resno != r:
                updated_tickets.append(ticket)
            else:
                found = True

        with open("Ticket1.dat", "wb") as file:
            pickle.dump(updated_tickets, file)

        if not found:
            print("NO SUCH RESERVATION IS MADE!!! PLEASE RETRY")
        else:
            print("RESERVATION CANCELLED")
        input()

def showMenu():
    print("==========================")
    print("RAILWAY TICKET RESERVATION")
    print("==========================")
    print("1. TRAIN DETAILS")
    print("2. UPDATE TRAIN DETAILS")
    print("3. RESERVING A TICKET")
    print("4. CANCELLING A TICKET")
    print("5. DISPLAY THE PRESENT TICKET STATUS")
    print("6. EXIT")
    print("ENTER YOUR CHOICE: ", end='')

def main():
    while True:
        showMenu()
        try:
            choice = int(input())
            tr = Train()
            tick = Tickets()

            if choice == 1:
                try:
                    with open("Train1.dat", "rb") as file:
                        trains = pickle.load(file)
                except (FileNotFoundError, EOFError):
                    print("ERROR IN THE FILE !!!")
                else:
                    for train in trains:
                        train.display()
            elif choice == 2:
                password = int(input("ENTER THE PASSWORD: "))
                if password == 1234:  # assuming 1234 as the password
                    try:
                        with open("Train1.dat", "rb") as file:
                            trains = pickle.load(file)
                    except (FileNotFoundError, EOFError):
                        trains = []

                    continueUpdating = 'y'
                    while continueUpdating.lower() == 'y':
                        tr.input()
                        trains.append(tr)
                        continueUpdating = input("DO YOU WISH TO CONTINUE UPDATING? (Y/N): ")

                    with open("Train1.dat", "wb") as file:
                        pickle.dump(trains, file)
                else:
                    print("INVALID PASSWORD!!!")
            elif choice == 3:
                tick.reservation()
            elif choice == 4:
                tick.cancellation()
            elif choice == 5:
                tick.display()
            elif choice == 6:
                exit(0)
            else:
                print("INVALID CHOICE!!!")
        except ValueError:
            print("Invalid input. Please enter a valid integer.")

if __name__ == "__main__":
    main()