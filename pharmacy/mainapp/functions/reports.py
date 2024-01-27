import pdfkit
from django.template.loader import get_template

from pharmacy import settings


# def get_report(dic):
#     template = ''
#     rep_resp = {}
#
#     if dic['report'] == 0:
#         template = 'reports/report0.html'
#         rep_resp = {
#             'dn': dic['dn'],
#             'de': dic['de'],
#         }
#         # couple__horse = h.id, couple__result=1,
#         resp = []
#         horses = Horse.objects.all()
#         for h in horses:
#             resp.append({
#                 'name': h.name,
#                 'owner': h.owner.__str__(),
#                 'count_all': Race.objects.filter(couple__horse=h.id, date__gte=dic['dn'], date__lte=dic['de']).count(),
#                 'one': Race.objects.filter(couple__horse=h.id, couple__result=1, date__gte=dic['dn'],
#                                            date__lte=dic['de']).count(),
#                 'two': Race.objects.filter(couple__horse=h.id, couple__result=2, date__gte=dic['dn'],
#                                            date__lte=dic['de']).count(),
#                 'tree': Race.objects.filter(couple__horse=h.id, couple__result=3, date__gte=dic['dn'],
#                                             date__lte=dic['de']).count(),
#             })
#         resp.sort(key=lambda item: (item['one'], item['two'], item['tree']), reverse=True)
#         for i in range(len(resp)):
#             resp[i]['num'] = i + 1
#
#         rep_resp['table'] = resp
#
#     if dic['report'] == 1:
#         template = 'reports/report1.html'
#         rep_resp = {
#             'dn': dic['dn'],
#             'de': dic['de'],
#         }
#         resp = []
#         jockeys = Jockey.objects.all()
#         for j in jockeys:
#             resp.append({
#                 'fio': j.__str__(),
#                 'category': j.category,
#                 'count_all': Couple.objects.filter(jockey=j.id, race__date__gte=dic['dn'],
#                                                    race__date__lte=dic['de']).count(),
#                 'one': Couple.objects.filter(jockey=j.id, result=1, race__date__gte=dic['dn'],
#                                              race__date__lte=dic['de']).count(),
#                 'two': Couple.objects.filter(jockey=j.id, result=2, race__date__gte=dic['dn'],
#                                              race__date__lte=dic['de']).count(),
#                 'tree': Couple.objects.filter(jockey=j.id, result=3, race__date__gte=dic['dn'],
#                                               race__date__lte=dic['de']).count(),
#             })
#         resp.sort(key=lambda item: (item['one'], item['two'], item['tree']))
#         for i in range(len(resp)):
#             resp[i]['num'] = i
#
#         rep_resp['table'] = resp
#
#     if dic['report'] == 2 and dic['jockey'] != '':
#         dic['jockey'] = dic['jockey'][0]
#         template = 'reports/report2.html'
#         rep_resp = {
#             'fio': dic['jockey'].__str__(),
#             'city': dic['jockey'].user.city.__str__(),
#             'category': dic['jockey'].category,
#
#             'dn': dic['dn'],
#             'de': dic['de'],
#         }
#         resp = []
#         couples = Couple.objects.filter(race__date__gte=dic['dn'], race__date__lte=dic['de'], jockey=dic['jockey'].id)
#         for c in couples:
#             resp.append({
#                 'date': c.race.date,
#                 'race': c.race.__str__(),
#                 'horse': c.horse.__str__(),
#                 'distance': c.race.distance,
#                 'result': c.result,
#             })
#         resp.sort(key=lambda item: (item['date']))
#         rep_resp['table'] = resp
#
#     if dic['report'] == 3 and dic['horse'] != '':
#         dic['horse'] = dic['horse'][0]
#         template = 'reports/report3.html'
#         rep_resp = {
#             'name': dic['horse'].name,
#             'mast': dic['horse'].mast,
#             'owner': dic['horse'].owner.__str__(),
#             'age': dic['horse'].age,
#
#             'dn': dic['dn'],
#             'de': dic['de'],
#         }
#         resp = []
#         couples = Couple.objects.filter(race__date__gte=dic['dn'], race__date__lte=dic['de'], horse=dic['horse'].id)
#         for c in couples:
#             resp.append({
#                 'date': c.race.date,
#                 'race': c.race.__str__(),
#                 'jockey': c.jockey.__str__(),
#                 'distance': c.race.distance,
#                 'result': c.result,
#             })
#         resp.sort(key=lambda item: (item['date']))
#         rep_resp['table'] = resp
#
#     if dic['report'] == 4:
#         template = 'reports/report4.html'
#         rep_resp = {
#             'dn': dic['dn'],
#             'de': dic['de'],
#         }
#         resp = []
#         races = Race.objects.filter(date__gte=dic['dn'], date__lte=dic['de'])
#         for r in races:
#             resp.append({
#                 'date': r.date,
#                 'race': r.__str__(),
#                 'count': Couple.objects.filter(race=r.id).count(),
#                 'summa': r.summa,
#                 'horse': Horse.objects.filter(couple__race__id=r.id, couple__result=1)[0].__str__() if
#                 Horse.objects.filter(couple__race__id=r.id, couple__result=1).exists() else '',
#                 'jockey': Jockey.objects.filter(couple__race__id=r.id, couple__result=1)[0].__str__() if
#                 Jockey.objects.filter(couple__race__id=r.id, couple__result=1).exists() else '',
#             })
#         resp.sort(key=lambda item: (item['date']))
#         rep_resp['table'] = resp
#
#     if dic['report'] == 5 and dic['race'] != '':
#         dic['race'] = dic['race'][0]
#         template = 'reports/report5.html'
#         rep_resp = {
#             'title': dic['race'].__str__(),
#             'org': dic['race'].org,
#             'date': dic['race'].date,
#             'time_begin': dic['race'].time_begin,
#             'time_end': dic['race'].time_end,
#             'distance': dic['race'].distance,
#             'summa': dic['race'].summa,
#         }
#         resp = []
#         couples = Couple.objects.filter(race=dic['race'].id)
#         for c in couples:
#             resp.append({
#                 'horse': c.horse.__str__(),
#                 'jockey': c.jockey.__str__(),
#                 'result': c.result,
#                 'time': c.time,
#             })
#         resp.sort(key=lambda item: (item['result']))
#         rep_resp['table'] = resp
#
#     return template, rep_resp
#

def render_pdf(url_template, contexto):
    template = get_template(url_template)
    html = template.render(contexto)

    return pdfkit.from_string(
        html,
        False,
        options={'encoding': "utf-8", },
        configuration=pdfkit.configuration(wkhtmltopdf=settings.WKHTMLTOPDF_PATH),
        css=settings.STATIC_ROOT + "/../mainapp/static/reports/css/reports.css"
    )
