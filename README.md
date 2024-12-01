
# CS50p Final Project
# PyVentory

![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/z6wsdvemve5r12mfbvn2.png)



#### Video Demo:  <https://www.youtube.com/watch?v=Ummuj-72A7g>
#
#
## **DESCRIPTION**
This Program is a basic inventory manager in which a user could add items, edit/delete items, view inventory, generate barcodes for items, search for items by using a barcodes, as well as saving the inventory as a PDF.

### **How the Program Works?**
The Program uses many librarys, including: Tkinter for UI, PIL for images, SQLite3 for databases, random, python-barcode to generate barcodes, pyzbar to read barcodes, FPDF2 to create PDFs, as well as a few others, to manage the user's inventory, along with making it easy for the user to manipulate.


## **Installing Libraries**
There is a a requirements.txt file that has all the libraries used.

and simply can be install by this pip command:

```pip install -r requirements.txt```

## Screenshots

![Main Menu](https://github.com/user-attachments/assets/2803b92b-169e-4f7d-9f13-50b3d70b1b6d)

![View/Generate/Search/Save Menu](https://github.com/user-attachments/assets/157a4d51-7724-45fb-948b-9d382b9ef1e6)

![Add An Item](https://github.com/user-attachments/assets/c4665522-d79f-459d-92fd-d86a7a7110f8)

![Edit/Delete Menu](https://github.com/user-attachments/assets/211c342b-e7a3-4562-ab94-42861b33aed4)

![example barcode](https://github.com/user-attachments/assets/d79240ae-1b83-4088-b056-9d87eb474dcf)

![PDF example](https://github.com/user-attachments/assets/1dcdd8e9-6823-445b-9279-dc2360c40ec4)

## Usage/Examples
To use, you simply press buttons and enter info if needed. 

To view the inventory simply click the "View Inventory" button on the main menu. From there you could also select a item and generate a unique barcode for it, search a item from a already made barcode, or save the inventory as a PDF.

To add an item, click the "Add An Item" button on the main menu.
Once clicked, it will give you a popup to enter the item's info. If you do not have a Item ID for it already, click the Generate ID button to generate a unused, unique Item ID. When done, simply click Save to save the item to the inventory.

To edit or delete a item from the inventory, click the "Edit or Delete Item" button on the main menu. There you will find a box in which you can select an item, and below, you will find a few buttons in which you can edit, or delete an item.

Once done, feel free to click the handy "Exit Program" button on the main menu to, obviously, exit the program.
## Running Tests

Inclued is a file that contains some PyTest functions. Feel free to test anytime by running this command while in the correct dir:

```bash
  pytest test_project.py
```


#
#
## __Libraries__

__RANDOM__ : This module implements pseudo-random number generators for various distributions. [(Readmore)](https://docs.python.org/3/library/random.html)

__TKINTER__ : The tkinter package (“Tk interface”) is the standard Python interface to the Tcl/Tk GUI toolkit. Both Tk and tkinter are available on most Unix platforms, including macOS, as well as on Windows systems. [(Readmore)](https://docs.python.org/3/library/tkinter.html)

__PILLOW__ : The Python Imaging Library adds image processing capabilities to your Python interpreter. [(Readmore)](https://pillow.readthedocs.io/en/stable/)

__SQLITE3__ : SQLite is a C library that provides a lightweight disk-based database that doesn’t require a separate server process and allows accessing the database using a nonstandard variant of the SQL query language. [(Readmore)](https://docs.python.org/3/library/sqlite3.html)

__PYTHON-BARCODE__ : python-barcode is a pure-python library for generating barcodes in various formats. It’s 100% pure python. [(Readmore)](https://python-barcode.readthedocs.io/en/stable/)

__PYZBAR__ : Read one-dimensional barcodes and QR codes from Python 2 and 3 using the zbar library. [(Readmore)](https://pypi.org/project/pyzbar/)

__FPDF2__ : fpdf2 is a library for simple & fast PDF document generation in Python. [(Readmore)](https://pypi.org/project/fpdf2/)
![Logo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/z6wsdvemve5r12mfbvn2.png)


__DATETIME__ : The datetime module supplies classes for manipulating dates and times. [(Readmore)](https://docs.python.org/3/library/datetime.html)


## Authors

- [@GoobersG](https://github.com/GoobersG)

