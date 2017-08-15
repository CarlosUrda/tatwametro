# Tatwámetro
## Implementación de un tatwámetro para el cálculo de tatwas.

### Requisitos
El proyecto se ha realizado usando las versiones de herramientas y módulos (versiones anteriores no han sido probadas):
- *Python >= 3.5*
- *requests >= 2.18.3*
- *pytz >= 2017.2*
- *datetime*
- *ast*

En el módulo *claves.py* deben estar las claves privadas para acceso a API. Los nombres de variables a asignar dichas claves privadas son:
- **TIMEZONEDB_API_KEY**: clave de acceso a la API TimeZoneDB de zonas horarias.

### Ejecución
Importar el proyecto:
``` 
git clone https://github.com/CarlosUrda/tatwametro.git`
cd tatwametro
``` 

Para ejecutarlo se puede usar el intérprete Python 3.

`python3 tatwametro`

o (en Linux) configurar el archivo *tatwametro.py* como ejecutable y ejecutarlo directamente:
```
chmod +x tatwametro.py
./tatwametro.py
```

### Recursos externos
Se han usado las siguientes API:
- *https://sunrise-sunset.org/api* para obtener las horas de eventos del sol: salida, puesta, crepúsculos, etc.
- *https://timezonedb.com/api* para obtener la zona horaria.

### Agradecimientos
*Agradece el proyecto al autor => https://saythanks.io/to/CarlosUrda*
