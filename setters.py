from datetime import datetime
import re
from classes import CheckingAccount, Base

def _reIssueDateFn(date):
    '''
    This function takes a possible date value and checks to see if it is valid. If not, it requires the user to correct
    :param date: String
    :return: Valid datetime value
    '''
    validDate = False
    reIssueDate = str(date)
    while not validDate:
        try:
            datetime.strptime(reIssueDate, "%Y-%m-%d")
        except ValueError as e:
            reIssueDate = str(input("Invalid date format, please use '%Y-%m-%d'"))
        else:
            validDate = True
    return datetime.strptime(reIssueDate, "%Y-%m-%d")

def _parseUserInput(displayText, expectedNumber):
    '''
    If a user enters the wrong number of arguments, it prompts the user to enter them again matches it up against the
    correct number.
    :param displayText: String
    :param expectedNumber: integer
    :return: list of strings
    '''
    details = input(displayText)
    while len(details.split(" ")) != expectedNumber:
        details = input("Please enter the correct number of arguments ({args})".format(args=expectedNumber))
    return details.split(" ")


def _setString(inputString):
    '''
    Checks to make sure an input string consists only of characters and prompts the user to enter it again if its
    incorrect
    :param inputString: String
    :return: String
    '''
    reIssueName = str(inputString)
    while sum([char.isdigit() for char in reIssueName]) > 0 or len(reIssueName) > 15:
        print(reIssueName)
        reIssueName = input("Please ensure the string entered is free of digits and less than 15 characters")
    return str(reIssueName)

def _setFloat(inputFloat):
    '''
    Takes a particular string and checks to see if it is a float number
    :param inputFloat: String
    :return: Float
    '''
    reIssueFloat = inputFloat
    while not all([bool(re.search("(\d|\.)", char)) for char in str(reIssueFloat)]):
        reIssueFloat = input("Please enter a valid floating number")
    return float(reIssueFloat)

def _updateString(session, typeID, ID, objectType, inputStringVar, inputStringVal):
    '''
    Helper function to update a particular column.
    :param session: Session
    :param typeID: String
    :param ID: Integer
    :param objectType: String
    :param inputStringVar: String
    :param inputStringVal: String or Float
    :return: Boolean
    '''
    result = session.query(objectType).filter(getattr(objectType, typeID).__eq__(ID))
    if result.count() == 1:
        if getattr(result.first(), inputStringVar).__class__.__name__ in ['str','bool']:
            newVal = inputStringVal
        elif getattr(result.first(), inputStringVar).__class__.__name__ in ['float', 'int']:
            newVal = getattr(result.first(), inputStringVar) + inputStringVal
        result.update({inputStringVar: (newVal)})
        session.commit()
        return True
    elif result.count() > 1:
        print("Found too many")
        return False
    elif result.count() == 0:
        print("Unable to find row to update")
        return False

def _checkValue(session, typeID, ID, objectType, inputStringVar, increaseVal, limit):
    '''
    Function checks to see whether the variable being updated along with the original value is within constraints
    :param session: Session
    :param typeID: String
    :param ID: Integer
    :param objectType: String
    :param inputStringVar: String
    :param increaseVal: String or Integer
    :param limit: Contraint list
    :return: Boolean
    '''
    result = session.query(objectType).filter(getattr(objectType, typeID).__eq__(ID))
    result = getattr(result, inputStringVar)

    if result.__class__.__name__ in ['float','int']:
        if result + increaseVal >= limit[0] and result + increaseVal <= limit[1]:
            return True
        else:
            return False
    elif result.__class__.__name__ == 'str':
        if increaseVal in limit:
            return True
        else:
            return False

#The next are specific function that update specific variables after performing a check
def updateMonthlyFee(session, id, increaseVal):
    check = _checkValue(session, "accountNumber", id, CheckingAccount, "monthlyFee", increaseVal, CheckingAccount.MONTHLY_FEE_LIMITS)
    if check:
        return _updateString(session, "accountNumber", id, CheckingAccount, "monthlyFee", increaseVal)
    else:
        return check

def updateInterestRate(session, id, increaseVal):
    check = _checkValue(session, "accountNumber", id, CheckingAccount, "interestRate", increaseVal, CheckingAccount.INTEREST_RATE_LIMITS)
    if check:
        return _updateString(session, "accountNumber", id, CheckingAccount, "interestRate", increaseVal)
    else:
        return check

def updateBalance(session, id, increaseVal):
    check = _checkValue(session, "accountNumber", id, CheckingAccount, "balance", increaseVal, CheckingAccount.BALANCE_LIMITS)
    if check:
        return _updateString(session, "accountNumber", id, CheckingAccount, "balance", increaseVal)
    else:
        return check

def updateDebitCard(session, id, newStatus):
    check = _checkValue(session, "accountNumber", id, CheckingAccount, "balance", newStatus, CheckingAccount.DEBIT_STATUSES)
    if check:
        return _updateString(session, "accountNumber", id, CheckingAccount, "balance", newStatus)
    else:
        return check

