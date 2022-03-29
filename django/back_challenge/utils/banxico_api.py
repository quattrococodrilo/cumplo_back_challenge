import re
from calendar import monthrange

import requests


class BanxicoApi:

    _base_url: str = ''
    _serie: str = ''
    _errors: list = []
    _token: str = ''
    _entry_point = ''

    def __init__(self, api_url: str, token: str, entry_point: str) -> None:

        if not api_url:
            raise Exception('api_url is required.')

        if not token:
            raise Exception('token is required.')

        if not token:
            raise Exception('entry_point is required.')

        self._base_url = api_url if api_url[-1] != '/' else api_url[0:-1]

        self._token = token

        self._entry_point = entry_point

        if not api_url:
            raise Exception('API URL is required.')

    @staticmethod
    def create(api_url: str, token: str, entry_point: str) -> object:
        return BanxicoApi(api_url, token, entry_point)

    def _date_validator(self, date: str) -> bool:

        if not bool(re.search(r"^\d{4}-\d{1,2}-\d{1,2}$", date)):
            raise Exception('El formato de la fecha no coincide.')

        [year, month, day] = [int(i) for i in date.split('-')]

        if year < 1995:
            raise Exception('El año debe ser mayor o igual a 1995.')

        if month > 13 or month < 1:
            raise Exception('El año no puede ser mayor a 13 o menor de 1')

        number_of_days_in_month: int = monthrange(year, month)[1]

        if day > number_of_days_in_month or day < 1:
            raise Exception(
                f'El día no puede ser mayor a {number_of_days_in_month} o menor de 1'
            )

        return True

    def _url_builder(self, serie: str, start_date: str, end_date: str = '') -> str:

        if not serie:
            raise Exception('serie parametter is required.')

        if not start_date:
            raise Exception('start_date parametter is required.')

        url = f'{self._base_url}/{serie.replace("/", "")}/datos'

        if start_date and self._date_validator(start_date):
            url += f"/{start_date}"

        if end_date and self._date_validator(end_date):
            url += f"/{end_date}"

        if start_date and not end_date:
            url += f"/{start_date}"

        return url

    def get(self, serie: str, start_date: str, end_date: str = ''):
        url = self._url_builder(serie, start_date, end_date)

        respose = requests.get(
            url, headers={
                'Bmx-Token': self._token,
            }
        )

        data = respose.json()

        if 'bmx' in data:
            return data['bmx']['series'][0]['datos']

        return []
