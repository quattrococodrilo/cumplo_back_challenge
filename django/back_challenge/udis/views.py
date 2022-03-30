from datetime import datetime

from back_chanllenge.settings import BANXICO_UDIS_SERIES
from django.views.generic import TemplateView
from utils.helpers import get_banxico_data

from .forms import UdisForm


class UdisIndexView(TemplateView):

    template_name = 'udis/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.today().strftime('%Y-%m-%d')

        udis_today = get_banxico_data(
            serie=BANXICO_UDIS_SERIES,
            start_date=today
        )

        context['udis_today'] = udis_today[0]['dato']

        params = self.request.GET.dict()

        if 'start_date' in params or 'end_date' in params:
            form = UdisForm(params)

            context['form'] = form

            if form.is_valid():
                dataCleaned = list(form.cleaned_data.values())

                udis = get_banxico_data(
                    serie=BANXICO_UDIS_SERIES,
                    start_date=dataCleaned[0].strftime('%Y-%m-%d'),
                    end_date=(dataCleaned[1].strftime('%Y-%m-%d')
                              if dataCleaned[1] else ''),
                )

                context['udis_dates'] = [i['fecha'] for i in udis]
                context['udis_values'] = [i['dato'] for i in udis]

                context['average'] = sum([i['dato'] for i in udis]) / len(udis)

                context['max'] = max(udis, key=lambda i: i['dato'])

                context['min'] = min(udis, key=lambda i: i['dato'])

        else:
            context['form'] = UdisForm()
        return context
