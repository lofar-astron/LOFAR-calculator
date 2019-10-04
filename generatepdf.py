from fpdf import FPDF

def generatepdf(pdffile, obsT, nCore, nRemote, nInt, nChan, nSb, integT, 
                antSet, pipeType, tAvg, fAvg, isDysco, imNoiseVal, rawSize, 
                procSize, pipeTime, isMsgBoxOpen):
   """Function to generate a pdf file summarizing the content of the calculator.
       Return nothing."""   
   # Create an A4 sheet
   pdf = FPDF('P', 'mm', 'A4')
   pdf.add_page()
   pdf.set_font('Arial', '', 16)
   
   # Generate string to be written to the file
   string  = 'Observation time (in seconds): \t {}\n'.format(obsT)
   string += 'No. of stations: \t\t\t ({}, {}, {})\n'.format(nCore, nRemote, nInt)
   string += 'No. of subbands:\t {}\n'.format(nSb)
   string += 'No. of channels per subband:\t {}\n'.format(nChan)
   string += 'Correlator integration time:\t {}\n'.format(integT)
   if antSet == 'enable':
      mode = 'HBA'
   else:
      mode = 'LBA'
   string += 'Antenna set:\t {}\n'.format(mode)
   string += '\n'
   if pipeType == 'none':
      string += 'Pipeline type:\t None\n'
   else:
      string += 'Pipeline type:\t Preprocessing\n'
      string += 'Averaging factor (time, freq):\t {}, {}\n'.format(tAvg, fAvg)
      if isDysco == 'enable':
         mode = 'enabled'
      else:
         mode = 'disabled'
      string += 'Dysco compression:\t {}\n'.format(mode)
   string += '\n'
   string += 'Theoretical image sensitivity (uJy/beam): \t {}\n'.format(imNoiseVal)
   string += 'Raw data size (in GB):\t {}\n'.format(rawSize)
   if pipeType != 'none':
      string += 'Processed data size (in GB):\t {}\n'.format(procSize)
      string += 'Pipeline processing time (in hours):\t {}\n'.format(pipeTime)
   
   # Write text to the pdf file
   pdf.write(7, txt=string)
   
   # Write the pdf to disk
   pdf.output(pdffile)
