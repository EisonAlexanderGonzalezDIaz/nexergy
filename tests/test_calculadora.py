"""
tests/test_calculadora.py
─────────────────────────────────────────────
Pruebas unitarias para el motor de cálculo.
Ejecutar con: python manage.py test tests
─────────────────────────────────────────────
"""

from decimal import Decimal
from django.test import TestCase
from entidades.models import Municipio, Entidad
from consumos.models import FactorEmision, Consumo
from calculadora.services import calcular_huella, obtener_resumen_entidad


class TestCalculoHuella(TestCase):

    def setUp(self):
        """Crea datos de prueba antes de cada test."""
        self.municipio = Municipio.objects.create(nombre='Chía', departamento='Cundinamarca')
        self.entidad   = Entidad.objects.create(
            nombre='Alcaldía de Chía', municipio=self.municipio,
            tipo='ALCALDIA', nit='900000001'
        )
        self.factor_gasolina = FactorEmision.objects.create(
            categoria='Gasolina', subcategoria='Gasolina corriente',
            valor=Decimal('2.310000'), unidad='litro',
            fuente='IPCC AR6', año_referencia=2021
        )
        self.factor_electrico = FactorEmision.objects.create(
            categoria='Energía eléctrica', subcategoria='Red SIN Colombia',
            valor=Decimal('0.195000'), unidad='kWh',
            fuente='UPME 2023', año_referencia=2023
        )

    def test_calculo_gasolina(self):
        """100 litros de gasolina × 2.31 kgCO2e/l = 0.231 tCO2e"""
        consumo = Consumo.objects.create(
            entidad=self.entidad, factor_emision=self.factor_gasolina,
            alcance=1, año=2024, mes=1, valor=Decimal('100')
        )
        emision = calcular_huella(consumo)
        self.assertAlmostEqual(float(emision.tco2e), 0.231, places=4)

    def test_calculo_electricidad(self):
        """1000 kWh × 0.195 kgCO2e/kWh = 0.195 tCO2e"""
        consumo = Consumo.objects.create(
            entidad=self.entidad, factor_emision=self.factor_electrico,
            alcance=2, año=2024, mes=2, valor=Decimal('1000')
        )
        emision = calcular_huella(consumo)
        self.assertAlmostEqual(float(emision.tco2e), 0.195, places=4)

    def test_valor_cero_produce_emision_cero(self):
        consumo = Consumo.objects.create(
            entidad=self.entidad, factor_emision=self.factor_gasolina,
            alcance=1, año=2024, mes=3, valor=Decimal('0.01')
        )
        emision = calcular_huella(consumo)
        self.assertGreater(emision.tco2e, 0)

    def test_resumen_entidad(self):
        """El resumen debe sumar correctamente los tres alcances."""
        Consumo.objects.create(entidad=self.entidad, factor_emision=self.factor_gasolina,
                               alcance=1, año=2024, mes=1, valor=Decimal('100'))
        Consumo.objects.create(entidad=self.entidad, factor_emision=self.factor_electrico,
                               alcance=2, año=2024, mes=1, valor=Decimal('1000'))
        # Calcular emisiones
        for c in Consumo.objects.filter(entidad=self.entidad):
            calcular_huella(c)

        resumen = obtener_resumen_entidad(self.entidad.id, 2024)
        self.assertAlmostEqual(float(resumen['alcance_1']), 0.231, places=4)
        self.assertAlmostEqual(float(resumen['alcance_2']), 0.195, places=4)
        self.assertAlmostEqual(float(resumen['total']),     0.426, places=4)
