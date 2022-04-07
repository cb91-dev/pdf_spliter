from PDFlib import PDFlib
import uuid
import json

input_file = 'input/Site00_PartF_01.pdf'
tempFile = '/pvf/tempFile'

p = PDFlib()

with open(input_file, 'rb') as f:
	data = f.read()

# Load the document from the event object that is a string
p.create_pvf(tempFile,data,'')

# Dump the data variable to save memory
data = None

# open the doc
indoc = p.open_pdi_document(tempFile, 'shrug=true inmemory=true')
if (indoc == -1):
	# Rejected: File is not a PDF or cannot be read
	msg = "Error opening pdi document: {0}\n".format(p.get_errmsg())
	print(msg)
	raise ValueError(msg)

endpage = int(p.pcos_get_number(indoc, "length:pages"))

# Loop over all pages of the input document
itemdata = []
for pageno in range(1, endpage + 1, 1):
	# Create new document
	if (p.begin_document("", "") == -1):
		# Rejected: Problem creating a blank PDF. Internal issue
		msg = f'Error creating blank PDF: {p.get_errmsg()}'
		print(msg)
		raise ValueError(msg)

	# Set the output variable to empty to ensure it doesn't contain the previous PDF batch
	output = ''

	# Dummy page size; will be adjusted later
	p.begin_page_ext(10, 10, "")

	page = p.open_pdi_page(indoc, pageno, "")
	if (page == -1):
		# Rejected: File is not a PDF or cannot be read
		msg = "ERROR: Could not read pages within this PDF"
		print(msg)
		raise ValueError(msg)

	# Place the imported page on the output page, and
	# adjust the page size

	p.fit_pdi_page(page, 0, 0, "adjustpage")
	p.close_pdi_page(page)

	p.end_page_ext("")

	# End the document now that the loop has finished
	p.end_document("")

	# The UUID for this file will be a combo of the receivedUUID-pageno
	newUUID = uuid.uuid4().hex

	# create newKey for new file
	newKey = f'output/{newUUID}-{str(pageno)}.pdf'

	# Get the PDF page from buffer
	output = p.get_buffer()
	size = len(output)

	# get the region data and process rules
	# TODO:

	# write the file to s3
	# with open(newKey, 'wb') as f:
	# 	f.write(output)

	print(f'Page={pageno}')

	# Clear output variable
	output = None


# Clean up and remove objects
p.close_pdi_document(indoc)
p.delete_pvf(tempFile)
p.delete()


print('done')