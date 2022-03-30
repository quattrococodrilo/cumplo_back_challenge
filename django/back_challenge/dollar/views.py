from datetime import datetime

from back_chanllenge.settings import BANXICO_DOLLAR_SERIES
from django.views.generic import TemplateView
from utils.helpers import get_banxico_data

from .forms import DollarForm


class DollarIndexView(TemplateView):

    template_name = 'dollar/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        today = datetime.today().strftime('%Y-%m-%d')

        udis_today = get_banxico_data(
            serie=BANXICO_DOLLAR_SERIES,
            start_date=today
        )

        context['dollar_today'] = udis_today[0]['dato']

        params = self.request.GET.dict()

        if 'start_date' in params or 'end_date' in params:
            form = DollarForm(params)

            context['form'] = form

            if form.is_valid():
                dataCleaned = list(form.cleaned_data.values())

                dollar = get_banxico_data(
                    serie=BANXICO_DOLLAR_SERIES,
                    start_date=dataCleaned[0].strftime('%Y-%m-%d'),
                    end_date=(dataCleaned[1].strftime('%Y-%m-%d')
                              if dataCleaned[1] else ''),
                )

                context['dollar_dates'] = [i['fecha'] for i in dollar]
                context['dollar_values'] = [i['dato'] for i in dollar]

                context['average'] = sum([i['dato'] for i in dollar]) / len(dollar)

                context['max'] = max(dollar, key=lambda i: i['dato'])

                context['min'] = min(dollar, key=lambda i: i['dato'])

        else:
            context['form'] = DollarForm()
        return context
