# NEXERGY 🌿
### Medición y Reducción de Huella de Carbono — Sabana Centro
**Proyecto 7.° Semestre · Ingeniería de Sistemas · 2025**

---

## ¿Qué es NEXERGY?
Aplicación web Django + MySQL que permite a alcaldías y entes gubernamentales
de la región Sabana Centro (Cundinamarca, Colombia) medir su huella de carbono
y recibir recomendaciones de energías renovables.

---

## Requisitos previos
- Python 3.10 o superior
- MySQL 8.0 instalado y corriendo localmente
- pip actualizado

---

## Pasos para correr el proyecto (primer arranque)

### 1. Clonar/descomprimir el proyecto
```bash
cd nexergy/
```

### 2. Crear el entorno virtual
```bash
python -m venv venv

# Activar en Windows:
venv\Scripts\activate

# Activar en Mac/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Crear la base de datos en MySQL
Abre MySQL Workbench o la terminal de MySQL y ejecuta:
```sql
CREATE DATABASE nexergy_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 5. Configurar las credenciales
```bash
# Copia el archivo de ejemplo
cp .env.example .env

# Abre .env y cambia estos valores con tus credenciales reales:
# DB_PASSWORD=tu_password_de_mysql
# SECRET_KEY=cualquier-texto-largo-y-aleatorio
```

### 6. Aplicar las migraciones (crear las tablas en MySQL)
```bash
python manage.py migrate
```

### 7. Cargar datos iniciales (11 municipios + factores de emisión)
```bash
python manage.py loaddata fixtures/datos_iniciales.json
```

### 8. Crear el superusuario administrador
```bash
python manage.py createsuperuser
# Te pedirá: usuario, email y contraseña
```

### 9. ¡Correr el servidor!
```bash
python manage.py runserver
```

Abre tu navegador en: **http://localhost:8000**

---

## Estructura del proyecto
```
nexergy/
├── manage.py               ← Comando principal de Django
├── requirements.txt        ← Dependencias Python
├── .env.example            ← Plantilla de configuración
├── fixtures/
│   └── datos_iniciales.json← 11 municipios + factores de emisión
├── nexergy/
│   ├── settings.py         ← Configuración global
│   └── urls.py             ← Router principal
├── accounts/               ← Login y roles de usuario
├── entidades/              ← Municipios y alcaldías
├── consumos/               ← Ingreso de datos de consumo
├── calculadora/
│   └── services.py         ← Motor de cálculo tCO₂e ← AQUÍ ESTÁ LA MAGIA
├── dashboard/              ← KPIs y gráficas Chart.js
├── recomendaciones/
│   └── services.py         ← Motor de recomendaciones de energías verdes
├── reportes/               ← Generación de PDF con ReportLab
├── templates/              ← HTML con Bootstrap 5
└── tests/
    └── test_calculadora.py ← Pruebas unitarias
```

---

## Ejecutar las pruebas unitarias
```bash
python manage.py test tests
```

---

## Stack tecnológico
| Componente       | Tecnología              |
|------------------|-------------------------|
| Framework web    | Django 4.2              |
| Base de datos    | MySQL 8.0               |
| Frontend         | Bootstrap 5 + Chart.js  |
| Reportes         | ReportLab               |
| Conector MySQL   | mysqlclient             |

---

## Usuarios del sistema
| Rol               | Acceso                              |
|-------------------|-------------------------------------|
| Administrador     | Todo + panel Django Admin           |
| Funcionario       | Ingreso de datos, dashboard, PDF    |
| Consultor/Auditor | Solo lectura — comparativa regional |

---

*NEXERGY — Proyecto 7.° Semestre 2025*
