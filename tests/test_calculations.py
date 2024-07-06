import pytest
from app.calculations import add, BankAccount, InsufficientFunds

# с помощью fixture мы сокращаем повторение кода, оно передается в тесты как аргументы, и исполняется перед основным кодом (аналогично Depends в FastApi)
@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

# с помощью mark.parametrize мы можем пройтись тестом несколько раз с разными входными данными
@pytest.mark.parametrize('num1, num2, result', [
    (3,5,8),
    (9,7,16),
    (1,19,20),
    ('a','b','ab')
])
def test_add(num1, num2, result):
    print('testing add function')
    assert add(num1, num2,) == result

# bank_account это fixture
def test_deposit(bank_account):
    bank_account.deposit(30)
    assert bank_account.balance == 80 # если указать больше одного assert в одном тесте то чтобы тест был успешно пройден ВСЕ assert должны быть True
    assert 1 == 1

def test_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()
    # это не будет ровно, потому что в первом значении после многих нулей будет 1
    # assert bank_account.balance == 55
    assert round(bank_account.balance, 6) == 55

# с помощью mark.parametrize мы можем пройтись тестом несколько раз с разными входными данными
@pytest.mark.parametrize('num1, num2, result', [
    (100,60,40),
    (9,7,2),
    (110,9,101)
])
def test_bank_transaction(zero_bank_account, num1, num2, result):
    zero_bank_account.deposit(num1)
    zero_bank_account.withdraw(num2)
    assert zero_bank_account.balance == result

def test_incufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)