# weatherstation

Read data from various sensors, send them to RabbitMQ. Build internal stack which reads the data, stores in a timescaledb and provides possibilitiers to process and display them via JupyterNotebook, Grafana and Plotly Dash.

## Sensor reader
Install by creating a venv with system packages (important for gpio stuff)
wetter@wetter02:~/weatherstation/read_sensors $ python3 -mvenv venv --system-site-packages
Install requirements
wetter@wetter02:~/weatherstation/read_sensors $ venv/bin/pip install requirements.txt 

Create .env ile with parameters to access the messagebroker

