# WebModels

This is the project for an assignment for the subject *Web Project*.

## Description

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Installaition

First of all, `clone` the repository.

```
git clone https://github.com/josalhor/WebModels.git
cd WebModels
```

Use `pip` to install Pipenv

```
pip install --user pipenv
```
If pipenv is not available in your shell after the installation you will need to [add the user's binaries root folder to your PATH](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/). 

Use `pipenv` to create the virtual environment and install the
dependencies.

```
pipenv --python 3.9   # Initializes the virtual environment
pipenv install --dev  # Installs all dependencies
pipenv shell  # Activates the environment
```

Use `make` to reset the entire database and run the server,

```
make reset_run
```

or you can directly run the server using 

```
make run
```

If you are using Windows, to use the make command you previously need to [install Chocolatey](https://chocolatey.org/install). Once installed you simlpy need to install make (you may need to run it in an elevated/admin command prompt).

```
choco install make
```

## Documentation

You can find basic functionality of our site in the DOMAIN.md file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Authors

- Josep Maria Salvia Hornos
- Balma Cascón Piñol
- Sara Quejido Garriga
- Anna Torres Tuca

