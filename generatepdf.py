from fpdf import FPDF, HTMLMixin

# Dummy class needed to generate the PDF file
class MyFPDF(FPDF, HTMLMixin): pass

def generatepdf(pdffile, obsT, nCore, nRemote, nInt, nChan, nSb, integT, 
                antSet, pipeType, tAvg, fAvg, isDysco, imNoiseVal, rawSize, 
                procSize, pipeTime, isMsgBoxOpen):
   """Function to generate a pdf file summarizing the content of the calculator.
       Return nothing."""   
   # Create an A4 sheet
   pdf = MyFPDF('P', 'mm', 'A4')
   pdf.add_page()
   pdf.set_font('Arial', '', 16)
   
   # Generate an html string to be written to the file
   string  = '<table border="0" align="left" width="80%">'
   string += '<thead><tr><th width="70%" align="left">Parameter</th>'
   string += '<th width="30%" align="left">Value</th></tr></thead>'
   string += '<tbody>'
   string += '<tr><td>Observation time (in seconds)</td>'
   string += '    <td>{}</td></tr>'.format(obsT)
   string += '<tr><td>No. of stations</td>'
   string += '    <td>({}, {}, {})</td></tr>'.format(nCore, nRemote, nInt)
   string += '<tr><td>No. of subbands</td>'
   string += '    <td>{}</td></tr>'.format(nSb)
   string += '<tr><td>No. of channels per subband</td>'
   string += '    <td>{}</td></tr>'.format(nChan)
   string += '<tr><td>Integration time (in seconds)</td>'
   string += '    <td>{}</td></tr>'.format(integT)
   if antSet == 'enable':
      mode = 'HBA'
   else:
      mode = 'LBA'
   string += '<tr><td>Antenna set</td>'
   string += '    <td>{}</td></tr>'.format(mode)
   string += '<tr></tr>'
   string += '<tr><td>Pipeline type</td>'
   if pipeType == 'none':
      string += '    <td>{}</td></tr>'.format('None')
   else:
      string += '    <td>{}</td></tr>'.format('Preprocessing')
      string += '<tr><td>Averaging factor (time, freq)</td>'
      string += '    <td>{}, {}</td></tr>'.format(tAvg, fAvg)
      string += '<tr><td>Dysco compression</td>'
      if isDysco == 'enable':
         string += '    <td>{}</td></tr>'.format('enabled')
      else:
         string += '    <td>{}</td></tr>'.format('disabled')
   string += '<tr></tr>'
   string += '<tr><td>Theoretical image sensitivity (uJy/beam)</td>'
   string += '    <td>{}</td></tr>'.format(imNoiseVal)
   string += '<tr><td>Raw data size (in GB)</td>'
   string += '    <td>{}</td></tr>'.format(rawSize)
   if pipeType != 'none':
      string += '<tr><td>Processed data size (in GB)</td>'
      string += '    <td>{}</td></tr>'.format(procSize)
      string += '<tr><td>Pipeline processing time (in hours)</td>'
      string += '    <td>{}</td></tr>'.format(pipeTime)
   string += '</tbody>'
   string += '</table>'
   
   # Write text to the pdf file
   pdf.write_html(string)
   
   # Write the pdf to disk
   pdf.output(pdffile)
