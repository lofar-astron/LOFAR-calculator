"""Functions to validate user-input"""

import numpy as np
from astropy.coordinates import SkyCoord

def compute_baselines(n_core, n_remote, n_int, hba_mode):
    """For a given number of core, remote, and international stations
       and the HBA mode, compute the number of baselines formed by
       the array. The number of baselines includes autocorrelations."""
    if 'hba' in hba_mode:
        n_stations = (2*n_core)+n_remote+n_int
    else:
        n_stations = n_core+n_remote+n_int
    return (n_stations*(n_stations+1))/2

def calculate_im_noise(n_core, n_remote, n_int, hba_mode, obs_t, n_sb):
    """Calculate the image sensitivity for a given number of stations, HBA/LBA mode,
       observation time, and number of subbands."""
    # Hardcoded value for subband width
    sb_width = 195.3125 # kHz

    # Hardcoded values for station SEFD
    core_sefd = {'lba' : 38160, 'hba' : 2820}
    remote_sefd = {'lba' : 38160, 'hba' : 1410}
    int_sefd = {'lba' : 18840, 'hba' : 710}

    # Figure out whether the user wants to observe with LBA or HBA.
    if 'hba' in hba_mode:
        mode = 'hba'
        n_core *= 2
    else:
        mode = 'lba'

    # Calculate the bandwidth in MHz
    bandwidth = n_sb * sb_width * 1.E3
    bandwidth /= 1.E6

    # Calculate the sensitivity
    prodcc = core_sefd[mode]
    if hba_mode == 'hbadualinner':
        # SEFD of the tapered remote station is the same as a core station
        prodrr = core_sefd[mode]
    else:
        prodrr = remote_sefd[mode]
    prodii = int_sefd[mode]
    prodcr = np.sqrt(prodcc) * np.sqrt(prodrr)
    prodci = np.sqrt(prodcc) * np.sqrt(prodii)
    prodri = np.sqrt(prodrr) * np.sqrt(prodii)
    nccbl = n_core*(n_core-1)/2
    nrrbl = n_remote*(n_remote-1)/2
    niibl = n_int*(n_int-1)/2
    ncrbl = n_core * n_remote
    ncibl = n_core * n_int
    nribl = n_remote * n_int
    denom = 4 * bandwidth * obs_t * 1.E6 * \
                ((nccbl/prodcc**2) + (nrrbl/prodrr**2) + \
                 (niibl/prodii**2) + (ncrbl/prodcr**2) + \
                 (ncibl/prodci**2) + (nribl/prodri**2))
    im_noise = 1/np.sqrt(denom)
    im_noise *= 1.E6 # In uJy
    return '{:0.2f}'.format(im_noise)

def calculate_raw_size(obs_t, int_time, n_baselines, n_chan, n_sb):
    """Compute the datasize of a raw LOFAR measurement set given the
       length of the observation, correlator integration time, number
       of baselines, number of channels per subband, and number of subbands"""
    n_rows = int(n_baselines * (obs_t / int_time)) - n_baselines
    # A single row in LofarStMan format contains
    #    - 32-bit sequence number (4 bytes)
    #    - n_chan*16-bit samples for weight and sigma calculation (2*n_chan bytes)
    #    - 4*n_chan*2*float data array (4*n_chan*2*4 bytes)
    sb_size = n_rows * ((4) + (2*n_chan) + (4*n_chan*2*4))/(1024*1024*1024) # in GB
    tot_size = sb_size * n_sb
    return '{:0.2f}'.format(tot_size)

def calculate_proc_size(obs_t, int_time, n_baselines, n_chan, n_sb, pipe_type,
                        t_avg, f_avg, dy_compress):
    """Compute the datasize of averaged LOFAR measurement set given the
       length of the observation, integration time, number of baselines,
       pipeline type, time and frequency averaging factor, and
       enable dysco compression."""
    if pipe_type == 'none':
        return ''
    elif pipe_type == 'preprocessing':
        # Change n_chan to account for f_avg
        n_chan //= f_avg
        # Change integ_t to account for t_avg
        int_time *= t_avg
        n_rows = int(n_baselines * (obs_t / int_time)) - n_baselines
        # What does a single row in an averaged MS contain?
        sb_size = n_rows * ((7*8) + \
                         (4+(4*n_chan)) + \
                         (4*11) + \
                         (8*1) + \
                         (4) + \
                         (4 * (8 + 8*n_chan + 4*n_chan)))
        # Convert byte length to GB
        sb_size /= (1024*1024*1024)
        tot_size = sb_size * n_sb
        # Reduce the data size if dysco is enabled.
        if dy_compress == 'enable':
            tot_size = tot_size/3.
        return '{:0.2f}'.format(tot_size)

def calculate_pipe_time(obs_t, n_sb, array_mode, ateam_names, pipe_type):
    """Compute the pipeline processing time.
       Inputs:
           obs_t - Observation time in hours
           n_sb  - Number of subbands
           ateam_names - List of A-team sources to demix
           pipe_type - Name of the pipeline
       Returns pipeline processing time in hours"""
    proc_time = 0
    # Figure out the number of ateam sources specified
    if ateam_names is None:
        n_ateams = 0
    else:
        n_ateams = len(ateam_names)

    # Hard-coded P/O factors for 1 SB. Empirically determined.
    hba_factor = {0:0.002, 1:0.0025, 2:0.005}
    lba_factor = {0:0.004, 1:0.004, 2:0.014}

    if pipe_type == 'preprocessing':
        if 'hba' in array_mode:
            proc_time = hba_factor[n_ateams] * n_sb * obs_t
        else:
            proc_time = lba_factor[n_ateams] * n_sb * obs_t
    # Convert to hours
    proc_time /= 3600.
    return proc_time

def validate_inputs(obs_t, n_core, n_remote, n_int, n_sb, integ_t, t_avg,
                    f_avg, src_name, coord, hba_mode, pipe_type, ateam_names):
    """Valid text input supplied by the user: observation time, number of
       subbands, and integration time. Following checks will be performed:
         - obs_time is a valid positive number
         - n_core is not None
         - n_remote is not None
         - n_int is not None
         - n_core+n_remote+n_int is at least 1
         - n_sb is an integer and is at least 1 or greater
         - integ_t is a valid positive number greater than or equal to 0.16
         - t_avg is an integer
         - f_avg is an integer
         - src_name is a string
         - coord is a valid AstroPy coordinate
         - While observing with HBA, check if the targets are inside the tile beam.
         - ateam_names <= 2 if pipe_type is not "None"
       Return state=True/False accompanied by an error msg
       Note: all input parameters are still strings."""
    msg = ''
    # Validate the length of the observing time
    try:
        float(obs_t)
        if float(obs_t) <= 0:
            msg += 'Observation time cannot be zero or negative.\n'
    except ValueError:
        msg += 'Invalid observation time specified.\n'
    # Validate the number of stations
    if n_core < 0 or n_core > 24:
        msg += 'Number of core stations must be between 0 and 24.\n'
    if n_remote < 0 or n_remote > 14:
        msg += 'Number of remote stations must be between 0 and 14.\n'
    if n_int < 0 or n_int > 14:
        msg += 'Number of international stations must be between 0 and 14.\n'
    if n_core + n_remote + n_int < 2:
        msg += 'At least 2 station must be included.\n'
    # Validate the number of subbands
    try:
        int(n_sb)
        if int(n_sb) < 1:
            msg += 'Number of subbands cannot be less than 1.\n'
        if int(n_sb) > 488:
            msg += 'Number of subbands cannot be larger than 488.\n'
    except ValueError:
        msg += 'Invalid number of subbands specified.\n'
    # Validate integration time
    try:
        float(integ_t)
        if float(integ_t) < 0.16:
            msg += 'Invalid integration time specified. Must be >= 0.16\n'
    except:
        msg += 'Invalid integration time specified.\n'
    # Validate time averaging factor
    try:
        int(str(t_avg))
    except ValueError:
        msg += 'Invalid time averaging factor specified.'
    # Validate frequency averaging factor
    try:
        int(str(f_avg))
    except ValueError:
        msg += 'Invalid frequency averaging factor specified.'
    # Validate the number of A-team sources if a pipeline is specified
    # Figure out the number of ateam sources specified
    if ateam_names is None:
        n_ateams = 0
    else:
        n_ateams = len(ateam_names)
    if pipe_type != 'none' and n_ateams > 2:
        msg += 'Cannot demix more than two A-team sources.'
    # Validate the coordinates specified under target setup
    if coord is not '':
        # Warn if the number of targets do not match the number of coordinates
        if len(src_name.split(',')) != len(coord.split(',')):
            msg += 'Number of target names do not match the number of coordinates. '
        # Check if the coordinates are valid
        try:
            for i in range(len(coord.split(','))):
                SkyCoord(coord.split(',')[i])
        except:
            msg += 'Invalid coodinate value under Target setup. Please make ' +\
                   'sure it is compatible with the AstroPy formats.'
    # While observing with HBA, check if the specified targets all lie within 10 deg
    coord_list = coord.split(',')
    if 'hba' in hba_mode and len(coord_list) > 1:
        ref_point = SkyCoord(coord_list[0])
        ang_distance = []
        for i in range(1, len(coord_list)):
            this_point = SkyCoord(coord_list[i])
            ang_distance.append(this_point.separation(ref_point).deg)
        max_distance = np.max(np.asarray(ang_distance))
        if max_distance > 10.:
            msg += 'Maximum angular separation between specified target ' + \
                   'pointings is {:.2f} degrees. This is '.format(max_distance) + \
                   'not allowed while observing with the High Band Antenna'
    # If any error has been triggered above, return the error message
    if msg is not '':
        return False, msg
    else:
        return True, msg
