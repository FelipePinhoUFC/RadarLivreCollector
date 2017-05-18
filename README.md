# RadarLivre

The RadarLivre system is a mixed software-hardware solution based in the ASD-B technology for monitoring the airspace. The main components are: 

* ADS-B receptor
* Software for interpreting the collected data
* Web server that receives the data and store them in a database
* Software for analising the collected information and detecting possible collision between the airplanes and geographical accidents
* Website that presents the data publicly.

## Getting Started

This paper will help you get a copy of the project(client-side) to run it in your local machine. If you are looking for the server-side, [this is the repository](https://github.com/FelipePinhoUFC/RadarLivre). You need both to get the system running.

### Prerequisites

This project was designed to run in ubuntu.
You need to have these installed before installing the project.

```
* Python 2.7
* SQLite database
```

### Installing

Follow these steps to install and run the collector.

* Open the terminal and install Git (if you have done this already, you may skip this step).

```
sudo apt-get install git
```

* Clone this repository from github where you want to have your copy installed.

```
git clone http://github.com/FelipePinhoUFC/RadarLivreCollector.git
```

* From now on, you need to have a running server to send the data. If you have not installed it yet, you need to do it now.
Now we have to create a superuser to manage collectors inside the server.
For this, activate your virtual enviroment where you installed your server by using.

```
source venv/bin/activate
```

* Create a super user. You will be asked to provide a username, email and password. For security reasons, your password need to be strong.

```
python manage.py createsuperuser
```

* Now, you need to add a collector. For this, you need to run the server.

```
python manage.py runserver
```

<!--information about timestamp and timestampData needed-->
* And  access the admin page located at [127.0.0.1:8000/admin](127.0.0.1:8000/admin)(if running a local server) by providing the user you just created. There, click +add in Collectors and provide the information needed. Make sure to link the receptor to the correct user.

* Copy the generated key and change it in "config.py". It should look like:

```
COLLECTOR_ID = “29384c61-c588-488f-9390-52251d6491ed”
```

* If you are not using a local server, you need to change the server host in "config.py" located in the collector folder. Else, skip this step.

```
SERVER_HOST = “http:\\path\to\your\server:port”
```

* Now, change login and password with your created user. It should look like:

```
LOGIN = "username"
PASSWORD = "123password"
```

* Install the library used to send data to the server.

```
sudo apt-get install python-requests
```

* Install the library used to read from serial port(USB port).

```
sudo apt-get install python-serial
```

* Now we are ready to start sending data. Start the receptor.

```
sudo ./start_receptor
```

Congratulations! Now that you you can access your server by going to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser. If you did it right and the collector is feeding the server, you should see the airplanes close to your receptor.
Don't worry if it doesn't display anything as you just started feeding. The airplanes will appear as they come close to your receptor's range. Remember that not every airplane have an ASD-B transceiver that you need.

<!--
## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```
-->

## Deployment

Once you have set up your server, you can aways access it by following these steps:

Activate the virtual enviroment

```
source venv/bin/activate
```

With the virtual enviroment activated, run the server

```
python manage.py runserver
```

Access it by going to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser.

<!--
## Built With

* [Python](https://www.python.org/)
* [Django](https://www.python.org/)
* [Markdown](https://daringfireball.net/projects/markdown/)
* [Pillow](https://python-pillow.org/)
* [SQLite](https://www.sqlite.org/)
* [Virtualenv](https://virtualenv.pypa.io/en/stable/)

## Versioning

We use [SemanticVersioning](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/FelipePinhoUFC/RadarLivre/tags).

## Changelog

You can refer to [CHANGELOG.md](https://github.com/FelipePinhoUFC/RadarLivre/blob/master/CHANGELOG.md) for details about the development and differences between versions.
-->

<!-- Old readme
# Coleta de mensagens ADS-B

O aparelho coletor de mensagens ADS-B é um componente simples, que pode ser instalado e configurado facilmente. É composto por uma antena pequena e um receptor que pode ser conectado a uma porta USB de qualquer computador. Para o tratamento das mensagens recebidas é necessário um software específico. As aplicações disponíveis atualmente para o reconhecimento das mensagens ADS-B são em sua maioria privadas e para o sistema operacional Windows, o que gera uma dependência da plataforma e um alto custo de instalação. O sistema Radar livre conta com seu próprio software de coleta, uma aplicação de código fonte aberto implementada sobre a plataforma linux pela equipe do projeto na UFC. A aplicação interpreta as mensagens e extrai informações como identificação, posicionamento, velocidade e altitude, armazenando-os em um banco de dados local. Posteriormente, os dados são enviados a um servidor web.
_-->