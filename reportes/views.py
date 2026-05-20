"""reportes/views.py — Genera y sirve el PDF con ReportLab."""
import io
import datetime
from django.http import FileResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT
from calculadora.services import obtener_resumen_entidad


VERDE        = colors.HexColor('#1A6B3C')
VERDE_OSCURO = colors.HexColor('#0D3B22')
VERDE_CLARO  = colors.HexColor('#E8F5E9')
AZUL         = colors.HexColor('#1565C0')
NARANJA      = colors.HexColor('#E65100')
GRIS         = colors.HexColor('#F5F5F5')
GRIS_TEXTO   = colors.HexColor('#666666')
BLANCO       = colors.white


def header_footer(canvas, doc):
    """Dibuja encabezado y pie en cada página."""
    canvas.saveState()
    w, h = letter

    # Encabezado verde
    canvas.setFillColor(VERDE_OSCURO)
    canvas.rect(0, h - 70, w, 70, fill=True, stroke=False)

    # Logo/texto en encabezado
    canvas.setFillColor(BLANCO)
    canvas.setFont('Helvetica-Bold', 22)
    canvas.drawString(inch, h - 44, 'NEXERGY')
    canvas.setFont('Helvetica', 10)
    canvas.drawString(inch, h - 58, 'Medición y Reducción de Huella de Carbono')

    # Fecha en encabezado derecho
    canvas.setFont('Helvetica', 9)
    canvas.drawRightString(w - inch, h - 44, f'Reporte generado: {datetime.date.today().strftime("%d/%m/%Y")}')
    canvas.drawRightString(w - inch, h - 58, 'Sabana Centro — Cundinamarca, Colombia')

    # Línea decorativa verde claro
    canvas.setStrokeColor(colors.HexColor('#5DCAA5'))
    canvas.setLineWidth(3)
    canvas.line(0, h - 73, w, h - 73)

    # Pie de página
    canvas.setFillColor(VERDE_OSCURO)
    canvas.rect(0, 0, w, 40, fill=True, stroke=False)
    canvas.setFillColor(BLANCO)
    canvas.setFont('Helvetica', 8)
    canvas.drawString(inch, 14, 'NEXERGY © 2026 — Universidad de Cundinamarca — Ingeniería de Sistemas — Comunicación de Datos')
    canvas.drawRightString(w - inch, 14, f'Página {doc.page}')

    canvas.restoreState()


@login_required
def generar_pdf(request):
    try:
        entidad = request.user.perfil.entidad
    except Exception:
        return HttpResponse('Sin entidad asignada.', status=400)

    año = int(request.GET.get('año', datetime.date.today().year))
    resumen = obtener_resumen_entidad(entidad.id, año)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=1.3 * inch,
        bottomMargin=0.8 * inch,
    )

    styles = getSampleStyleSheet()

    # Estilos personalizados
    titulo_style = ParagraphStyle(
        'Titulo', parent=styles['Normal'],
        textColor=VERDE_OSCURO, fontSize=18,
        fontName='Helvetica-Bold', spaceAfter=4,
    )
    subtitulo_style = ParagraphStyle(
        'Subtitulo', parent=styles['Normal'],
        textColor=GRIS_TEXTO, fontSize=11,
        spaceAfter=16,
    )
    seccion_style = ParagraphStyle(
        'Seccion', parent=styles['Normal'],
        textColor=VERDE_OSCURO, fontSize=12,
        fontName='Helvetica-Bold', spaceBefore=16, spaceAfter=8,
    )
    normal_style = ParagraphStyle(
        'Normal2', parent=styles['Normal'],
        fontSize=10, textColor=colors.HexColor('#333333'),
        spaceAfter=4,
    )
    centro_style = ParagraphStyle(
        'Centro', parent=styles['Normal'],
        fontSize=10, alignment=TA_CENTER,
    )
    nota_style = ParagraphStyle(
        'Nota', parent=styles['Normal'],
        fontSize=8, textColor=GRIS_TEXTO,
        spaceAfter=4,
    )

    story = []

    # ── PORTADA / ENCABEZADO ──────────────────────────────
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph('Reporte de Huella de Carbono', titulo_style))
    story.append(Paragraph(f'{entidad.nombre} — Año {año}', subtitulo_style))
    story.append(HRFlowable(width='100%', thickness=2, color=VERDE_CLARO, spaceAfter=14))

    # ── DATOS DE LA ENTIDAD ───────────────────────────────
    story.append(Paragraph('Información de la Entidad', seccion_style))

    datos_entidad = [
        ['Campo', 'Detalle'],
        ['Entidad', entidad.nombre],
        ['Municipio', str(entidad.municipio)],
        ['NIT', str(entidad.nit)],
        ['Tipo', str(entidad.tipo)],
        ['Año del reporte', str(año)],
        ['Fecha de generación', datetime.date.today().strftime('%d de %B de %Y')],
    ]
    t_entidad = Table(datos_entidad, colWidths=[2 * inch, 4.5 * inch])
    t_entidad.setStyle(TableStyle([
        ('BACKGROUND',  (0, 0), (-1, 0), VERDE_OSCURO),
        ('TEXTCOLOR',   (0, 0), (-1, 0), BLANCO),
        ('FONTNAME',    (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0, 0), (-1, 0), 10),
        ('BACKGROUND',  (0, 1), (0, -1), VERDE_CLARO),
        ('FONTNAME',    (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE',    (0, 1), (-1, -1), 10),
        ('TEXTCOLOR',   (0, 1), (0, -1), VERDE_OSCURO),
        ('ROWBACKGROUNDS', (1, 1), (-1, -1), [BLANCO, GRIS]),
        ('GRID',        (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
        ('ROWHEIGHT',   (0, 0), (-1, -1), 20),
        ('TOPPADDING',  (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(t_entidad)
    story.append(Spacer(1, 0.2 * inch))

    # ── RESUMEN DE EMISIONES ──────────────────────────────
    story.append(Paragraph('Resumen de Emisiones (tCO₂e)', seccion_style))

    total = resumen.get('total', 0)
    a1    = resumen.get('alcance_1', 0)
    a2    = resumen.get('alcance_2', 0)
    a3    = resumen.get('alcance_3', 0)

    pct1 = (a1 / total * 100) if total > 0 else 0
    pct2 = (a2 / total * 100) if total > 0 else 0
    pct3 = (a3 / total * 100) if total > 0 else 0

    datos_resumen = [
        ['Alcance', 'Descripción', 'Emisiones (tCO₂e)', '% del Total'],
        ['Alcance 1', 'Emisiones directas — Combustibles',    f'{a1:.4f}', f'{pct1:.1f}%'],
        ['Alcance 2', 'Emisiones indirectas — Electricidad',  f'{a2:.4f}', f'{pct2:.1f}%'],
        ['Alcance 3', 'Otras emisiones — Residuos',           f'{a3:.4f}', f'{pct3:.1f}%'],
        ['TOTAL',     'Huella de carbono total',               f'{total:.4f}', '100%'],
    ]
    t_resumen = Table(datos_resumen, colWidths=[1.1*inch, 3*inch, 1.5*inch, 1*inch])
    t_resumen.setStyle(TableStyle([
        ('BACKGROUND',     (0, 0), (-1, 0), VERDE_OSCURO),
        ('TEXTCOLOR',      (0, 0), (-1, 0), BLANCO),
        ('FONTNAME',       (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',       (0, 0), (-1, 0), 10),
        ('ALIGN',          (2, 0), (-1, -1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [BLANCO, GRIS]),
        ('BACKGROUND',     (0, -1), (-1, -1), VERDE_OSCURO),
        ('TEXTCOLOR',      (0, -1), (-1, -1), BLANCO),
        ('FONTNAME',       (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('GRID',           (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
        ('ROWHEIGHT',      (0, 0), (-1, -1), 22),
        ('TOPPADDING',     (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING',  (0, 0), (-1, -1), 6),
        ('LEFTPADDING',    (0, 0), (-1, -1), 10),
    ]))
    story.append(t_resumen)
    story.append(Spacer(1, 0.2 * inch))

    # ── TOP FUENTES ───────────────────────────────────────
    if resumen.get('por_categoria'):
        story.append(Paragraph('Top Fuentes de Emisión', seccion_style))
        datos_cat = [['#', 'Categoría de Consumo', 'Emisiones (tCO₂e)']]
        for i, cat in enumerate(resumen['por_categoria'], 1):
            datos_cat.append([
                str(i),
                str(cat['categoria']),
                f"{cat['total']:.4f}",
            ])
        t_cat = Table(datos_cat, colWidths=[0.4*inch, 4.5*inch, 1.7*inch])
        t_cat.setStyle(TableStyle([
            ('BACKGROUND',     (0, 0), (-1, 0), VERDE),
            ('TEXTCOLOR',      (0, 0), (-1, 0), BLANCO),
            ('FONTNAME',       (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE',       (0, 0), (-1, 0), 10),
            ('ALIGN',          (2, 0), (2, -1), 'RIGHT'),
            ('ALIGN',          (0, 0), (0, -1), 'CENTER'),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANCO, GRIS]),
            ('GRID',           (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
            ('ROWHEIGHT',      (0, 0), (-1, -1), 20),
            ('TOPPADDING',     (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING',  (0, 0), (-1, -1), 5),
            ('LEFTPADDING',    (0, 0), (-1, -1), 10),
        ]))
        story.append(t_cat)
        story.append(Spacer(1, 0.2 * inch))

    # ── ODS ───────────────────────────────────────────────
    story.append(HRFlowable(width='100%', thickness=1, color=VERDE_CLARO, spaceAfter=10))
    story.append(Paragraph('Alineación con Objetivos de Desarrollo Sostenible', seccion_style))
    datos_ods = [
        ['ODS', 'Objetivo', 'Relación con NEXERGY'],
        ['ODS 7',  'Energía asequible y no contaminante', 'Recomendaciones de energías renovables'],
        ['ODS 11', 'Ciudades y comunidades sostenibles',  'Gestión ambiental municipal'],
        ['ODS 13', 'Acción por el clima',                 'Medición y reducción de CO₂'],
        ['ODS 17', 'Alianzas para lograr los objetivos',  'Comparativa regional Sabana Centro'],
    ]
    t_ods = Table(datos_ods, colWidths=[0.8*inch, 2.5*inch, 3.3*inch])
    t_ods.setStyle(TableStyle([
        ('BACKGROUND',     (0, 0), (-1, 0), VERDE_OSCURO),
        ('TEXTCOLOR',      (0, 0), (-1, 0), BLANCO),
        ('FONTNAME',       (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',       (0, 0), (-1, 0), 10),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [BLANCO, GRIS]),
        ('GRID',           (0, 0), (-1, -1), 0.5, colors.HexColor('#DDDDDD')),
        ('ROWHEIGHT',      (0, 0), (-1, -1), 20),
        ('TOPPADDING',     (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING',  (0, 0), (-1, -1), 5),
        ('LEFTPADDING',    (0, 0), (-1, -1), 10),
    ]))
    story.append(t_ods)
    story.append(Spacer(1, 0.2 * inch))

    # ── NOTA METODOLÓGICA ─────────────────────────────────
    story.append(HRFlowable(width='100%', thickness=1, color=VERDE_CLARO, spaceAfter=8))
    story.append(Paragraph('Nota Metodológica', seccion_style))
    story.append(Paragraph(
        'Las emisiones de gases de efecto invernadero fueron calculadas siguiendo el estándar '
        'GHG Protocol Corporate Standard, utilizando factores de emisión del IPCC Sexto Informe '
        'de Evaluación (AR6) y la Unidad de Planeación Minero Energética (UPME) de Colombia. '
        'Los resultados se expresan en toneladas de CO₂ equivalente (tCO₂e).',
        nota_style
    ))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(
        f'Reporte generado por NEXERGY — Universidad de Cundinamarca — '
        f'Ingeniería de Sistemas — Comunicación de Datos — 2026',
        nota_style
    ))

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=f'nexergy_{entidad.nit}_{año}.pdf'
    )