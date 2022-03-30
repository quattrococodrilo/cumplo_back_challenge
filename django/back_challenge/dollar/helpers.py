from utils import BanxicoApi
from back_chanllenge.settings import (BANXICO_API, BANXICO_TOKEN,
                                      BANXICO_DOLLAR_SERIES)


def get_banxico_data(start_date: str, end_date: str = ''):
    """Obtiene los datos de Banxico según la serie de DOLLAR.

    Args:
        start_date (str): Fecha de inicio
        end_date (str, optional): Fecha de término. Default ''.

    Returns:
        list: [{'fecha': string, 'dato': float}]
    """

    api = BanxicoApi.create(
        api_url=BANXICO_API,
        token=BANXICO_TOKEN
    )

    if not end_date:
        return api.get(
            serie=BANXICO_DOLLAR_SERIES,
            start_date=start_date
        )

    return api.get(
        serie=BANXICO_UDIS_SERIES,
        start_date=start_date,
        end_date=end_date
    )