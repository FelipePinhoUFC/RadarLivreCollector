# RadarLivre

The RadarLivre system is a mixed software-hardware solution based in the ASD-B technology for monitoring the airspace. The main components are: 

* ADS-B receptor
* Software for interpreting the collected data
* Web server that receives the data and store them in a database
* Software for analising the collected information and detecting possible collision between the airplanes and geographical accidents
* Website that presents the data publicly.

## Getting Started

This paper will help you get a copy of the project(client-side) to run it with your ADS-B receptor. If you are looking for the server-side, [this is the repository](https://github.com/RadarLivre/RadarLivreCollector).
You need both to get the system running, so it is recomended that, if you plan on running in your local machine, install the server first.

### Prerequisites

This project was designed to run in ubuntu.
You need to have these installed before installing the project.
The other dependencies are covered when installing.

```
* Python 2.7
```

### Installing

Follow these steps to install, configure and run the server.

```
HINT: The following commands in these boxes should be used in your terminal.
```

* Open the terminal by typing CTRL+ALT+T.

* Install Git

```
sudo apt-get install git
```

* Clone this repository from github where you want to have your copy installed.

```
git clone http://github.com/RadarLivre/RadarLivreCollector.git
```

* Enter the RadarLivre collector directory

```
cd RadarLivreCollector
```

* Run INSTALL.sh to install the dependencies.

```
sudo ./INSTALL.sh
```

* From now on, you need to have a running server to send the data. If you have not installed it yet and are planning on running it locally, you need to do it now.
Now we have to create a superuser to manage collectors inside the server. Read the "Create Superuser" section of your server's [README](https://github.com/RadarLivre/RadarLivre/blob/master/README.md).

* Now, you need to add a collector. Read the "Insert new Collector" section of your server's [README](https://github.com/RadarLivre/RadarLivre/blob/master/README.md).

* Run CONFIGURE.sh and follow the instructions to configure your collector.

```
sudo ./CONFIGURE.sh
```

* With the collector configured, we are ready to start sending data. Start the receptor.

```
sudo ./start_receptor
```

Congratulations! Now that you you can access your server by going to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your web browser. If you did it right and the collector is feeding the server, you should see the aircrafts that get close to your receptor.
Don't worry if it doesn't show anything, as you just started feeding. The aircrafts will appear as they come close to your receptor's range. Remember that not every airplane have an ASD-B transceiver that you need to get data.

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

Once you have set up your collector, you can starting sending data by following these steps:

* Run the server (described at the server's README Deployment section).

* Open the terminal by typing CTRL+ALT+T.

* Enter the RadarLivre collector directory

```
cd RadarLivreCollector
```

* Start the receptor.

```
sudo ./start_receptor
```

Then, your server is going to show any ADS-B transceiver equipped aircraft that gets within range.

* You can stop sending data to the server by pressing CTRL+C(in the terminal).

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