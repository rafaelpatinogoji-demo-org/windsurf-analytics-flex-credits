# Flex Credits por Modelo de Lenguaje

Desglosa los **FLEX CREDITS** por modelo de lenguaje cada día.

## 🚀 Uso Rápido

```bash
# Septiembre 2025
python flex_credits_by_model.py --year 2025 --month 9

# Octubre 2025
python flex_credits_by_model.py --year 2025 --month 10

# Con más velocidad (equipos grandes)
python flex_credits_by_model.py --year 2025 --month 9 --workers 50
```

## 📊 Salida

### Archivo CSV generado:
```
TeamFlexCredits/output/flex_credits_by_model_september_2025_2025-10-21.csv
```

### Formato CSV:
```csv
event_date,date_formatted,model,flex_credits
2025-09-01,September 01, 2025,claude-3.5-sonnet,2450.75
2025-09-01,September 01, 2025,gpt-4,1710.00
2025-09-01,September 01, 2025,claude-opus,0.00
2025-09-02,September 02, 2025,claude-3.5-sonnet,2100.50
...
```

### Consola:
```
📊 Processing users: 100%|████████████████████| 5930/5930 [05:23<00:00, 18.3user/s, active=347, data_points=12543]

✅ Complete! Processed 5930 users | Active: 347 | Data points: 12,543

====================================================================================================
FLEX CREDITS BY MODEL - SEPTEMBER 2025
====================================================================================================

📅 2025-09-01 - September 01, 2025
----------------------------------------------------------------------------------------------------
   Claude Sonnet 4.5 Thinking                           2,450.75
   Claude Sonnet 4.5                                    1,710.00
   DAILY TOTAL                                          4,160.75

📅 2025-09-02 - September 02, 2025
----------------------------------------------------------------------------------------------------
   claude-3.5-sonnet                                    2,100.50
   gpt-4                                                1,792.00
   DAILY TOTAL                                          3,892.50

====================================================================================================
TOTALS BY MODEL
====================================================================================================
claude-3.5-sonnet                                      75,234.50  ( 60.0%)
gpt-4                                                  45,890.25  ( 36.6%)
claude-opus                                             4,325.25  (  3.4%)
----------------------------------------------------------------------------------------------------
GRAND TOTAL                                           125,450.00  (100.0%)
====================================================================================================

📊 Statistics:
   - Days with data: 30
   - Total models used: 3
   - Total flex credits: 125,450.00
   - Avg flex credits/day: 4,181.67

⚠️  Days with flex credits: 25
```

## 💡 ¿Qué Muestra?

Para cada día:
- ✅ **Solo FLEX CREDITS** (no prompt credits normales)
- ✅ Desglosado por **modelo de lenguaje** (claude-3.5-sonnet, gpt-4, etc.)
- ✅ Ordenado por **uso descendente** (mayor a menor)
- ✅ **Totales** por modelo y por día

## 🎯 Casos de Uso

### 1. Identificar qué modelo consume más flex credits
```
claude-3.5-sonnet: 75,234.50 (60%) ← Modelo más costoso
gpt-4: 45,890.25 (36.6%)
```

### 2. Ver tendencias diarias
```
2025-09-01: 4,160.75 flex credits
2025-09-02: 3,892.50 flex credits
→ Reducción de uso
```

### 3. Analizar días específicos con alto uso
```
📅 2025-09-15 - DAILY TOTAL: 12,543.00 ← Pico de uso
```

## ⚡ Performance

Mismo procesamiento paralelo que el script principal:
- **Default: 20 workers**
- Equipos grandes (5000+ usuarios): usar `--workers 50`
- Tiempo estimado: 5-15 minutos para 5,930 usuarios

## 🔧 Diferencia con el Script Principal

| Script | Salida |
|--------|--------|
| `team_daily_flex_credits.py` | **Total por día** (todos los modelos sumados) |
| `flex_credits_by_model.py` | **Desglose por modelo cada día** |

## 📈 Ejemplos de Análisis

### ¿Qué modelo debería optimizar primero?
```bash
python flex_credits_by_model.py --year 2025 --month 9
# Mira el "TOTALS BY MODEL" → optimiza el modelo con mayor %
```

### ¿Cuándo empezamos a usar flex credits?
```bash
python flex_credits_by_model.py --year 2025 --month 9
# Busca el primer día con flex credits > 0
```

### Comparar dos meses
```bash
python flex_credits_by_model.py --year 2025 --month 9
python flex_credits_by_model.py --year 2025 --month 10
# Compara los CSVs para ver cambios en uso por modelo
```

---

**¡Listo para analizar! 🎯**
