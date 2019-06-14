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
