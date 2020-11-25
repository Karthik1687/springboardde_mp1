from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from adders import addCustomer, addEmployee, addChecking
from getters import _getCheckingAccount
from setters import _setFloat, updateMonthlyFee, updateInterestRate, updateBalance, updateDebitCard
from classes import Base
import re


engine = create_engine('sqlite:///data.sqlite', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base.metadata.create_all(engine)
continueLoop = True
while continueLoop:
    print("Please select an action:")
    userInput = str(input("1. Add Customer \n2. Add Employee \n3. Add Account (Checking or Savings) \n" + \
                          "4. Increase interest Rate \n5. Increase Monthly Fee \n6. Deposit or Withdrawal \n7. Attach Debit Card \n" +\
                          "8. Quit"))
    if len(userInput) == 1 and bool(re.search("\\d", userInput)):
        if int(userInput) >= 1 or int(userInput) <= 8:
            condition = False
        else:
            print("Please enter a valid selection (1)")
    else:
        print("Please enter a valid selection (2)")

    if int(userInput) == 1:
        addCustomer(session)

    elif int(userInput) == 2:
        addEmployee(session)

    elif int(userInput) == 3:
        addChecking(session)

    elif int(userInput) == 4:
        id = input("What is the account number that you would like to increase the interest for?")
        if not _getCheckingAccount(session, int(id)):
            id = input("Please enter a valid account number")
        newInterest = _setFloat(input("What would you like to increase the interest rate by?"))
        if updateInterestRate(session, id, newInterest):
            print("Interest rate successfully updated")

    elif int(userInput) == 5:
        id = input("What is the account number that you would like to increase the monhtly fee for?")
        if not _getCheckingAccount(session, int(id)):
            id = input("Please enter a valid account number")
        newFee = _setFloat(input("What would you like to increase the monthly fee by?"))
        if updateMonthlyFee(session, id, newFee):
            print("Monthly fee successfully updated")

    elif int(userInput) == 6:
        id = input("What is the account number that you would like to deposit? (Withdrawals are negative)")
        if not _getCheckingAccount(session, int(id)):
            id = input("Please enter a valid account number")
        newFee = _setFloat(input("What would you like to increase or decrease the balance by?"))
        if updateBalance(session, id, newFee):
            print("Deposit or withdrawal successful")

    elif int(userInput) == 7:
        id = input("What is the account number that you would like to attach a debit card to?")
        if not _getCheckingAccount(session, int(id)):
            id = input("Please enter a valid account number")
        if updateDebitCard(session, id, True):
            print("Debit card added")

    elif int(userInput) == 8:
        continueLoop = False
