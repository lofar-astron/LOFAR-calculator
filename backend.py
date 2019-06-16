def compute_baselines(nCore, nRemote, nInt, hbaMode):
   """For a given number of core, remote, and international stations
      and the HBA mode, compute the number of baselines formed by 
      the array. The number of baselines includes autocorrelations."""
   if hbaMode == 'enable':
      nStations = (2*nCore)+nRemote+nInt
   else:
      nStations = nCore+nRemote+nInt
   return (nStations*(nStations-1))/2 + nStations

def calculate_raw_size(obsT, intTime, nBaselines, nChan, nSB):
   """Compute the datasize of a raw LOFAR measurement set given the 
      length of the observation, correlator integration time, number 
      of baselines, number of channels per subband, and number of subbands"""
   nRows = int( nBaselines * (obsT / intTime) )
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
      return 0
   elif pipeType == 'preprocessing':
      # Change nChan to account for fAvg
      nChan //= fAvg
      # Change integT to account for tAvg
      intTime *= tAvg
      nRows = int( nBaselines * (obsT / intTime) )
      # What does a single row in an averaged MS contain?
      return 0
   else:
      pass

def validate_inputs(obsT, nSB, integT):
   """Valid text input supplied by the user: observation time, number of 
      subbands, and integration time. Following checks will be performed:
         - obsTime is a valid positive number
         - nSB is an integer and is at least 1 or greater
         - integT is a valid positive number
      Return state=True/False accompanied by an error msg
      Note: all input parameters are still strings."""
   # Check if observation time is a valid number
   try:
      float(obsT)
   except ValueError:
      return False, 'Invalid observation time specified.'
   # Check if observation time is positive
   if not float(obsT) > 0:
      return False, 'Observation time cannot be zero or negative.'
   # Check if the number of subbands is a valid number
   try:
      int(nSB)
   except ValueError:
      return False, 'Invalid number of subbands specified.'
   # Check if the number of subband is greater than or equal to 1
   if int(nSB) < 1:
      return False, 'Number of subbands cannot be less than 1.'
   # Check if integration time is a number
   try:
      float(integT)
   except:
      return False, 'Invalid integration time specified.'
   # Check if integration time is greater than 0
   if float(integT) <= 0.:
      return False, 'Invalid integration time specified.'
   # If all checks pass, return True
   return True, None
