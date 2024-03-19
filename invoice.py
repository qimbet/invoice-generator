# Jacob Mattie
# Feb 2024

# to do: 
#   Build markdown/html invoice sheet
#   Capitalize First Letters of all "menu list" items in invoice table
#   Remove surplus lines/compactify

import pypandoc
import os

debugFlag = False
mode = input("press Enter to begin program!") 
if(mode == "debug"):
    debugFlag = True

newDirectory = r"C:\Users\j_mat\AppData\Local\Programs\Python\Python311\Scripts" #r defines a string literal, allowing for easier use of "\" characters
os.chdir(newDirectory)

if debugFlag == True:
    print("\n\n-----------------------------------------------------------------    Running program in debug mode   -----------------------------------------------------------------\n\n")
    print("CWD is: " + os.getcwd())


filePath = "invoiceDetails.txt" 
invoiceNumberFilePath = "invoiceNumber.txt"


# def writeInvoice(invoiceNumber, clientName, address, CSP, billType, receipt):   #creates the appropriate markdown file and exports it to .pdf
#     #CSP = City/State/Postal Code
#     # ----------------------------------------------------------------------------------------------------------------------------------



#     markdown_content = """
#     # Document Title

#     This is a Markdown document with variables.

#     Invoice Number: {invoiceNumber}
#     Name: {clientName}
#     Address: {address}
#     City, Province/State, Postal Code: {CSP}
#     Bill Type: {billType}
#     Receipt: {receipt}                      #this one will likely need to be reformatted from an array into a table. New Function? readReceipt(receipt, lineToRead). How to return multiple values from a function?
#     Variable 2: {variable_2}
#     """

#     # Replace variables with actual values
#     markdown_content = markdown_content.format(variable_1="Value 1", variable_2="Value 2")

#     # Convert Markdown to PDF
#     output_pdf = pypandoc.convert_text(markdown_content, 'pdf', format='md', outputfile='output.pdf')

#     print(f"PDF file created: {output_pdf}")    






#     print("Invoice #" + invoiceNumber + " for " + clientName + " has been generated.\n")
#     return 0

#************************************************************************************************************
#------------------------------------------------------------------------------------------------------------
#************************************************************************************************************

def generateReceipt(orderList):                                                              #returns a 2D array of rows: item/unitPrice/quantity/productPrice
    #orderList is a variable-length collection of rows. Each row contains "/" delimited data. Use str.split("/") to create an array of strings, separated by the delimiter. 
    
    #Strings from the orderList array are of the format: productName / hours: [x] / price (per unit) [y]$

    receipt = [[0 for _ in range(4)] for element in orderList]  #initialize nx4 table to hold: Item Name, unitPrice, Quantity, ProductPrice
    price = ""
    quantity = ""
    
    for index, value in enumerate(orderList):
        itemList = value.split("/")
        for ILelement in itemList:
            ILelement.strip()       #removes leading & trailing whitespace
        for char in itemList[1]:    #data cleaning for QUANTITY
            if char.isnumeric():
                quantity += char
        for char in itemList[2]:    #data cleaning for PRICE
            if char.isnumeric():
                price += char

        productName = itemList[0]
        intQuantity = int(quantity)
        unitPrice = float(price)
        productPrice = unitPrice * intQuantity

        itemSummary = [productName, unitPrice, intQuantity, productPrice]

        for i in range(4):
            receipt[index][i] = itemSummary[i]    #receipt[row][column]

    return receipt

#************************************************************************************************************
#------------------------------------------------------------------------------------------------------------
#************************************************************************************************************

def isEndOfEntry(line):                                                                      #Boolean output. Looks for a line containing only "\n"
    if line.strip(" \t") == "\n":  
        if debugFlag == True:
            print("end of entry! Next line is blank. Identified by isEndOfEntry")
        return True
    else:
        return False

#************************************************************************************************************
#------------------------------------------------------------------------------------------------------------
#************************************************************************************************************
#------------------------------------------------------------------------------------------------------------
#
#                                            Begin Program 
#
#------------------------------------------------------------------------------------------------------------
if debugFlag == True:
    print("start program")
    print("Looking for data in: " + newDirectory + "\\" + filePath)

# Open the file in read mode
with open(filePath, "r") as file:
    if debugFlag == True:
        print("data file opened")
#   Read each line and append it to the list
    allData = file.readlines() #generates a list, with each element of entry corresponding to a line of file

with open(invoiceNumberFilePath, "r") as invoiceNumberFile:
    if debugFlag == True:
        print("number file opened")
#   Read each line and append it to the list
    invoiceNumberFileContent = invoiceNumberFile.readlines() #generates a list, with each element of entry corresponding to a line of file
    invoiceNumber = int(invoiceNumberFileContent[0])


index = 0 
offset = 0
entry = []  #the list of sorted, machine-ready data
orderList = []
clientName = ""

allData.append("\n") #adds an empty row to the end of allData to dodge a bug


if debugFlag == True:
    print("Data gathered. Entering enumeration of allData")

for index, value in enumerate(allData):        
        if debugFlag == True:
            print("In 'enumerate' loop at iteration: " + str(index))

        if(allData[index] == "\n"):
            index += 1
            offset += 1
            if debugFlag == True:
                print(entry)
                print("skipped blank line ------------------------------------------------")
            continue   


        entry.append(allData[index]) 
        if debugFlag == True:
            print("appended to entry")

        if (index < len(allData)):                  #if the program is not looking at the last line of the file
            if debugFlag == True:
                print("Not yet at the last line")
            if isEndOfEntry(allData[index+1]):    #checks the next line for a linebreak. Builds invoice if so.
                if debugFlag == True:
                    print("End of entry")
                clientName = entry[0]
                address = entry [1]
                CSP = entry[2]
                billType = entry[3] 
                for i in range(4, len(entry)): 
                    orderList.append(entry[i])
                receipt = generateReceipt(orderList)

                #writeInvoice(invoiceNumber, clientName, address, CSP, billType, receipt)------------------------------**************************************************
                print("Invoice generated for " + clientName)
                if debugFlag == True:
                    print("Using entry data: " + str(entry))
                invoiceNumber += 1
                if debugFlag == True:   
                    print("updated invoice number: " + str(invoiceNumber))
                offset += len(entry)+1              #adds offset to index, to move on to the next entry. Includes \n character.
                
                entry.clear()
                orderList.clear()
                if debugFlag == True:
                    print("entry cleared! Entry: \n" + str(entry))               

                if debugFlag == True:
                    print("Invoice generated using data:\n")
                    print(receipt)
                    

with open(invoiceNumberFilePath, "w") as invoiceNumberFile:
    if debugFlag == True:
        print("number file opened for updating. Current saved invoice number is: " + str(invoiceNumber))
    invoiceNumberFile.write(str(invoiceNumber))                 
