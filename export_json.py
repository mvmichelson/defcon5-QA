import os
import django
from django.core.management import call_command
from django.core.management.base import CommandError

# Configura las settings del proyecto
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DEFCON5.settings")
django.setup()

# Ruta de salida del backup
output_path = "bcp/fixtures/backup.json"

try:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        call_command("dumpdata", "--natural-foreign", "--natural-primary", indent=2, stdout=f)
    print(f"[✔] Backup exitoso. Datos guardados en: {output_path}")
except CommandError as ce:
    print(f"[✘] Error al ejecutar dumpdata: {ce}")
except Exception as e:
    print(f"[✘] Error inesperado: {e}")
