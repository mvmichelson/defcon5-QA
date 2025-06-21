# Navega a la raíz del proyecto DEFCON5 antes de ejecutar

# Extensiones a procesar
$extensiones = @('*.py', '*.html', '*.js', '*.css', '*.txt')

foreach ($ext in $extensiones) {
    Get-ChildItem -Recurse -Include $ext | ForEach-Object {
        $contenido = Get-Content $_.FullName -Raw
        if ($contenido -match 'BCP') {
            $contenidoMod = $contenido -replace 'BCP', 'bcp'
            Set-Content -Path $_.FullName -Value $contenidoMod
            Write-Host "Actualizado $_.FullName"
        }
    }
}
