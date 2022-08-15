# weatherstation

Read data from various sensors, send them to RabbitMQ. Build internal stack which reads the data, stores in a timescaledb and provides possibilitiers to process and display them via JupyterNotebook, Grafana and Plotly Dash.

## Sensor reader
Install by creating a venv with system packages (important for gpio stuff)
wetter@wetter02:~/weatherstation/read_sensors $ python3 -mvenv venv --system-site-packages
Install requirements
wetter@wetter02:~/weatherstation/read_sensors $ venv/bin/pip install requirements.txt 

Create .env ile with parameters to access the messagebroker


## Database
Create Extension:  


CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;

Create Table:  

`
CREATE TABLE ambientdata (
  dt TIMESTAMPTZ NOT NULL,
  sensor VARCHAR(255) NOT NULL,
  humidity DOUBLE PRECISION NULL,
  temperature DOUBLE PRECISION NULL,
  air_pressure DOUBLE PRECISION NULL
);  
  
SELECT create_hypertable('ambientdata','dt');

Create grafana user:
CREATE USER grafana WITH ENCRYPTED PASSWORD 'mypassword';

weatherdata=# GRANT SELECT ON TABLE sensordata to grafana;
GRANT
weatherdata=# GRANT CONNECT ON DATABASE weatherdata TO grafana;
GRANT
weatherdata=# GRANT USAGE ON SCHEMA public TO grafana;
GRANT
`

