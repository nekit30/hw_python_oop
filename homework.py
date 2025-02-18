import datetime as dt

DATE_FORMAT = '%d.%m.%Y'


class Record:
    '''Класс записей пользователя.'''
    def __init__(
        self,
        amount: float,
        comment: str,
        date: dt.date = None
    ) -> None:
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:
    '''Базовый класс калькулятора.'''
    def __init__(self, limit) -> None:
        self.limit = limit
        self.records = []

    def get_today_date(self) -> dt.date:
        """Получить текущую дату."""
        return dt.date.today()

    def get_week_date(self) -> dt.date:
        """Получить дату неделю назад."""
        return self.get_today_date() - dt.timedelta(days=7)

    def add_record(self, record) -> None:
        """Добавить новую запись."""
        return self.records.append(record)

    def get_today_stats(self) -> float:
        """Получить сумму расходов за сегодня."""
        today = self.get_today_date()
        t_amount = [record.amount for record in self.records
                    if record.date == today]
        return sum(t_amount)

    def get_week_stats(self) -> float:
        """Получить сумму расходов за неделю."""
        today = self.get_today_date()
        week_ago = self.get_week_date()
        week_amount = [record.amount for record in self.records
                       if today >= record.date > week_ago]
        return sum(week_amount)

    def get_today_limit(self) -> float:
        """Получить допустимую сумму расходов за сегодня."""
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    '''Класс калькулятора денег.'''
    USD_RATE = 73.20
    EURO_RATE = 86.64

    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def get_today_cash_remained(self, currency: str) -> str:
        """Вернуть информационное сообщение о  финансовых расходах."""
        self.currency = currency
        t_amount = self.get_today_limit()
        currencies = {'rub': ('руб', 1),
                      'usd': ('USD', CashCalculator.USD_RATE),
                      'eur': ('Euro', CashCalculator.EURO_RATE)}
        if self.currency not in currencies:
            return 'Указана неверная валюта. Повторите ввод.'
        c_type, c_rate = currencies[currency]

        if t_amount == 0:
            return 'Денег нет, держись'
        if t_amount > 0:
            return (f'На сегодня осталось '
                    f'{abs(round((t_amount / c_rate), 2))} {c_type}')
        return (f'Денег нет, держись: твой долг - '
                f'{abs(round((t_amount / c_rate), 2))} {c_type}')


class CaloriesCalculator(Calculator):
    '''Класс калькулятора калорий.'''
    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def get_calories_remained(self) -> str:
        """Вернуть информационное сообщение о расходах калорий."""
        positive_message = ('Сегодня можно съесть что-нибудь ещё, '
                            'но с общей калорийностью не более')
        t_amount = self.get_today_limit()

        if t_amount > 0:
            return (f'{positive_message} {t_amount} кКал')
        return 'Хватит есть!'
