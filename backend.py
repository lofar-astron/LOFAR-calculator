def compute_baselines(nCore, nRemote, nInt, hbaMode):
   """For a given number of core, remote, and international stations
      and the HBA mode, compute the number of baselines formed by 
      the array. The number of baselines includes autocorrelations."""
   if hbaMode == 'enable':
      nStations = (2*nCore)+nRemote+nInt
   else:
      nStations = nCore+nRemote+nInt
   return (nStations*(nStations+1))/2

def calculate_raw_size(obsT, intTime, nBaselines, nChan, nSB):
   """Compute the datasize of a raw LOFAR measurement set given the 
      length of the observation, correlator integration time, number 
      of baselines, number of channels per subband, and number of subbands"""
   nRows = int( nBaselines * (obsT / intTime) ) - nBaselines
   # A single row in LofarStMan format contains 
   #    - 32-bit sequence number (4 bytes)
   #    - nChan*16-bit samples for weight and sigma calculation (2*nChan bytes)
   #    - 4*nChan*2*float data array (4*nChan*2*4 bytes)
   sbSize = nRows * ((4) + (2*nChan) + (4*nChan*2*4))/(1024*1024*1024) # in GB
   totSize = sbSize * nSB
   return totSize

def calculate_avg_size(obsT, intTime, nBaselines, nChan, nSB, pipeType, tAvg, 
                       fAvg, dyCompress):
   """Compute the datasize of averaged LOFAR measurement set given the
      length of the observation, integration time, number of baselines,
      pipeline type, time and frequency averaging factor, and
      enable dysco compression."""
   if pipeType == 'none':
      return ''
   elif pipeType == 'preprocessing':
      # Change nChan to account for fAvg
      nChan //= fAvg
      # Change integT to account for tAvg
      intTime *= tAvg
      nRows = int( nBaselines * (obsT / intTime) ) - nBaselines
      # What does a single row in an averaged MS contain?
      sbSize = nRows * ((7*8) + \
                        (4+(4*nChan)) + \
                        (4*11) + \
                        (8*1) + \
                        (4) + \
                        (4 * (8 + 8*nChan + 4*nChan)) )
      # Convert byte length to GB
      sbSize /= (1024*1024*1024)
      totSize = sbSize * nSB
      return totSize
   else:
      pass

def validate_inputs(obsT, nSB, integT, tAvg, fAvg):
   """Valid text input supplied by the user: observation time, number of 
      subbands, and integration time. Following checks will be performed:
         - obsTime is a valid positive number
         - nSB is an integer and is at least 1 or greater
         - integT is a valid positive number
         - tAvg is an integer
         - fAvg is an integer
      Return state=True/False accompanied by an error msg
      Note: all input parameters are still strings."""
   msg = ''
   # Validate the length of the observing time
   try:
      float(obsT)
      if not float(obsT) > 0:
         msg += 'Observation time cannot be zero or negative.\n'
   except ValueError:
      msg += 'Invalid observation time specified.\n'
   # Validate the number of subbands
   try:
      int(nSB)
      if int(nSB) < 1:
         msg += 'Number of subbands cannot be less than 1.\n'
   except ValueError:
      msg += 'Invalid number of subbands specified.\n'
   # Validate integration time
   try:
      float(integT)
      if float(integT) <= 0.:
         msg += 'Invalid integration time specified.\n'
   except:
      msg += 'Invalid integration time specified.\n'
   # Validate time averaging factor
   try:
      int(str(tAvg))
   except ValueError:
      msg += 'Invalid time averaging factor specified.'
   # Validate frequency averaging factor
   try:
      int(str(fAvg))
   except ValueError:
      msg += 'Invalid frequency averaging factor specified.'
   # If any error has been triggered above, return the error message
   if msg is not '':
      return False, msg
   else:
      return True, msg
