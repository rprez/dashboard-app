# dashboard-app

## Descripción

Dashboard web para monitoreo de los medidores inteligentes. Permite ver el estado de salud de los medidores, mostrando los que se encuentran activos.

El dashboard esta desarrollado sobre el framework Flask y las gráficas son realizadas con Dash

## Requisitos

### runtime
 Python 3.6 o +

### dependencias

Listadas en el requirements.txt

* Flask
* Flask-SQLAlchemy
* Flask-RESTful
* gunicorn
* psycopg2-binary
* cx_Oracle
* dash
* dash-daq

### Server 

Se levanta el server a través de Gunicorn y el modulo run_app.

#### Entorno simple para levantar Gunicorn
* gunicorn run_app:server

## Configuración

### Variables de ambientes
* **APP_SETTINGS** - Configuración de la aplicación:
    * config.ProductionConfig
    * config.StagingConfig
    * config.DevelopmentConfig
    * config.TestingConfig
    
* **PG_CONNECTION** - Conexión a PostGres ej: postgres:postgres@172.17.0.3:5432/utenotificaciones
* **ORA_CONNECTION** - Conexión a Oracle ej: ute:ute@172.17.0.3:1521/ORCLCDB

### Oracle
Instalar el driver correspondiente a la versión desde:
* https://oracle.github.io/odpi/doc/installation.html#other-platforms
