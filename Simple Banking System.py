# Write your code here
import random
import sqlite3


class Banking:

    # CONNECTING TO THE DATABASE
    conn = sqlite3.connect('card.s3db')
    c = conn.cursor()


    # CREATING THE TABLE IF NOT EXISTS
    c.execute("""CREATE TABLE IF NOT EXISTS card (
                id      INTEGER PRIMARY KEY,
                number  TEXT,
                pin     TEXT,
                balance INTEGER DEFAULT 0)
              """)

    conn.commit()

    def __init__(self):
        self.card_number = ''
        self.card_pin = ''
        self.balance = 0
        self.id = 0
        self.UI()

# ----------------------------------------------------
    # TEST IF LUHN ALGORITHM
    def luhn_checksum(self, card_number):
        def digits_of(n):
            return [int(d) for d in str(n)]

        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = 0
        checksum += sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10

    def is_luhn_valid(self, card_number):
        return self.luhn_checksum(card_number) == 0
# ----------------------------------------------------

    # CREATING THE UI
    def UI(self):
        print('\n1. Create an account \n'
              '2. Log into account \n'
              '0. Exit')
        option = input('>')

        self.actions(option)

    # CREATE THE CREDIT CARD NUMBER WITH ALL THE RESTRICTIONS (LUHN ALGORITHM)
    def create_credit_card(self):
        self.card_number = '400000' + str(random.randint(10 ** 8, 10 ** 9 - 1))
        tmp_card_number = list(map(int, self.card_number))

        for i in range(len(tmp_card_number)):
            if not i % 2:
                tmp_card_number[i] = tmp_card_number[i] * 2
        tmp_card_number = [x - 9 if x > 9 else x for x in tmp_card_number]
        if sum(tmp_card_number) % 10 == 0:
            last_digit = 0
        else:
            last_digit = 10 - sum(tmp_card_number) % 10
        print(last_digit)

        self.card_number = self.card_number + str(last_digit)
        print(self.card_number)
        return self.card_number

    # CREATE THE PIN
    def create_pin(self):
        self.card_pin = str(random.randint(10 ** 3, 10 ** 4 - 1))
        print(self.card_pin)
        return self.card_pin

    # ADDING THE ACCOUNT INTO DATABASE
    def add_account(self):
        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()

        c.execute("INSERT INTO card VALUES (NULL, :number, :pin, :balance)", {'number': self.card_number,
                                                                              'pin': self.card_pin,
                                                                              'balance': self.balance
                                                                              })


        conn.commit()
        conn.close()

    # CREATING THE ACCOUNT
    def create_account(self):
        print('Your card has been created')
        print('Your card number:')
        self.create_credit_card()
        print('Your card PIN:')
        self.create_pin()
        self.add_account()

    # CREATING THE LOGIN APP
    def login(self):
        print('Enter your card number:')
        card_number = input()
        print('Enter your PIN:')
        card_pin = input()

        conn = sqlite3.connect('card.s3db')
        c = conn.cursor()

        c.execute("SELECT * FROM card WHERE number=(?)", (card_number,))
        card_number_test = c.fetchall()
        c.execute("SELECT * FROM card WHERE number=(?) AND pin=(?)", (card_number, card_pin))
        card_number_and_pin_test = c.fetchall()

        if card_number_test and card_number_and_pin_test:
            print('You have successfully logged in!')
        else:
            print('Wrong card number or PIN')
            self.UI()

        # UI FOR THE ACCOUNT MENU
        def account_menu():
            print('\n1. Balance\n'
                  '2. Add income \n'
                  '3. Do transfer \n'
                  '4. Close account \n'
                  '5. Log out\n'
                  '0. Exit')
            option = input('>')

            if option == '1':
                c.execute("SELECT balance FROM card WHERE number=(?)", (card_number,))
                print('\nBalance:', c.fetchone()[0])
                account_menu()
            elif option == '2':
                print('Enter income:')
                income = int(input())
                c.execute("UPDATE card SET balance=balance+(?) WHERE number=(?)", (income, card_number))
                conn.commit()
                print('Income was added!')
                account_menu()
            elif option == '3':
                print('Enter card number:')
                curr_balance = c.execute("SELECT balance FROM card WHERE number=(?)", (card_number,)).fetchone()[0]

                transfer_to = input()

                if card_number == transfer_to:
                    print("You can't transfer money to the same account!")
                    account_menu()

                test_exists = c.execute("SELECT EXISTS (SELECT 1 FROM card WHERE number=(?))", (transfer_to,)).fetchone() == (1,)

                if test_exists:
                    transfer_sum = int(input())
                    if curr_balance > transfer_sum:
                        c.execute("UPDATE card SET balance=balance+(?) WHERE number=(?)", (transfer_sum, transfer_to))
                        c.execute("UPDATE card SET balance=balance-(?) WHERE number=(?)", (transfer_sum, card_number))
                        conn.commit()
                        account_menu()
                    else:
                        print('Not enough money!')
                        account_menu()
                elif not self.is_luhn_valid(int(transfer_to)):
                    print('Probably you made a mistake in the card number. Please try again!')
                    account_menu()
                else:
                    print('Such a card does not exist.')
                    account_menu()
            elif option == '4':
                c.execute("DELETE FROM card WHERE number=(?)", (self.card_number,))
                conn.commit()
                print('\nThe account has been closed!')
                account_menu()
            elif option == '5':
                print('\nYou have successfully logged out! \n')
                self.UI()
            elif option == '0':
                print('\nBye!')
                exit()

        account_menu()

    # CREATING THE ACTION MENU
    def actions(self, action):
        if action == '1':
            self.create_account()
            self.UI()
        elif action == '2':
            self.login()
        elif action == '0':
            print('\nBye!')
            exit()


if __name__ == "__main__":
    Banking()
