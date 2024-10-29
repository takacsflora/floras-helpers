import numpy as np
import matplotlib.pyplot as plt
import scipy.signal as signal
from sklearn.cluster import KMeans

from plotting import off_axes
from floras_helpers.numerical import schmitt


def get_move_raster(on_times,camt,camv,pre_time=.1,post_time=1,bin_size=.005,sortPC1=False,sortAmp=False,baseline_subtract=True,ax=None,to_plot=False):
    """
    Function to rasterise behavioral measures (camera/wheel) that are 
    sampled at low frequency and thus need to be interpolated 

    Parameters: 
    -----------
    on_times: list 
        instances of onsets (same scale as camt)
    camt: np.ndarray 
        camera timepoints (same length as camv)
    camv: np.ndarray
        camera values 
    pre_time: float
        time prior to event 
    post_time: float 
        time taken after event for the raster 
    bin_size: float 
    sortPC1: bool
        whether to sort the raster based on how much each trial weighs on PC1, output is descending ?
    sortAmp: bool
        whether to sort the raster based on amplitude of movement after the event (specified by on_times). Output is ascending
    baseline_subtract: bool 
    to_plot: bool 
        can plot the raster output directly 
    ax: matplotlib.pyplot.axis
        can pass down on which axis to plot the raster output (in case of subplot)
    
    
    Returns:
    --------
    raster: np.ndarray
        len(on_times) x time 
    bin_range: np.ndarray
        timepoints at of the raster 
    sort_idx: 
        indices over trials by which raster was sorted 

    todo: 
        return mean/mad and bunch output

    """
    # If requested, input on_times in a sorted fashion
    on_times = on_times[:,np.newaxis]
    bin_range = np.arange(-pre_time,post_time,bin_size)
    zero_bin_idx = np.argmin(np.abs(bin_range))
    raster = np.interp((on_times+bin_range),np.ravel(camt),np.ravel(camv))

    sort_idx = None

    if baseline_subtract: 
        baseline = raster[:,zero_bin_idx][:,np.newaxis]
        baseline = np.tile(baseline,bin_range.size)
        raster = raster - baseline 

    if sortPC1:
        mu,_,_ = np.linalg.svd(raster[zero_bin_idx:,:],full_matrices=False)
        sort_idx = np.argsort(np.abs(mu[:,0]))
        raster = raster[sort_idx,:]

    if sortAmp:
        sort_idx=np.argsort(raster[:,zero_bin_idx:].mean(axis=1))
        raster = raster[sort_idx,:]

    if to_plot:
        if not ax:
            fig,ax = plt.subplots(1,1)
        movement_values = np.median(np.ravel(raster))
        print([movement_values*.65, movement_values*3])
        ax.matshow(np.repeat(raster,repeats=10,axis=0),aspect='auto',cmap='Greys',norm=LogNorm(vmin=movement_values*.65, vmax=movement_values*3))
        #ax.matshow(raster,aspect='auto',cmap=cm.gray_r, norm=LogNorm(vmin=2500, vmax=12500))
        #ax.matshow(raster, cmap=cm.gray_r,aspect='auto')
        #ax.axvline(zero_bin_idx,color = 'r')
        ax.plot(zero_bin_idx,-2,marker='v',markersize=12,color='blue')
        off_axes(ax)

    return raster,bin_range,sort_idx


def digitise_motion_energy(camt,camv,plot_sample=False,min_off_time=.01,min_on_time =.01):
    """
    converts camera motion energy signal to digitised motion on/off
    process: 
        1. lowpass (<10Hz) 7th order Butterworth
        2. kmeans to determine min threshold 
        3. drop periods that don't last min_period time (s)

    Parameters: 
    -----------
    camt: numpy ndarray
    camv: numpy ndarray
    plot_sample: bool
    min_period_time: float64

    Returns: 
    -------
    (on_times,off_times,digitised) : (numpy ndarrays)


    """

    fs = 1/np.diff(camt).mean()
    fc = 10  # frequency cutoff
    w  = fc / (fs/2)
    b,a = signal.butter(7,w,'low')
    camv_filt = signal.filtfilt(b, a, camv)

    k_clus  = KMeans(n_clusters=5).fit(camv[:,np.newaxis])
    # remove clusters with less than 2% points
    keep_idx = [(k_clus.labels_==clusIdx).mean()>.02 for clusIdx in np.unique(k_clus.labels_)]
    # get the center of each of the remainder of the clusters. 
    thresh = k_clus.cluster_centers_[keep_idx,0]
    thresh = np.min(thresh)#+np.ptp(thresh)*0.02 # determine the minimum thershold for crossing
    std_low = np.std(camv_filt[k_clus.labels_==np.argmin(thresh)])
    low_up_thr = np.array([thresh,thresh+std_low])
    # schmitt trigger of the trace
    camv_thr,_ = schmitt(camv,low_up_thr)

    on_times = camt[1:][(camv_thr[:-1]==-1) & (camv_thr[1:]==1)]        
    off_times = camt[1:][(camv_thr[:-1]==1) & (camv_thr[1:]==-1)]

    # previous version was detecting simple thrshold crossings...
    # camv_thr = (camv_filt>thresh).astype('int')
    # df_camv_thr = np.diff(camv_thr)
    # df_camv_thr = np.insert(df_camv_thr,0,df_camv_thr[0])
    # on_times = camt[df_camv_thr>0]
    # off_times = camt[df_camv_thr<0]

    while on_times.size!=off_times.size: 
        # if stating in on state
        if camv_thr[0]>=0: 
            on_times = np.insert(on_times,0,camt[0])
        elif camv_thr[-1]>0: 
            off_times = np.insert(off_times,0,camt[-1])
        else: 
            print('more on off differences than expected...') 
            break



    # getting rid of too short on-periods
    is_sel =(off_times-on_times)>min_off_time
    on_times, off_times = on_times[is_sel],off_times[is_sel]
    # also getting rid of too short off periods
    is_sel =(on_times[1:]-off_times[:-1])>min_on_time

    if is_sel.size>0:
        on_times, off_times = on_times[np.insert(is_sel,0,True)],off_times[np.insert(is_sel,-1,True)]

    # digitis e the signal
    digitised = np.concatenate([((camt>=on) & (camt<=off))[:,np.newaxis] for on,off in zip(on_times,off_times)],axis=1)
    digitised  = np.sum(digitised,axis=1)

    if plot_sample: 
        st = 2500
        en = 10500
        _,ax = plt.subplots(1,1,figsize=(20,5))
        plt.plot(camt[st:en],camv[st:en])
        plt.plot(camt[st:en],camv_filt[st:en])
        #plt.plot(camt[st:en],camv_thr[st:en])
        plt.plot(camt[st:en],digitised[st:en]*np.max(k_clus.cluster_centers_)*1.1)

    return (on_times,off_times,digitised)

