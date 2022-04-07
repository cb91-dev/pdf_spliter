from pdfminer.layout import LAParams, LTTextBox
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator

input_file = 'input/Site00_PartF_01.pdf'
tempFile = '/pvf/tempFile'


# opening doc to be read
fp = open(input_file, 'rb')
rsrcmgr = PDFResourceManager()
laparams = LAParams()
device = PDFPageAggregator(rsrcmgr, laparams=laparams)
interpreter = PDFPageInterpreter(rsrcmgr, device)
pages = PDFPage.get_pages(fp)


result = []
for page in pages:
    # new page starting helper
    # print('Processing next page...')
    interpreter.process_page(page)
    layout = device.get_result()
    # looping of layout 
    for lobj in layout:
        if isinstance(lobj, LTTextBox):
            text = lobj.bbox[0], lobj.bbox[3], lobj.get_text()
            #split tuple sample
            test = (0.0, 839.7991, 'SPLIT HERE\n')
            if text == test:
                print(1)
            else:
                print(2)

                
                
                
                
                

        

