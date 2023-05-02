# XML/HTML parser

The XML/HTML parser supports the following file formats of publishers.

<table>
    <tr>
        <td><b>Format</b></td>
        <td><b>Publisher</b></td>
        <td><b>DOI prefix</b></td>
        <td><b>Func. arg.</b></td>
    </tr>
    <tr>
        <td>XML</td>
        <td>Elsevier</td>
        <td>10.1016</td>
        <td>elsevier</td>
    </tr>
    <tr>
        <td rowspan="11">HTML</td>
    </tr>
    <tr>
        <td>ASME</td>
        <td>10.1115</td>
        <td>asme</td>
    </tr>
    <tr>
        <td>Emerald</td>
        <td>10.1108</td>
        <td>emerald</td>
    </tr>
    <tr>
        <td>IOP</td>
        <td>10.1088</td>
        <td>iop</td>
    </tr>    
    <tr>
        <td>MDPI</td>
        <td>10.3390</td>
        <td>mdpi</td>
    </tr>    
    <tr>
        <td>Nature</td>
        <td>10.1038</td>
        <td>nature</td>
    </tr>         
    <tr>
        <td>Sage</td>
        <td>10.1177</td>
        <td>sage</td>
    </tr>      
    <tr>
        <td>SPIE</td>
        <td>10.1117</td>
        <td>spie</td>
    </tr>      
    <tr>
        <td>Springer</td>
        <td>10.1007<br>10.1557</td>
        <td>springer</td>
    </tr>      
    <tr>
        <td>Taylor & Francis</td>
        <td>10.1080</td>
        <td>taylorfrancis</td>
    </tr>      
    <tr>
        <td>Wiley</td>
        <td>10.1002<br>10.1111</td>
        <td>wiley</td>
    </tr>      
</table>


## Usage

Download the `doc_parser.py` file and import the function `parser`.

INPUT

`parser` includes 4 function arguments, *path*, *file*, *publisher* and *doi*, which is defined as

``` python
def parser(path,file,publisher='',doi='')
```

*path* and *file* specify the file for parsing.
The default values of *publisher* and *doi* are set as empty strings, but at least one of them should be passed to the `parser` to specify the type of parser.
Use the function arguments (func. arg.) defined in the above table for *publisher*, which are case-sensitive.

OUTPUT

`parser` returns a class instance which inludes variables, *path*, *file*, *title*, *abstract*, *keywords*, *doi* and *sections*.
 *keywords* and *sections* are lists and other variables are strings.
 The element of *sections* are dictionaries, which contains 'sec_title' and 'content'.
 'sec_title' stands for section title in the string format.
 'content' is a list of strings or dictionaries.
 Each string is a paragraph and each dictionary is a sub-section whose format is the same to the section. 

A example for the `parser` is given below:

``` python
from doc_parser import parser

path='$PATH'
file='$FILE'
publisher='elsevier'
doi='10.1016/xxx'
d=parser(path,file,publisher,doi)
```

Please change '\$PATH' and '\$FILE' to your path and filename of the document. '\$PATH' should be ended with a '/'.
