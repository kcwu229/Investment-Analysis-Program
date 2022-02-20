# Import HTML template & Server
from flask import Flask, render_template, request, send_from_directory
import string

# import function from py file
import codeChecker
import stockTransaction

# file path for delete
import os


''' -------------------------                                         Page 1: Input Field                                          -------------------------   '''

app = Flask(__name__)
# Adding html variables from scraping

# index page
@app.route('/')
def index():
    stockCats = list(string.ascii_uppercase)    
    stockCats.append('All')
    return render_template('index.html', stockCats=stockCats)




''' -------------------------                        Page 2: Download Code | Download Transaction Data                              -------------------------   '''
 

# Retrive the data from the form, with name Parameter
@app.route('/response', methods=['POST'])
def response():  
    
    # If access Code 
    if ((request.form.get('action')) == 'Code'):   
        stockLetter = request.form.get('stockCatResult')
        
        # Call function
        codes = codeChecker.StockChecker(stockLetter)
        fileDir = 'document/StockCode.txt'
        with open(fileDir, 'w') as file:
            for code in codes:
                file.write(f'{code}\n')
                        
        return send_from_directory('document', 'StockCode.txt', as_attachment=True)
    
    
    # If access Transaction data by own code list
    else:
        dataLocation = request.form.get('dataLocation')
        startDate = request.form.get('stockStartDate')
        endDate = request.form.get('stockEndDate')
        
        
        # LOAD & READ OWN CODE LIST
        if (dataLocation == 'upload'):
            codeFile = request.files.get('file')
            codes = []
            if codeFile.filename != '':
                fileDir = f'document/{codeFile.filename}'
                codeFile.save(fileDir) 
                
                with open(fileDir, 'r') as file:
                    for line in file:
                        codes.append(line.strip())
                        
                data = stockTransaction.stockDataGetter(codes, startDate, endDate)
                data.to_csv(f'document/stockList_{endDate}.csv', index=False)
                os.remove(fileDir)
                return send_from_directory('document', f'stockList_{endDate}.csv', as_attachment=True)
        
            else:
                return 'Error'
        
        
        # DOWNLOAD FROM WEB
        else:
            stockLetter = request.form.get('stockCatResult')
            codes = codeChecker.StockChecker(stockLetter)
 
            # Call function
            data = stockTransaction.stockDataGetter(codes, startDate, endDate)
            data.to_csv(f'document/stockList_{endDate}.csv', index=False)

            return send_from_directory('document', f'stockList_{endDate}.csv', as_attachment=True)
        
        
        
''' -------------------------                Page 2: Connect to Mock Transaction API & Plot graphs/ take record            -------------------------   '''

# Activate the Server
if __name__ == '__main__':
    app.run(debug=True)
    
    