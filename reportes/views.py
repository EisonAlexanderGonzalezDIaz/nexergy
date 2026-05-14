"""reportes/views.py — Genera y sirve el PDF con ReportLab."""
import io
import datetime
from django.http import FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from calculadora.services import obtener_resumen_entidad


@login_required
def generar_pdf(request):
    """Genera un PDF de huella de carbono para la entidad del usuario."""
    try:
        entidad = request.user.perfil.entidad
    except Exception:
        return HttpResponse('Sin entidad asignada.', status=400)

    año = int(request.GET.get('año', datetime.date.today().year))
    resumen = obtener_resumen_entidad(entidad.id, año)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                            rightMargin=inch, leftMargin=inch,
                            topMargin=inch, bottomMargin=inch)
    styles = getSampleStyleSheet()
    verde  = colors.HexColor('#1A6B3C')

    titulo_style = ParagraphStyle('Titulo', parent=styles['Title'],
                                  textColor=verde, fontSize=20)
    sub_style    = ParagraphStyle('Sub', parent=styles['Heading2'],
                                  textColor=verde, fontSize=13)

    story = []

    # Encabezado
    story.append(Paragraph('NEXERGY', titulo_style))
    story.append(Paragraph('Reporte de Huella de Carbono', styles['Heading2']))
    story.append(Spacer(1, 0.2 * inch))

    # Datos de la entidad
    story.append(Paragraph(f'Entidad: {entidad.nombre}', styles['Normal']))
    story.append(Paragraph(f'Municipio: {entidad.municipio}', styles['Normal']))
    story.append(Paragraph(f'Año: {año}', styles['Normal']))
    story.append(Spacer(1, 0.3 * inch))

    # Tabla de resumen
    story.append(Paragraph('Resumen de Emisiones', sub_style))
    datos_tabla = [
        ['Alcance', 'Descripción', 'Emisiones (tCO₂e)'],
        ['Alcance 1', 'Emisiones directas (combustibles)', f"{resumen.get('alcance_1', 0):.4f}"],
        ['Alcance 2', 'Energía eléctrica',               f"{resumen.get('alcance_2', 0):.4f}"],
        ['Alcance 3', 'Residuos y transporte',           f"{resumen.get('alcance_3', 0):.4f}"],
        ['TOTAL',     '',                                 f"{resumen.get('total', 0):.4f}"],
    ]
    t = Table(datos_tabla, colWidths=[1.2*inch, 3.5*inch, 1.8*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), verde),
        ('TEXTCOLOR',  (0, 0), (-1, 0), colors.white),
        ('FONTNAME',   (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN',      (2, 0), (2, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#E8F5E9')]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#0D3B22')),
        ('TEXTCOLOR',  (0, -1), (-1, -1), colors.white),
        ('FONTNAME',   (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.3 * inch))

    # Pie
    story.append(Paragraph(
        f'Generado el {datetime.date.today().strftime("%d/%m/%Y")} — NEXERGY © 2025',
        styles['Normal']
    ))

    doc.build(story)
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f'nexergy_{entidad.nit}_{año}.pdf'
    )
