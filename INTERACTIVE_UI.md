# 🎨 Interfaz Interactiva - Guía Visual

## 🚀 Cómo usar `run_analysis.py`

La interfaz interactiva hace que sea súper fácil ejecutar análisis sin recordar comandos complicados.

---

## 📺 Flujo de la Interfaz

### 1. Banner de Bienvenida

```
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║       📊  TEAM FLEX CREDITS ANALYTICS  📊                   ║
    ║                                                              ║
    ║       Análisis de uso de Flex Credits del equipo            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
```

### 2. Selección de Tipo de Análisis

```
? ¿Qué tipo de análisis quieres realizar?
❯ 📅 Totales diarios de flex credits
  🤖 Desglose por modelo de lenguaje
  🔄 Ambos análisis
  ❌ Salir
```

**Opciones:**
- **📅 Totales diarios**: Genera `team_daily_flex_credits_*.csv`
- **🤖 Por modelo**: Genera `flex_credits_by_model_*.csv` 
- **🔄 Ambos**: Genera ambos reportes en una sola ejecución
- **❌ Salir**: Cierra la aplicación

---

### 3. Tipo de Rango de Fechas

```
? ¿Cómo quieres especificar el rango de fechas?
❯ 📆 Mes específico
  📅 Rango personalizado
  ⬅️  Volver
```

**Opciones:**
- **📆 Mes específico**: Selecciona año y mes fácilmente
- **📅 Rango personalizado**: Especifica fechas exactas (YYYY-MM-DD)
- **⬅️ Volver**: Regresa al menú anterior

---

### 4a. Mes Específico - Año

```
? ¿Qué año? 2025
```

**Validación automática**: Solo acepta años entre 2020-2030

---

### 4b. Mes Específico - Mes

```
? ¿Qué mes?
  Enero (1)
  Febrero (2)
  Marzo (3)
  Abril (4)
  Mayo (5)
  Junio (6)
  Julio (7)
  Agosto (8)
❯ Septiembre (9)
  Octubre (10)
  Noviembre (11)
  Diciembre (12)
```

**Auto-calcula**: El sistema calcula automáticamente el primer y último día del mes.

```
✅ Rango seleccionado: 2025-09-01 a 2025-09-30
```

---

### 4c. Rango Personalizado

```
? Fecha inicial (YYYY-MM-DD): 2025-09-01
? Fecha final (YYYY-MM-DD): 2025-09-15

✅ Rango personalizado: 2025-09-01 a 2025-09-15
```

**Validación**: Verifica que las fechas estén en formato correcto.

---

### 5. Configuración de Workers

```
? ¿Cuántos workers paralelos quieres usar?
❯ ⚡⚡⚡ 50 workers (ultra rápido - recomendado)
  ⚡⚡ 30 workers (rápido y estable)
  ⚡ 20 workers (default)
  🐢 10 workers (conservador)
```

**Guía de velocidad** (para 5,930 usuarios):
- **50 workers**: ~2-6 minutos ⚡⚡⚡
- **30 workers**: ~4-8 minutos ⚡⚡
- **20 workers**: ~5-15 minutos ⚡
- **10 workers**: ~10-20 minutos 🐢

---

### 6. Archivo de Mapeo

Si se encuentra automáticamente:
```
✅ Se encontraron 1 archivo(s) de mapeo
? ¿Usar el archivo más reciente? (email_api_mapping_2025-10-17.json) (Y/n)
```

Si no se encuentra:
```
⚠️  No se encontró archivo de mapeo automáticamente
? Especifica la ruta del archivo email_api_mapping_*.json:
```

---

### 7. Resumen y Confirmación

```
======================================================================
📋 RESUMEN DE CONFIGURACIÓN
======================================================================
📊 Análisis: Ambos (totales + por modelo)
📅 Período: 2025-09-01 a 2025-09-30
⚡ Workers: 50
📁 Archivo mapeo: email_api_mapping_2025-10-17.json
======================================================================

? ¿Continuar con el análisis? (Y/n)
```

**Última oportunidad**: Revisa toda la configuración antes de ejecutar.

---

### 8. Ejecución

```
🚀 Iniciando análisis...

======================================================================

📊 Ejecutando: Totales diarios de flex credits

📊 Processing users: 100%|████████████| 5930/5930 [05:23<00:00, 18.3user/s]

✅ Complete! Processed 5930 users | Active: 347 | Data points: 12,543

====================================================================
TEAM FLEX CREDITS - SEPTEMBER 2025
====================================================================
...

======================================================================

🤖 Ejecutando: Desglose por modelo de lenguaje

📊 Processing users: 100%|████████████| 5930/5930 [05:25<00:00, 18.2user/s]

✅ Complete! Processed 5930 users | Active: 347 | Data points: 12,543

====================================================================
FLEX CREDITS BY MODEL - SEPTEMBER 2025
====================================================================
...
```

---

### 9. Completado

```
======================================================================
✅ ¡Análisis completado exitosamente!
======================================================================

📁 Los resultados se guardaron en: /path/to/TeamFlexCredits/output

? ¿Quieres realizar otro análisis? (y/N)
```

**Opciones:**
- **Y**: Vuelve al inicio para otro análisis
- **N**: Sale de la aplicación

---

## 🎨 Características de la UI

### Colores y Estilo
- 🟣 **Púrpura**: Preguntas y opciones resaltadas
- 🔴 **Rojo**: Respuestas seleccionadas
- ⚫ **Gris**: Opciones no seleccionadas
- ✅ **Verde**: Confirmaciones y éxitos
- ⚠️ **Amarillo**: Advertencias
- ❌ **Rojo**: Errores o cancelaciones

### Navegación
- **↑/↓**: Mover entre opciones
- **Enter**: Seleccionar opción
- **Ctrl+C**: Cancelar en cualquier momento
- **⬅️ Volver**: Opción para regresar al menú anterior

### Validaciones
- ✅ Formato de fecha YYYY-MM-DD
- ✅ Año entre 2020-2030
- ✅ Archivo existe y es accesible
- ✅ Valores numéricos válidos

---

## 💡 Ventajas vs Línea de Comandos

| Característica | CLI Interactiva | Línea de Comandos |
|----------------|-----------------|-------------------|
| **Facilidad de uso** | ⭐⭐⭐⭐⭐ Super fácil | ⭐⭐⭐ Requiere recordar flags |
| **Validación** | ✅ En tiempo real | ❌ Errores al ejecutar |
| **Visualización** | ✅ Preview de config | ❌ Sin preview |
| **Descubribilidad** | ✅ Todas las opciones visibles | ❌ Requiere `--help` |
| **Para nuevos usuarios** | ⭐⭐⭐⭐⭐ Perfecto | ⭐⭐ Intimidante |
| **Para scripting** | ⭐⭐ No automatizable | ⭐⭐⭐⭐⭐ Perfecto |

---

## 🚀 Casos de Uso

### Caso 1: Usuario Nuevo
**Situación**: Primera vez usando el sistema

```bash
python run_analysis.py
```

→ La interfaz te guía paso a paso
→ No necesitas leer documentación extensa
→ Todas las opciones están explicadas

### Caso 2: Análisis Rápido
**Situación**: Necesitas un reporte rápido del mes actual

```bash
python run_analysis.py
```

→ Selecciona "Mes específico"
→ Usa año y mes actual (pre-llenados)
→ Usa 50 workers
→ Listo en 2-3 minutos

### Caso 3: Comparar Múltiples Meses
**Situación**: Quieres ver Septiembre y Octubre

```bash
python run_analysis.py
```

1. Ejecuta para Septiembre
2. Al final, selecciona "Sí" para otro análisis
3. Ejecuta para Octubre
4. Compara los CSVs

### Caso 4: Análisis Detallado
**Situación**: Quieres ver totales Y desglose por modelo

```bash
python run_analysis.py
```

→ Selecciona "🔄 Ambos análisis"
→ Genera ambos reportes en una ejecución
→ Ahorra tiempo

---

## 🐛 Manejo de Errores

La interfaz maneja errores gracefully:

### Error: Archivo no encontrado
```
⚠️  No se encontró archivo de mapeo automáticamente
? Especifica la ruta del archivo email_api_mapping_*.json:
```

### Error: Fecha inválida
```
? Fecha inicial (YYYY-MM-DD): 2025-13-45
❌ Formato inválido. Usa YYYY-MM-DD (ejemplo: 2025-09-01)
```

### Error durante ejecución
```
❌ Error al ejecutar el análisis de totales diarios
```
→ Muestra el error y termina limpiamente

### Cancelación por usuario
```
^C
❌ Análisis interrumpido por el usuario
```

---

## 🎯 Tips y Trucos

### Tip 1: Usa 50 Workers por Default
Para equipos grandes (5000+ usuarios), siempre usa 50 workers para máxima velocidad.

### Tip 2: Ejecuta Ambos Análisis
Seleccionar "🔄 Ambos análisis" es más eficiente que ejecutar dos veces.

### Tip 3: Mantén Archivos de Mapeo Actualizados
El sistema detecta automáticamente el archivo más reciente. Mantén uno actualizado en `output/`.

### Tip 4: Usa Rangos Personalizados para Semanas
Para análisis semanales, usa "Rango personalizado" con lunes a domingo.

### Tip 5: Confirma Antes de Ejecutar
Siempre revisa el resumen de configuración antes de confirmar.

---

**¡Disfruta de la nueva interfaz! 🎉**
