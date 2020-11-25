from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Person(Base):
    __tablename__ = "Person"
    person_id = Column(Integer, primary_key = True)
    firstName = Column(String)
    lastName = Column(String)
    genderFemale = Column(Boolean)
    birthDate = Column(DateTime)


class Customer(Base):
    __tablename__ = "Customer"
    memberID = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.person_id))

    person = relationship(Person,
                          backref = "Customer")

    def __repr__(self):
        return "Customer(memberID = " + str(self.memberID) + ", person_id = " + str(self.person_id) + ")"

#USE DEFAULT ARGUEMENT IN COLUMN

class Employee(Base):
    ROLES = ['TELLER','MANAGER']
    SENIORITY_LIMITS = [1, 25]
    LOCATIONS = ['SF','NYC','LA']
    SALARY_LIMITS = [25000, 100000]

    __tablename__ = "Employee"
    employeeID = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.person_id))
    role = Column(String)
    seniority = Column(Integer)
    location = Column(String)
    salary = Column(Integer)

    def __repr__(self):
        return "Employee(employeeID = " + str(self.employeeID) + ", person_id = " + str(self.person_id) + ", role = " + self.role + ", seniority = " + str(self.seniority) + ", location = " + self.location + ", salary = " + str(self.salary) + ")"


class CheckingAccount(Base):
    INTEREST_RATE_LIMITS = [0.01, 1.0]
    MONTHLY_FEE_LIMITS = [0, 15]
    BALANCE_LIMITS = [0, 999999]
    DEBIT_STATUSES = [True, False]

    __tablename__ = 'CheckingAccount'
    accountNumber = Column(Integer, primary_key=True)
    memberID = Column(Integer, ForeignKey(Customer.memberID))
    acctOpen = Column(Boolean, default=True)
    interestRate = Column(Float, default=0.01)
    monthlyFee = Column(Float, default=12.99)
    balance = Column(Float, default=0)
    attachedDebitCard = Column(Boolean)

    customer = relationship(Customer, backref="CheckingAccount")

    def __repr__(self):
        return "CheckingAccount(accountNumber =" + str(self.accountNumber) + ", memberID = " + str(self.memberID) + ", accotOpen = " + str(self.acctOpen) + ", interestRate = " + str(self.interestRate) + ", monthlyFee = " + str(self.monthlyFee) +\
                ", balance = " + str(self.balance) + ", attachedDebitCard = " + str(self.attachedDebitCard) + ")"

class SavingsAccount(Base):
    __tablename__ = "SavingsAccount"
    MAX_WIDTHDRAWALS_PER_MONTH = 6

    savingsAccountID = Column(Integer, primary_key=True)
    accountNumber = Column(Integer, ForeignKey(CheckingAccount.accountNumber))
    withdrawalsThisMonth = Column(Integer, default = 0)

    checkingaccount = relationship(CheckingAccount,
                                   backref = "SavingsAccount")

    def __repr__(self):
        return "SavingsAccount(savingsAccountID = " + str(self.savingsAccountID) + ", accountNumber = " + str(self.accountNumber) + ", withdrawalsThisMonth = " + str(self.withdrawalsThisMonth) + ")"