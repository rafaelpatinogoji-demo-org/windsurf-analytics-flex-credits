#!/usr/bin/env python3
"""
Team Flex Credits - Interactive CLI
Beautiful interactive interface for running flex credits analysis
"""

import os
import sys
import subprocess
from datetime import datetime, timedelta
import questionary
from questionary import Style

# Custom style for the CLI
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),       # Question mark (purple)
    ('question', 'bold'),                # Question text
    ('answer', 'fg:#f44336 bold'),       # Selected answer (red)
    ('pointer', 'fg:#673ab7 bold'),      # Pointer (purple)
    ('highlighted', 'fg:#673ab7 bold'),  # Highlighted choice (purple)
    ('selected', 'fg:#cc5454'),          # Selected choice (red)
    ('separator', 'fg:#cc5454'),         # Separator
    ('instruction', ''),                 # Instructions
    ('text', ''),                        # Text
    ('disabled', 'fg:#858585 italic')    # Disabled
])


def print_banner():
    """Print welcome banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║       📊  TEAM FLEX CREDITS ANALYTICS  📊                   ║
    ║                                                              ║
    ║       Análisis de uso de Flex Credits del equipo            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def get_month_dates(year, month):
    """Calculate start and end dates for a month"""
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def validate_date(date_str):
    """Validate date format YYYY-MM-DD"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return "❌ Formato inválido. Usa YYYY-MM-DD (ejemplo: 2025-09-01)"


def find_email_mapping_files():
    """Find available email mapping files"""
    import glob
    
    # Check parent output directory
    parent_output = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'output')
    pattern = os.path.join(parent_output, 'email_api_mapping_*.json')
    files = glob.glob(pattern)
    
    # Also check local output directory
    local_output = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
    local_pattern = os.path.join(local_output, 'email_api_mapping_*.json')
    files.extend(glob.glob(local_pattern))
    
    return sorted(set(files))


def main():
    """Main interactive CLI"""
    
    print_banner()
    
    # Step 1: Choose analysis type
    analysis_type = questionary.select(
        "¿Qué tipo de análisis quieres realizar?",
        choices=[
            questionary.Choice("📅 Totales diarios de flex credits", value="daily"),
            questionary.Choice("🤖 Desglose por modelo de lenguaje", value="by_model"),
            questionary.Choice("📆 Resumen mensual (rango de meses)", value="monthly"),
            questionary.Choice("🔄 Ambos análisis (diarios + modelo)", value="both"),
            questionary.Choice("❌ Salir", value="exit")
        ],
        style=custom_style
    ).ask()
    
    if analysis_type == "exit" or analysis_type is None:
        print("\n👋 ¡Hasta luego!\n")
        return
    
    # Step 2: Choose date range type
    if analysis_type == "monthly":
        date_range_type = "month_range"
    else:
        date_range_type = questionary.select(
            "¿Cómo quieres especificar el rango de fechas?",
            choices=[
                questionary.Choice("📆 Mes específico", value="month"),
                questionary.Choice("📅 Rango personalizado", value="custom"),
                questionary.Choice("⬅️  Volver", value="back")
            ],
            style=custom_style
        ).ask()
    
    if date_range_type == "back" or date_range_type is None:
        return main()
    
    # Step 3: Get date parameters
    if date_range_type == "month_range":
        # Choose year
        current_year = datetime.now().year
        year = questionary.text(
            "¿Qué año?",
            default=str(current_year),
            validate=lambda x: x.isdigit() and 2020 <= int(x) <= 2030 or "❌ Año inválido (2020-2030)"
        ).ask()
        
        if year is None:
            return main()
        
        year = int(year)
        
        # Choose start month
        months = [
            "Enero (1)", "Febrero (2)", "Marzo (3)", "Abril (4)",
            "Mayo (5)", "Junio (6)", "Julio (7)", "Agosto (8)",
            "Septiembre (9)", "Octubre (10)", "Noviembre (11)", "Diciembre (12)"
        ]
        
        start_month_choice = questionary.select(
            "¿Mes inicial?",
            choices=months,
            style=custom_style
        ).ask()
        
        if start_month_choice is None:
            return main()
        
        start_month = int(start_month_choice.split("(")[1].rstrip(")"))
        
        # Choose end month
        end_month_choice = questionary.select(
            "¿Mes final?",
            choices=months[start_month-1:],  # Only show months >= start month
            style=custom_style
        ).ask()
        
        if end_month_choice is None:
            return main()
        
        end_month = int(end_month_choice.split("(")[1].rstrip(")"))
        
        # Calculate date range
        start_date = datetime(year, start_month, 1).strftime("%Y-%m-%d")
        if end_month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, end_month + 1, 1) - timedelta(days=1)
        end_date = end_date.strftime("%Y-%m-%d")
        
        print(f"\n✅ Rango seleccionado: {start_month_choice.split('(')[0].strip()} a {end_month_choice.split('(')[0].strip()} de {year}")
        print(f"   ({start_date} a {end_date})")
        
    elif date_range_type == "month":
        # Choose year
        current_year = datetime.now().year
        year = questionary.text(
            "¿Qué año?",
            default=str(current_year),
            validate=lambda x: x.isdigit() and 2020 <= int(x) <= 2030 or "❌ Año inválido (2020-2030)"
        ).ask()
        
        if year is None:
            return main()
        
        year = int(year)
        
        # Choose month
        months = [
            "Enero (1)", "Febrero (2)", "Marzo (3)", "Abril (4)",
            "Mayo (5)", "Junio (6)", "Julio (7)", "Agosto (8)",
            "Septiembre (9)", "Octubre (10)", "Noviembre (11)", "Diciembre (12)"
        ]
        
        month_choice = questionary.select(
            "¿Qué mes?",
            choices=months,
            style=custom_style
        ).ask()
        
        if month_choice is None:
            return main()
        
        month = int(month_choice.split("(")[1].rstrip(")"))
        start_date, end_date = get_month_dates(year, month)
        
        print(f"\n✅ Rango seleccionado: {start_date} a {end_date}")
        
    else:  # custom range
        start_date = questionary.text(
            "Fecha inicial (YYYY-MM-DD):",
            validate=validate_date
        ).ask()
        
        if start_date is None:
            return main()
        
        end_date = questionary.text(
            "Fecha final (YYYY-MM-DD):",
            validate=validate_date
        ).ask()
        
        if end_date is None:
            return main()
        
        print(f"\n✅ Rango personalizado: {start_date} a {end_date}")
    
    # Step 4: Workers configuration
    workers = questionary.select(
        "¿Cuántos workers paralelos quieres usar?",
        choices=[
            questionary.Choice("⚡⚡⚡ 50 workers (ultra rápido - recomendado)", value="50"),
            questionary.Choice("⚡⚡ 30 workers (rápido y estable)", value="30"),
            questionary.Choice("⚡ 20 workers (default)", value="20"),
            questionary.Choice("🐢 10 workers (conservador)", value="10"),
        ],
        style=custom_style
    ).ask()
    
    if workers is None:
        return main()
    
    # Step 5: Email mapping file (optional)
    available_files = find_email_mapping_files()
    json_file = None
    
    if available_files:
        print(f"\n✅ Se encontraron {len(available_files)} archivo(s) de mapeo")
        use_default = questionary.confirm(
            f"¿Usar el archivo más reciente? ({os.path.basename(available_files[-1])})",
            default=True,
            style=custom_style
        ).ask()
        
        if use_default is None:
            return main()
        
        if use_default:
            json_file = available_files[-1]
        else:
            json_file = questionary.path(
                "Especifica la ruta del archivo:"
            ).ask()
            
            if json_file is None:
                return main()
    else:
        print("\n⚠️  No se encontró archivo de mapeo automáticamente")
        print("💡 El script lo generará automáticamente si es necesario")
    
    # Step 6: Confirmation
    print("\n" + "="*70)
    print("📋 RESUMEN DE CONFIGURACIÓN")
    print("="*70)
    
    if analysis_type == "daily":
        print("📊 Análisis: Totales diarios")
    elif analysis_type == "by_model":
        print("📊 Análisis: Desglose por modelo")
    elif analysis_type == "monthly":
        print("📊 Análisis: Resumen mensual")
    else:
        print("📊 Análisis: Ambos (totales + por modelo)")
    
    print(f"📅 Período: {start_date} a {end_date}")
    print(f"⚡ Workers: {workers}")
    if json_file:
        print(f"📁 Archivo mapeo: {os.path.basename(json_file)}")
    else:
        print(f"📁 Archivo mapeo: Se generará automáticamente")
    print("="*70 + "\n")
    
    proceed = questionary.confirm(
        "¿Continuar con el análisis?",
        default=True,
        style=custom_style
    ).ask()
    
    if not proceed:
        print("\n❌ Análisis cancelado\n")
        return
    
    # Step 7: Execute the script(s)
    print("\n🚀 Iniciando análisis...\n")
    print("="*70 + "\n")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if analysis_type == "monthly":
        print("📆 Ejecutando: Resumen mensual de credits\n")
        cmd = [
            sys.executable,
            os.path.join(script_dir, "team_monthly_credits.py"),
            "--start-date", start_date,
            "--end-date", end_date,
            "--workers", workers
        ]
        if json_file:
            cmd.extend(["--json-file", json_file])
        
        result = subprocess.run(cmd)
        
        if result.returncode != 0:
            print("\n❌ Error al ejecutar el análisis mensual")
            return
    
    elif analysis_type in ["daily", "both"]:
        print("📊 Ejecutando: Totales diarios de flex credits\n")
        cmd = [
            sys.executable,
            os.path.join(script_dir, "team_daily_flex_credits.py"),
            "--start-date", start_date,
            "--end-date", end_date,
            "--workers", workers
        ]
        if json_file:
            cmd.extend(["--json-file", json_file])
        
        result = subprocess.run(cmd)
        
        if result.returncode != 0:
            print("\n❌ Error al ejecutar el análisis de totales diarios")
            return
        
        if analysis_type == "both":
            print("\n" + "="*70 + "\n")
    
    if analysis_type in ["by_model", "both"]:
        print("🤖 Ejecutando: Desglose por modelo de lenguaje\n")
        cmd = [
            sys.executable,
            os.path.join(script_dir, "flex_credits_by_model.py"),
            "--start-date", start_date,
            "--end-date", end_date,
            "--workers", workers
        ]
        if json_file:
            cmd.extend(["--json-file", json_file])
        
        result = subprocess.run(cmd)
        
        if result.returncode != 0:
            print("\n❌ Error al ejecutar el análisis por modelo")
            return
    
    # Step 8: Success message
    print("\n" + "="*70)
    print("✅ ¡Análisis completado exitosamente!")
    print("="*70)
    print(f"\n📁 Los resultados se guardaron en: {os.path.join(script_dir, 'output')}\n")
    
    # Step 9: Ask to run another analysis
    run_another = questionary.confirm(
        "¿Quieres realizar otro análisis?",
        default=False,
        style=custom_style
    ).ask()
    
    if run_another:
        print("\n")
        return main()
    else:
        print("\n👋 ¡Hasta luego!\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Análisis interrumpido por el usuario\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}\n")
        sys.exit(1)
