from setters import _parseUserInput, _setString, _setFloat, _reIssueDateFn
from classes import Customer, Person, Employee, CheckingAccount, SavingsAccount, Base
from distutils.util import strtobool

#Added creation functions
def addPerson(session):
    demoDetails = _parseUserInput("Enter basic demographic details in the following format: \n firstName(String) lastName(String) genderFemale(Boolean) birthDate(Datetime):", 4)
    demoDetails[0] = _setString(demoDetails[0])
    demoDetails[1] = _setString(demoDetails[1])
    demoDetails[2] = _setString(demoDetails[2])
    demoDetails[3] = _reIssueDateFn(demoDetails[3])

    person = Person(firstName=demoDetails[0],
                    lastName=demoDetails[1],
                    genderFemale=bool(strtobool(str(demoDetails[2]))),
                    birthDate=demoDetails[3])
    session.add(person)
    session.commit()
    return person



def addCustomer(session):
    person = addPerson(session)
    customer = Customer(person=person)
    session.add(customer)
    session.commit()



def addEmployee(session):
    person = addPerson(session)
    employeeDetails = _parseUserInput("Enter basic employee details in teh following format: \n role seniority location salary", 4)
    employeeDetails[0] = _setString(employeeDetails[0])
    employeeDetails[1] = _setString(employeeDetails[1])
    employeeDetails[2] = _setString(employeeDetails[2])
    employeeDetails[3] = _setString(employeeDetails[3])

    employee = Employee(role=employeeDetails[0],
                        seniority=employeeDetails[1],
                        location=employeeDetails[2],
                        salary=employeeDetails[3],
                        person=person)
    session.add(employee)
    session.commit()



def addChecking(session):
    checkingDetails = _parseUserInput("Enter basic checking account details in teh following format: \n memberID(Integer) interestRate(Float) monhtlyFee(Float) balance(Float) attachedDebitCard(Boolean) Savings(Boolean)", 6)
    member = session.query(Customer).filter_by(memberID=int(checkingDetails[0])).first()
    checkingDetails[1] = _setFloat(checkingDetails[1])
    checkingDetails[2] = _setFloat(checkingDetails[2])
    checkingDetails[3] = _setFloat(checkingDetails[3])

    checkingAccount = CheckingAccount(acctOpen=True,
                                      interestRate=checkingDetails[1],
                                      monthlyFee=checkingDetails[2],
                                      balance=checkingDetails[3],
                                      attachedDebitCard=bool(strtobool(str(checkingDetails[4]))),
                                      customer=member,
                                      memberID = member.memberID)
    session.add(checkingAccount)
    if strtobool(str(checkingDetails[5])):
        savingsAccount = SavingsAccount(checkingaccount=checkingAccount)
        session.add(savingsAccount)
    session.commit()
