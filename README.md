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

