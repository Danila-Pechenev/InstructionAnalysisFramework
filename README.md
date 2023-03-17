# Instruction analysis framework
## Description [En]
### Problem
During the migration software to processors of the new open RISC-V
architecture, the issue of optimizing programs for this architecture is acute.
It would be useful for compiler developers or specialists optimizing specific sections of machine code in a non-trivial
way manually to understand which applications and utilities in popular
GNU/Linux distributions on the x86-64 platform use, for example, vector extensions or
instructions to speed up encryption. This knowledge would help to understand how to improve
the compiler or in which programs there are sections of machine code that need
to be optimized manually for the RISC-V architecture.

This is far from the only case when statistical analysis of data on
the appearance of various instructions (or groups of instructions) in the machine code of programs would be useful.
Another example is the situation when the compiler developer needs to find out how
the generated machine code of programs has changed in general after changes in the compiler. This technique,
in particular, is used to assess the quality of firmware optimization of embedded systems
such as routers and data warehouses.

In order to quickly find answers to such questions, a framework
is being created that automates the collection of data on the use of machine instructions
and provides tools for their statistical analysis and visualization.

### Getting started
To start using the capabilities of the framework, you need to
1. Make a fork of this repository.
2. Clone the fork.
3. Create and activate virtual environment.
```bash
[InstructionAnalysisFramework]$ python -m venv venv
[InstructionAnalysisFramework]$ source venv/bin/activate
```
4. Install requirements.
```bash
(venv) [InstructionAnalysisFramework]$ pip install -r requirements.txt
```

### Data collection
A [Python script](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/src/data_collection.py) was written to collect the data.
It provides many options for configuration for the needs of particular
users. In general, the script runs through certain files in parallel and tries to get an assembly listing
of each file. If the attempt is successful, that is, the file contains the code,
the path to the file and the number of all instructions found in it are
recorded in a csv table, which is the result of the script. Program parameters determine
which files script goes through. You can get acquainted with them as follows:
```bash
(venv) [...]$ python src/data_collection.py --help
```
For example, one can run a script on all files that are available in the system as follows:
```bash
(venv) [...]$ python src/data_collection.py -r <path to table>
```
In order for data collection to take place on different GNU/Linux
distributions, regardless of which operating system is installed on the machine
on which the script is running, the script is run in Docker containers.
The [dockerfiles](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/tree/master/dockerfiles) folder
contains dockerfiles for building images. They include the installation of a utility for obtaining
assembly listings of programs, as well as the installation of all programs whose machine
code data the user wants to get. This approach allows the framework to achieve
extensibility — to add a distribution for scanning, one just needs
to add the corresponding docker file.

Data is collected using GitHub Actions in two stages ([yml-file](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/.github/workflows/DC.yml)).
First, the images are collected according to docker files and published in the [repository](https://hub.docker.com/repository/docker/danilapechenev/instruction-analysis/general)
on DockerHub. If the dockerfile has not been modified since the last GitHub Actions workflow,
the image is not reassembled. At the next stage, data is collected on all
distributions in parallel: in each distribution, an image is loaded from
DockerHub, a Docker container is launched, and a Python script is run in it
that generates a table with data. The resulting tables are stored in archives  on GitHub Actions
as workflow artifacts.

## Описание [Ru]
### Проблема
При миграции программного обеспечения на процессоры новой открытой архитектуры RISC-V
остро стоит вопрос оптимизации программ именно под эту архитектуру. Разработчикам
компиляторов или специалистам, оптимизирующим отдельные участки машинного кода нетривиальным
образом вручную, было бы полезно понимать, в каких приложениях и утилитах в популярных
дистрибутивах GNU/Linux на платформе x86-64 используются, например, векторные расширения или
инструкции для ускорения шифрования. Эти знания помогли бы понять, как можно улучшить
компилятор или в каких программах есть участки машинного кода, которые необходимо
оптимизировать вручную для архитектуры RISC-V.

Это далеко не единственный случай, когда был бы полезен статистический анализ данных о
появлении различных инструкций (или групп инструкций) в машинном коде программ. Другим
примером является ситуация, когда разработчику компилятора необходимо узнать, как в целом
поменялся сгенерированный машинный код программ после изменений в компиляторе. Эта методика,
в частности, применяется для оценки качества оптимизации прошивок встраиваемых систем,
например, маршрутизаторов и хранилищ данных.

С целью быстрого нахождения ответов на такого рода вопросы создается фреймворк,
автоматизирующий сбор данных об использовании машинных инструкций и предоставляющий
инструментарий для их статистического анализа и визуализации.

### Начало работы
Чтобы начать пользоваться возможностями фреймворка, необходимо
1. Сделать форк этого репозитория.
2. Склонировать форк.
3. Создать и активировать виртуальное окружение.
```bash
[InstructionAnalysisFramework]$ python -m venv venv
[InstructionAnalysisFramework]$ source venv/bin/activate
```
4. Установить необходимые пакеты.
```bash
(venv) [InstructionAnalysisFramework]$ pip install -r requirements.txt
```
### Сбор данных
Для сбора данных был написан [Python-скрипт](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/src/data_collection.py).
Он предоставляет множество возможностей для конфигурации под нужды конкретных
пользователей. В целом, скрипт параллельно проходит по определенным файлам и пробует получить ассемблерный
листинг каждого файла. Если попытка удачна, то есть файл содержит код, путь до файла
и количество всех инструкций, встречающихся в нем, записываются в csv-таблицу,
которая и является результатом работы скрипта. По каким именно файлам необходимо
пройтись и определяют параметры программы. Ознакомиться с ними можно так:
```bash
(venv) [...]$ python src/data_collection.py --help
```
Например, запустить скрипт на всех файлах, которые имеются в системе, можно следующим образом:
```bash
(venv) [...]$ python src/data_collection.py -r <path to table>
```
Чтобы сбор данных мог происходить на разных дистрибутивах GNU/Linux
вне зависимости от того, какая операционная система установлена на машине,
производящей запуск, скрипт запускается в Docker-контейнерах.
В папке [dockerfiles](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/tree/master/dockerfiles)
находятся докерфайлы для сборки образов. Они включают в себя установку утилиты для получения
ассемблерных листингов программ, а также установку всех программ, данные о машинном
коде которых пользователь хочет получить. Такой подход позволяет достигнуть
расширяемости — чтобы добавить дистрибутив для сканирования, нужно лишь
добавить соответствующий ему докерфайл.

Сбор данных происходит при помощи GitHub Actions в два этапа ([yml-файл](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/.github/workflows/DC.yml)).
Сначала образы собираются согласно докерфайлам и публикуются в [репозитории](https://hub.docker.com/repository/docker/danilapechenev/instruction-analysis/general)
на DockerHub. В случае, если докерфайл не был изменен с момента последнего
запуска процесса на GitHub Actions, повторная сборка образа не производится.
На следующем этапе данные собираются на всех дистрибутивах параллельно:
в каждом дистрибутиве загружается образ с DockerHub,
запускается Docker-контейнер, а в нем запускается Python-скрипт,
генерирующий таблицу с данными. Полученные таблицы сохраняются в архивах как
артефакты запуска процесса на GitHub Actions.
