import pdfkit
from django.template.loader import get_template

from pharmacy import settings

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
