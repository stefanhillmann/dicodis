# Introduction

This document describes the conversion of dialogues from the BoRis database (contact Stefan Hillmann for details) in to 
 the format used by this framework.
 
# Conversion
 
## Reading raw data

The BoRis database is originally defined in a Excel-Sheet based document. This document was converted into a CSV (comma 
separated values) document. These CSV files are used for the further conversion process. The CVS is loaded into a list 
of single and processed line by line.
For the further processing it is necessary that each dialogue is represented by one document (see class Document). 

## CSV data

### Raw data

iteration;sysSA;sysRep.field;userFields;userSA
1;request;ALL;field ;provide 
1;indicateValues;foodtype;foodtype ;provide 
1;request;time;time ;provide 
1;request;date;date ;provide 
1;request;price;price ;provide 
1;offerModification;logical;logical ;accept 
1;request;field;field ;provide 
1;indicateValues;foodtype;foodtype ;provide 
1;offerModification;logical;logical ;accept 
1;request;field;field ;provide 
1;indicateValues;foodtype;foodtype ;provide 
1;offerModification;logical;logical ;neglect 
1;bye;bye;;

### Table view of raw data

iteration|sysSA             |sysRep.field   |userFields |userSA
---------|------------------|---------------|-----------|-------
        1|request           |ALL            |field      |provide 
        1|indicateValues    |foodtype       |foodtype   |provide 
        1|request           |time           |time       |provide 
        1|request           |date           |date       |provide 
        1|request           |price          |price      |provide 
        1|offerModification |logical        |logical    |accept 
        1|request           |field          |field      |provide 
        1|indicateValues    |foodtype       |foodtype   |provide 
        1|offerModification |logical        |logical    |accept 
        1|request           |field          |field      |provide 
        1|indicateValues    |foodtype       |foodtype   |provide 
        1|offerModification |logical        |logical    |neglect 
        1|bye               |bye            |           |

### Conversion of on line (of raw data)

In the BoRis data each represents the utterance of the system and the user's subsequent utterance. For the further analysis
a single line in the rwa data is separated into two to tokens of the document. One reelecting the system's utterance and
the other reflecting the user's utterance. In a Document each token is represented by an item in a list (the python data
structure).

#### Conversion of a system utterance

The values of the system utterance (column sysSA and sysRep.field) are concatenated by comma. Thus, the system values of the 
first line in the table are represented by the string 'request,ALL'.

#### Conversion of a user utterance

The conversion is analogue to a system utterance, just the used columns differ: userFields and userSA. The result for the 
first row in the example table is 'field,provide'.

### Resulting document
 
The content of the resulting Document is a list of concatenated, either system or user, values. The list for the first three
  lines of the example table is:
* 'request,all'
* 'field,provide'
* 'indicateValues,foodtype'
* 'foodtype,provide'
* 'request,time'
* 'time,provide'

### Multiple values in one field

If a field in a row (i.e. a cell) contains multiple values, these values are directly concatenated; e.g. 'date' and 'price' 
are joined to 'dateprice'. That procedure has no side effect ot the later n-gram analysis, as the order of a unqiue set
of multiple values is always the same (in the BoRis database).

## Further data of a document

The latterly used n-Gram analysis supports binary classifiers. A binary classifier can distinguish between two categories.
Thus, each document get the information to which class it belongs. This information is stored in the field Dialogue.label.
In order to relieve the assignment of a document to a dialogue (e.g. for debugging), the id of the dialogue (iteration in 
the example data) is stored in the field Document.dialog_id.


