from datetime import datetime, timedelta
from fpdf import FPDF, HTMLMixin
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import os

# Dummy class needed to generate the PDF file
class MyFPDF(FPDF, HTMLMixin): pass

def convertFigureToAxisInfo(figure):
   """For a given Graph Figure object, return
      xaxis (a list of datetime.datetime objects), 
      yaxis (a list of source elevation), and 
      label (name of the source as a string)."""
   time_axis = figure['x']
   xaxis = []
   for val in time_axis:
      d = datetime.strptime(val, '%Y-%m-%dT%H:%M:%S')
      xaxis.append( d )
   yaxis = figure['y']
   label = figure['name']
   return xaxis, yaxis, label

def makePdfPlot(elevation_fig, outfilename):
   """For a given elevation_fig object and output filename, generate a 
      matplotlib plot and write it to disk."""
   fig, ax = plt.subplots(1, 1, figsize=(8,5))
   for figure in elevation_fig['data']:
      xaxis, yaxis,label = convertFigureToAxisInfo(figure)
      ax.plot(xaxis, yaxis, label=label)
   hour_loc = (0, 3, 6, 9, 12, 15, 18, 21)
   ax.xaxis.set_major_locator(mdates.HourLocator(hour_loc))
   ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
   plt.xlabel('Time (UTC)')
   plt.ylabel('Elevation (deg)')
   plt.title('Target visibility plot')
   
   if len(elevation_fig['data']) > 1:
      ax.legend()
   plt.tight_layout()
   plt.savefig(outfilename, dpi=100)

def generatepdf(pdffile, obsT, nCore, nRemote, nInt, nChan, nSb, integT, 
                antSet, pipeType, tAvg, fAvg, isDysco, imNoiseVal, rawSize, 
                procSize, pipeTime, elevation_fig, distance_table, isMsgBoxOpen):
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
   string += '<tr><td>Antenna set</td>'
   string += '    <td>{}</td></tr>'.format(antSet)
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
   
   # Generate a matplotlib plot showing the same plot as in the target 
   # visibility plot
   if elevation_fig != {}:
      # User has specified at least one source in the target setup
      pngfilename = pdffile.replace('summary', 'plot').replace('pdf', 'png')
      makePdfPlot(elevation_fig, pngfilename)
      # Add the elevation plot to html
      string += '<center>'
      string += '<img src={} width=400 height=250>'.format(pngfilename)
      string += '</center>'
   
   # Add the distance table to the PDF
   if distance_table != {}:
      title = distance_table['layout']['title']
      string += '<center><b>{}</b></center>'.format(title)
      string += '<table border="0" align="left" width="80%">'
      col_titles = distance_table['data'][0]['header']['values']
      col_width = 100//len(col_titles)
      string += '<thead><tr>'
      for item in col_titles:
         string += '<th width="{}%" align="left">'.format(col_width) + item + '</th>'
      string += '</tr></thead>'
      string += '<tbody>'
      row_titles = distance_table['data'][0]['cells']['values'][0]
      tab_data   = distance_table['data'][0]['cells']['values']
      # Transpose tab_data and write cells to the table
      tab_data = list(map(list, zip(*tab_data)))
      for row in tab_data:
         string += '<tr>'
         for item in row:
            string += '<td>{}</td>'.format(item)
         string += '</tr>'
      string += '</tbody>'
      string += '</table>'

   # Write text to the pdf file
   pdf.write_html(string)
   
   # Write the pdf to disk
   pdf.output(pdffile)
   
   # Remove the temporary PNG file from disk
   if elevation_fig != {}:
      os.remove(pngfilename)
