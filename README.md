This is a small script to help splitting PDF-bundles with a seperator page.

Use-Case:
You want to scan a lot of documents and have a ADF-Scanner.
Print couple of the seperatorPage.pdf 2-sided (if you can scan 2-sided) and put 
them between each document you want to scan (works fine with multi-Paged documents).

You can put multiple PDF-bundles into a folder.
Use the script on that folder
```sh
    python3 pdf-splitter.py -d /path/to/folder
```
The script searches for barcode pages and splits the bundle accordingly.
They will saved in folder/output with an individual name.
When proccessing the bundle is finish it will be renamed with '*_done'.

<!-- GETTING STARTED -->
## Getting Started
### Prerequisites

You need
* zbar library
    ```sh
    sudo apt-get install libzbar0
    ```
* python_packages 
    ```sh
    pip3 install pyzbar pdf2image PyPDF2 PIL 
    ```


<!-- USAGE EXAMPLES -->
## Usage

```sh
    python3 pdf-splitter.py --help

Splitting script

optional arguments:
    -h, --help  show this help message and exit
    -d [D]      a directory-path to directory
    -t [T]      number of proccesses/threads
    -v          enable some more output
    -single     splits after each page
```
