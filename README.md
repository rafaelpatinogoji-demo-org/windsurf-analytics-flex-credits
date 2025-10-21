# Team Flex Credits Analytics 📊

Análisis de **flex credits** del equipo con procesamiento paralelo optimizado para organizaciones grandes (miles de usuarios).

## 🎯 ¿Qué hace?

Obtiene y analiza el uso de **flex credits** de todo el equipo desde la API de Windsurf Analytics:
- ✅ Totales diarios de flex credits
- ✅ Desglose por modelo de lenguaje (GPT, Claude, Gemini, etc.)
- ✅ Procesamiento paralelo ultra-rápido (5-15 min para 5,930 usuarios)

---

## 🚀 Setup Rápido

### 1. Instala dependencias

```bash
pip install -r requirements.txt
```

### 2. Configura tu SERVICE_KEY

```bash
# Copia el archivo ejemplo
cp .env.example .env

# Edita .env y agrega tu SERVICE_KEY
# SERVICE_KEY=tu_service_key_aqui
```

### 3. Genera el archivo de mapeo de usuarios

**Importante**: Necesitas un archivo `email_api_mapping_*.json` con los usuarios de tu equipo.

Si ya lo tienes, colócalo en la carpeta `output/` del repositorio padre, o especifícalo con `--json-file`.

### 4. Ejecuta los reportes

#### ✨ Opción 1: Interfaz Interactiva (Recomendado)

```bash
python run_analysis.py
```

La interfaz te guiará paso a paso:
- ✅ Selecciona tipo de análisis (totales diarios, por modelo, o ambos)
- ✅ Escoge mes específico o rango personalizado
- ✅ Configura workers (10, 20, 30, 50)
- ✅ Selecciona archivo de mapeo automáticamente
- ✅ Visualiza resumen antes de ejecutar

#### 📝 Opción 2: Línea de Comandos (Avanzado)

```bash
# Septiembre 2025 - Recomendado: 50 workers para velocidad máxima
python team_daily_flex_credits.py --year 2025 --month 9 --workers 50

# Octubre 2025
python team_daily_flex_credits.py --year 2025 --month 10 --workers 50

# Rango personalizado
python team_daily_flex_credits.py --start-date 2025-09-01 --end-date 2025-09-30 --workers 50
```

**Nota**: Default = 20 workers. Para equipos grandes (5000+), usa `--workers 50` para máxima velocidad.

---

## 📊 Salida

### Archivo CSV generado:
```
TeamFlexCredits/output/team_daily_flex_credits_september_2025_2025-10-21.csv
```

### Formato:
```csv
event_date,date_formatted,total_flex_credits,total_prompt_credits,data_points
2025-09-01,September 01, 2025,4160.75,12543.20,145
2025-09-02,September 02, 2025,3892.50,11234.80,138
```

### Consola:
```
📊 Processing users: 100%|████████████████████| 5930/5930 [05:23<00:00, 18.3user/s, active=347, data_points=12543]

✅ Complete! Processed 5930 users | Active: 347 | Data points: 12,543

====================================================================
Event Date      Date                   Total Flex Credits
--------------------------------------------------------------------
2025-09-01      September 01, 2025           4,160.75
2025-09-02      September 02, 2025           3,892.50
...
--------------------------------------------------------------------
TOTAL                                      125,450.00
====================================================================
```

## 💡 Cómo Funciona

1. **Carga** el archivo `email_api_mapping_*.json` con todos los usuarios del equipo
2. **Consulta** la API de Windsurf en paralelo (50 llamadas simultáneas por defecto)
3. **Agrega** todos los resultados por fecha y/o modelo
4. **Guarda** los CSVs en `output/` (carpeta local)

**¿Por qué paralelo?**
- 5,930 usuarios secuencialmente = 1-2 horas ⏰
- 5,930 usuarios con 50 workers = 2-6 minutos ⚡⚡⚡

## 🔧 Requisitos

- **Python 3.6+**
- **SERVICE_KEY** de Windsurf en el archivo `.env`
- **Archivo de mapeo** `email_api_mapping_*.json` con los usuarios
- **Dependencias**: Ver `requirements.txt` (requests, python-dotenv, tqdm)

## ❌ Solución de Problemas

### No encuentra el archivo de mapeo

**Error**: `❌ No email_api_mapping file found`

**Solución**: Especifica la ruta del archivo manualmente:
```bash
python team_daily_flex_credits.py --year 2025 --month 9 --json-file /path/to/email_api_mapping_2025-10-17.json
```

O coloca el archivo en la carpeta `output/` del repositorio padre.

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

### Muy lento incluso con workers altos

- Verifica tu conexión de red
- Reduce workers si hay errores: `--workers 30`
- La mayoría de usuarios tienen 0 datos y se procesan rápido

### Errores con muchos workers

Si ves errores de timeout o rate limiting:
```bash
# Reduce a 20-30 workers
python team_daily_flex_credits.py --year 2025 --month 9 --workers 25
```

---

## 📋 Scripts Disponibles

### 🌟 `run_analysis.py` - Interfaz Interactiva (Nuevo)
**La forma más fácil de usar el sistema**. Interfaz CLI hermosa que te guía paso a paso.

```bash
python run_analysis.py
```

**Características:**
- 🎨 Interfaz visual colorida e intuitiva
- 📝 Validación de entradas en tiempo real
- 🔄 Ejecuta uno o ambos análisis
- 📅 Selección fácil de fechas (mes o rango)
- ⚡ Configuración de workers con descripciones
- 📁 Detección automática de archivos de mapeo
- ✅ Confirmación antes de ejecutar

📖 Ver guía visual completa → [INTERACTIVE_UI.md](INTERACTIVE_UI.md)

### 1. `team_daily_flex_credits.py`
Totales diarios de flex credits para todo el equipo (uso avanzado/scripting).
```bash
python team_daily_flex_credits.py --year 2025 --month 9 --workers 50
```

### 2. `flex_credits_by_model.py`
Desglose de flex credits por modelo de lenguaje cada día (uso avanzado/scripting).
```bash
python flex_credits_by_model.py --year 2025 --month 9 --workers 50
```
Ver detalles en → [README_BY_MODEL.md](README_BY_MODEL.md)

---

**Listo.** Simple y directo. 🎯
