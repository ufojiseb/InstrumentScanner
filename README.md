# InstrumentScanner

## Requisites

InstrumentScanner requires external libraries and programs which must be installed in the system in order for the program to run.

- [Python 3.8](https://www.python.org/downloads/) or newer
- [PyPDF2](https://pypi.org/project/PyPDF2/)
- [fpdf](https://pypi.org/project/fpdf/)
- [pytesseract](https://pypi.org/project/pytesseract/)
- [Tesseract](https://github.com/tesseract-ocr/tesseract)
- Poppler (available for [Windows](https://github.com/oschwartz10612/poppler-windows) and [Linux](https://poppler.freedesktop.org/))

## Project layout

In the project directory there are four folders:

|      |      |
| --- | --- |
| images |  **to be ignored**, contains all the images from the pages of all the PDFs |
| input | where the input PDFs with all the scanned scores have to be |
| scores | where the final PDFs will be saved, named with the instrument of the score |
| src | **to be ignored**, contains all the code |

Furthermore, there is `delete.bat` (or `delete.sh` if you are using Linux). These are simple scripts which will delete everything in the folders `images`, `input` and `scores`, as well as `superimposed.png`, which is the superimposed image. They can be run in order to easily reset the working directories between different executions.

## Usage

    python main.py -[mode]

Where `-[mode]` can be:

| mode | name | brief explanation |
| ------ | ------ | ------ |
| -s | split | Split all the PDFs pages in single images and groups them |
| -x | superimpose | Creates the superimposed image in order to see where the instrument names are |
| -r | rename | Tries to read the instrument name for each group, then creates the PDF with the same name |


Note that multiple modes can be used together, such as `-sx` for example.


#### Typical usage

First we have to modify the `config.json` file and change the configurations depending on the properties of the PDF that has to be elaborated. You won't need to change most of the configurations, but three properties in particular has to be checked and eventually changed:

|     |     |
| --- | --- |
| group_number| how many pages there are for each instrument |
| superimposed_index| on which page of each score there is the instrument name |
| paper_format| the format of the paper, either A3, A4 or A5 |

After checking the config, the program can be executed for the first time with:

    python main.py -sx

in order to split the PDFs in images, group them and create the superimposed image.

Open the superimposed image with an image editor and find the area where all the instrument names are. Now, imagining that all the names has to be contained in a box, draw one pixel where the top left corner would be, and another pixel for the bottom right corner. Note that the pixels have to be of the same RGB color specified in the `pixel_color` property. Save and exit the image editor.

After that, the program can be executed a second time with:

    python main.py -r

to rename the groups and create the final PDFs.

The final PDFs can be taken from the `scores` folder, and then you can run `delete.bat` or `delete.sh` to reset all the working directories for the next execution.

## Configuration

The `config.json` file contains all the possible customizable configurations.

| name | default | explanation |
| ----- | ----- | ----- |
| group_number | 1 | number of pages for each instrument |
| superimposed_index | 1 | the number of the page within each group which contains the instrument name, which will be used to create the superimposed image (usually set to 1) |
| paper_format | "A4" | The paper format of each page. Currently supports vertical A4, and horizontal A5 and A3 |
| scores_directory | "scores" | the name of the directory where the final scores will be saved |
| images_directory | "images" | the name of the directory where the groups and images will be saved |
| input_pdf_directory | "input" | the name of the directory where the program will search for PDFs to work on |
| splitter_resolution | 200 | the resolution in ppm of the pdf to png converter |
| enhancing_method | "equalize" | how the images are enhanced. Can either be  `equalize` or `extreme` |
| threshold_factor | 0.2 | factor used to enhance the image |
| threshold_range_min | 50 | used to enhance the image, how much the minimum pixel value will be stretched (only for `equalize` enhancing method) |
| threshold_range_max | 50 | used to enhance the image, how much the maximum pixel value will be stretched (only for `equalize` enhancing method) |
| pixel_color | [237, 28, 36] | the RGB values of the pixels used to signal the extreme corners in the superimposed image |
| default_top_left_corner | [0, 0] | the default coordinates of the top left corner |
| default_bottom_right_corner | [1, 1] | the default coordinates of the bottom right corner |
