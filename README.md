# Instruction analysis framework
## Description
### Problem
Currently, the open source RISC-V Instruction Set Architecture (ISA) is actively
developing and gaining popularity. In the RISC-V community, the issue of optimizing
programs specifically for this architecture is acute. In order to plan software migration,
compiler developers and specialists optimizing particular sections of machine code
in a non-trivial way manually need to understand which packages and utilities in
popular GNU/Linux distributions on various platforms use, for example, vector extensions
or instructions for speeding up encryption. This knowledge would help them understand
how the compiler can be improved and in which programs there are sections of
machine code that should be optimized manually for the RISC-V architecture.

In this context, it is also necessary to understand how the various GNU/Linux
distributions are ready to migrate to RISC-V, that is, how the machine code of
their packages is optimized and able to perform tasks in an effective manner.

To achieve this, a statistical analysis of the machine code is essential, namely,
an analysis of the use of different types of machine instructions in the program code.
However, the described problems are far from the only cases when such an analysis
would be useful. Another example is the situation when the compiler developer needs
to find out how the generated machine code of programs has changed in general after
changes in the compiler.

This repository provides a framework that will make it much easier to answer
such questions. On the one hand, it allows one to automate the collection of data
on the machine instruction usage on different GNU/Linux distributions and architectures,
and on the other hand, it provides a wide range of tools for statistical analysis
and visualization of this data.

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
A [Python program](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/data_collection.py) was written to collect the data.
It provides many options for configuration for the needs of particular
users. In general, the program runs through certain files in parallel and tries to get an assembly listing
of each file. If the attempt is successful, that is, the file contains the code,
the path to the file and the number of all instructions found in it are
recorded in a csv table, which is the result of the program. Program parameters determine
which files program goes through. One can get acquainted with them as follows:
```bash
(venv) [...]$ python data_collection/data_collection.py --help
```
For example, one can run a program on all files that are available in the system as follows:
```bash
(venv) [...]$ python data_collection/data_collection.py -r <path to the table>
```
#### On different GNU/Linux distributions
In order for data collection to take place on different GNU/Linux
distributions, regardless of which operating system is installed on the machine
on which the program is running, the program is run in Docker containers.
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
DockerHub, a Docker container is launched, and a program is run in it
that generates a table with data. The resulting tables are stored in archives  on GitHub Actions
as workflow artifacts.
#### On different platforms
The framework provides the ability to scan disk images (now in .iso format), which allows one to collect data
from different instruction set architectures (ISA). One can run a [script](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/local_disk_image_collection.sh)
to collect data from a disk image that is already downloaded, or use a [script](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/url_disk_image_collection.sh)
to scan the image by its URL. For example, one can collect data from an image by URL as follows:
```bash
(venv) [...]$ ./data_collection/url_iso_collection.sh <link to disk image> <table path>
```

In addition, data from disk images by their URL can be collected using GitHub Actions ([yml-file](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/.github/workflows/DiskImagesDC.yml)).
For this purpose, some information about the processed images is written to a special [json file](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/disk-images.json),
in particular, the URL and objdump, which will be used in the data collection process.
Then, the process on GitHub Actions, using an auxiliary [Python program](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/data_collection/gha_disk_image_scanner.py),
reads data from a json file, installs the necessary utilities, downloads and scans disk images.
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
Framework users may want to divide instructions into clusters.
At the moment, the framework provides an approach for
solving this problem for the x86-64 architecture. For this purpose, a [Python program](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/scripts/x86-64_instructions.py) was written
that collects information from the [site](https://linasm.sourceforge.net/docs/instructions/index.php),
covering a fairly large number of instructions.
We call the category of the instruction the section of the site on the left where it
is included, and the group — its subsection in it. Thus, the program collects for
each instruction its description, category and group and stores the result in a
[json file](https://github.com/Danila-Pechenev/InstructionAnalysisFramework/blob/master/x86-64_instructions.json).
The division of instructions into categories and groups significantly increases completeness of information and
clarity of data analysis.
