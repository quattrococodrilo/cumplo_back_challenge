import re
from calendar import monthrange

import requests


class BanxicoApi:
    """
    Consulta la API de BANXICO.

    @method create: devuelve una instanta de BanxicoApi. Requiere
        los parametros api_url, token y entry_point
    """

    _base_url: str = ''
    _serie: str = ''
    _errors: list = []
    _token: str = ''
    _entry_point = ''

    def __init__(self, api_url: str, token: str) -> None:

        if not api_url:
            raise Exception('api_url is required.')

        if not token:
            raise Exception('token is required.')

        self._base_url = api_url if api_url[-1] != '/' else api_url[0:-1]

        self._token = token

        if not api_url:
            raise Exception('API URL is required.')

    @staticmethod
    def create(api_url: str, token: str):
        """Devuelve una instancia de BanxicoApi

        Args:
            api_url (str): URL de la API.
            token (str): Token de autorización.

        Returns:
            object: BanxicoApi
        """
        return BanxicoApi(api_url, token)

    def _date_validator(self, date: str) -> bool:
        """Valida que las fechas recibidas sean correctas.

        Args:
            date (str): Fecha en string, debe estar en el formato: YYYY-mm-dd

        Raises:
            Exception: Date format incorrect.
            Exception: The month must be between 1 an 12.
            Exception: The day must be in the range of days of the month.

        Returns:
            bool: True si la fecha es correcta.
        """

        if not bool(re.search(r"^\d{4}-\d{1,2}-\d{1,2}$", date)):
            raise Exception('Date format incorrect, it must be YYYY-mm-dd.')

        [year, month, day] = [int(i) for i in date.split('-')]

        if month > 13 or month < 1:
            raise Exception('The month must be between 1 an 12.')

        number_of_days_in_month: int = monthrange(year, month)[1]

        if day > number_of_days_in_month or day < 1:
            raise Exception(
                f'The day must be in the range of days of the month.'
            )

        return True

    def _url_builder(self, serie: str, start_date: str, end_date: str = '') -> str:
        """ Construye la URL para la consulta.

        Args:
            serie (str): Serie de tópico a consultar.
            start_date (str): Fecha inicial (YYYY-mm-dd)
            end_date (str, optional): Fecha final (YYYY-mm-dd). Default ''.

        Raises:
            Exception: serie parametter is required.
            Exception: start_date parametter is required.

        Returns:
            str: URL para la consulta.
        """

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

    def get(self, serie: str, start_date: str, end_date: str = '') -> list:
        """Realiza la petición a BANXICO.

        Args:
            serie (str): Serie de tópico a consultar.
            start_date (str): Fecha inicial (YYYY-mm-dd)
            end_date (str, optional): Fecha final (YYYY-mm-dd). Default ''.

        Returns:
            list: lista de datos [{fecha: str, dato: float}]
        """
        url = self._url_builder(serie, start_date, end_date)

        respose = requests.get(
            url, headers={
                'Bmx-Token': self._token,
            }
        )

        data = respose.json()

        if 'bmx' in data:
            return [
                {'fecha': i['fecha'], 'dato':float(i['dato'])}
                for i in data['bmx']['series'][0]['datos']
            ]

        return []
