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
A [Python script](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/data_collection.py) was written to collect the data.
It provides many options for configuration for the needs of particular
users. In general, the script runs through certain files in parallel and tries to get an assembly listing
of each file. If the attempt is successful, that is, the file contains the code,
the path to the file and the number of all instructions found in it are
recorded in a csv table, which is the result of the script. Program parameters determine
which files script goes through. You can get acquainted with them as follows:
```bash
(venv) [...]$ python data_collection/data_collection.py --help
```
For example, one can run a script on all files that are available in the system as follows:
```bash
(venv) [...]$ python data_collection/data_collection.py -r <path to the table>
```
#### On different GNU/Linux distributions
In order for data collection to take place on different GNU/Linux
distributions, regardless of which operating system is installed on the machine
on which the script is running, the script is run in Docker containers.
The [dockerfiles](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/tree/master/dockerfiles) folder
contains dockerfiles for building images. They include the installation of a utility for obtaining
assembly listings of programs, as well as the installation of all programs whose machine
code data the user wants to get. This approach allows the framework to achieve
extensibility — to add a distribution for scanning, one just needs
to add the corresponding docker file.

Data is collected using GitHub Actions in two stages ([yml-file](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/.github/workflows/DockerContainersDC.yml)).
First, the images are collected according to docker files and published in the [repository](https://hub.docker.com/repository/docker/danilapechenev/instruction-analysis/general)
on DockerHub. If the dockerfile has not been modified since the last GitHub Actions workflow,
the image is not reassembled. At the next stage, data is collected on all
distributions in parallel: in each distribution, an image is loaded from
DockerHub, a Docker container is launched, and a Python script is run in it
that generates a table with data. The resulting tables are stored in archives  on GitHub Actions
as workflow artifacts.
#### On different platforms
The framework provides the ability to scan iso images, which allows one to collect data
from different instruction set architectures (ISA). One can run a [script](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/local_iso_collection.sh)
to collect data from an iso image that is already on the disk, or use a [script](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/url_iso_collection.sh)
to scan the image by its URL.

In addition, data from iso images by their URL can be collected using GitHub Actions ([yml-file](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/.github/workflows/IsoImagesDC.yml)).
For this purpose, some information about the processed images is written to a special [json file](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/iso-images.json),
in particular, the URL and objdump, which will be used in the data collection process.
Then, the process on GitHub Actions, using an auxiliary [Python script](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/gha_iso_scanner.py),
reads data from a json file, installs the necessary utilities, downloads and scans iso images.
The resulting tables are stored in archives  on GitHub Actions as workflow artifacts.

### Data analysis
Archives with tables are downloaded and analyzed in the Jupiter Notebook interactive environment
both using standard functions provided by the pandas library and using
[functions](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_analysis/analysis_tool.py)
provided by the framework.
An example of such an analysis with a demonstration of some capabilities of
the tool is presented in [demo.ipynb](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_analysis/demo.ipynb).
The functions for analysis and visualization are carefully documented. The documentation is
[published](https://danila-pechenev.github.io/InstructionAnalysisFramework/namespaceanalysis__tool.html)
on GitHub Pages and is updated automatically when changes occur.

### Dvision of instructions into categories and groups
There are a lot of instructions, and this can create inconvenience when analyzing data about their use.
Framework users may want to divide instructions into clusters. To solve this problem, a [Python script](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/scripts/x86-64_instructions.py) was written
that collects information from [the site](https://linasm.sourceforge.net/docs/instructions/index.php),
where a fairly large number of different instructions are presented.
We call the category of the instruction the section of the site on the left where it
is included, and the group — its subsection in it. Thus, the script collects for
each instruction its description, category and group and stores the result in
[json file](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/x86-64_instructions.json).
The division of instructions into categories and groups significantly increases completeness of information and
clarity of data analysis.

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
Для сбора данных был написан [Python-скрипт](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/data_collection.py).
Он предоставляет множество возможностей для конфигурации под нужды конкретных
пользователей. В целом, скрипт параллельно проходит по определенным файлам и пробует получить ассемблерный
листинг каждого файла. Если попытка удачна, то есть файл содержит код, путь до файла
и количество всех инструкций, встречающихся в нем, записываются в csv-таблицу,
которая и является результатом работы скрипта. По каким именно файлам необходимо
пройтись и определяют параметры программы. Ознакомиться с ними можно так:
```bash
(venv) [...]$ python data_collection/data_collection.py --help
```
Например, запустить скрипт на всех файлах, которые имеются в системе, можно следующим образом:
```bash
(venv) [...]$ python data_collection/data_collection.py -r <path to the table>
```
#### На разных дистрибутивах GNU/Linux
Чтобы сбор данных мог происходить на разных дистрибутивах GNU/Linux
вне зависимости от того, какая операционная система установлена на машине,
производящей запуск, скрипт запускается в Docker-контейнерах.
В папке [dockerfiles](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/tree/master/dockerfiles)
находятся докерфайлы для сборки образов. Они включают в себя установку утилиты для получения
ассемблерных листингов программ, а также установку всех программ, данные о машинном
коде которых пользователь хочет получить. Такой подход позволяет достигнуть
расширяемости — чтобы добавить дистрибутив для сканирования, нужно лишь
добавить соответствующий ему докерфайл.

Сбор данных происходит при помощи GitHub Actions в два этапа ([yml-файл](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/.github/workflows/DockerContainersDC.yml)).
Сначала образы собираются согласно докерфайлам и публикуются в [репозитории](https://hub.docker.com/repository/docker/danilapechenev/instruction-analysis/general)
на DockerHub. В случае, если докерфайл не был изменен с момента последнего
запуска процесса на GitHub Actions, повторная сборка образа не производится.
На следующем этапе данные собираются на всех дистрибутивах параллельно:
в каждом дистрибутиве загружается образ с DockerHub,
запускается Docker-контейнер, а в нем запускается Python-скрипт,
генерирующий таблицу с данными. Полученные таблицы сохраняются в архивах как
артефакты запуска процесса на GitHub Actions.
#### На разных платформах
Фреймворк предоставляет возможность сканирования iso-образов, что позволяет собирать данные
с разных архитектур набора команд. Можно запустить [скрипт](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/local_iso_collection.sh)
для сбора данных с iso-образа, который уже лежит на диске, или воспользовать [скриптом](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/url_iso_collection.sh)
для сканирования образа по его URL.

Помимо этого, данные с iso-образов по их URL могут собираться при помощи GitHub Actions ([yml-файл](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/.github/workflows/IsoImagesDC.yml)).
Для этого в специальный [json-файл](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/iso-images.json)
записывается некоторая информация об обрабатываемых образах, в частности, URL и objdump, который будет использоваться в процессе сбора данных.
Далее процесс на GitHub Actions, используя вспомогательный [Python-скрипт](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/gha_iso_scanner.py),
считывает данные с json-файла, устанавливает необходимые утилиты, скачивает и сканирует iso-образы.
Полученные таблицы сохраняются в архивах как
артефакты запуска процесса на GitHub Actions.

### Анализ данных
Архивы с таблицами скачиваются и анализируются в интерактивной среде Jupyter Notebook
как при помощи стандартных функций, предоставляемых библиотекой pandas, так и с помощью
[функций](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_analysis/analysis_tool.py),
предоставляемых фреймворком. Пример такого анализа с демонстрацией некоторых
возможностей инструмента представлен в [demo.ipynb](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_analysis/demo.ipynb).
Функции для анализа и визуализации тщательно документирована. Документация
[публикуется](https://danila-pechenev.github.io/InstructionAnalysisFramework/namespaceanalysis__tool.html)
на GitHub Pages и при изменениях обновляется автоматически.

### Разделение инструкций на категории и группы
Инструкций очень много, и это может создать неудобства при анализе данных об их использовании.
У пользователей фреймворка может возникнуть желание разделить инструкции на кластеры. Для решения этой проблемы был
написан [Python-скрипт](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/scripts/x86-64_instructions.py),
собирающий информацию с [сайта](https://linasm.sourceforge.net/docs/instructions/index.php),
где представлено достаточно большое количество различных инструкций.
Мы будем называть категорией инструкции тот раздел сайта слева, куда она
включена, а группой — ее подраздел в нем. Таким образом, скрипт собирает для
каждой инструкции ее описание, категорию и группу и сохраняет результат в
[json-файле](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/x86-64_instructions.json).
Разделение инструкций на категории и группы значительно повышает информативность и
ясность анализа данных.
