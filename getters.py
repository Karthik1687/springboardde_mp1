from classes import CheckingAccount

def _getCheckingAccount(session, id):
    result = session.query(CheckingAccount).filter(getattr(CheckingAccount, "accountNumber").__eq__(id)).count()
    if result == 1:
        return True
    else:
        return False