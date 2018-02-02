#!/usr/bin/env python



def make_multipanel_light_curve_all_data():
    import numpy as np
    import pandas as pd
    import aavso.aavso as aa

    raw_data=aa.invalids_delete(
             aa.aavso_csv_load(infile))

    clean_data=aa.fainterthans_repair(
               aa.differentials_delete(
               aa.nonstandard_filter_delete(
               aa.steps_delete(raw_data))))

    aa.multipanel_file(clean_data,7,outf='test_data.png')

    return


def make_multipanel_light_curve_vis_pos():
    import numpy as np
    import pandas as pd
    import aavso.aavso as aa

    raw_data=aa.invalids_delete(
             aa.aavso_csv_load(infile))

    clean_data=aa.fainterthans_delete(
               aa.differentials_delete(
               aa.steps_delete(
               aa.visual_estimates_only(raw_data))))


    aa.multipanel_file(clean_data,4,imtype='png',outf='test_data_vis.png')

    return


def make_multipanel_light_curve_transformed_phot():
    import numpy as np
    import pandas as pd
    import aavso.aavso as aa

    raw_data=aa.invalids_delete(
             aa.aavso_csv_load(infile))

    clean_data=aa.fainterthans_delete(
               aa.differentials_delete(
               aa.nonstandard_filter_delete(
               aa.transformed_only(raw_data))))

    aa.multipanel_file(clean_data,5,outf='test_data_phot.png')

    return


def perform_LS_periodogram():
#   Note: Lomb-Scargle is not my favorite for AAVSO data, but just
#   as an example....
    import numpy as np
    import pandas as pd
    import aavso.aavso as aa
    from scipy.signal import lombscargle as ls
    import matplotlib.pyplot as plt

    raw_data=aa.invalids_delete(
             aa.aavso_csv_load(infile))

    clean_data=aa.fainterthans_delete(
               aa.differentials_delete(
               aa.steps_delete(
               aa.visual_estimates_only(raw_data))))

    midpoint_jd=aa.midpoint_get(clean_data)

    (star_jd,star_magn)=aa.extract_timeseries(clean_data)

    star_jd=star_jd-midpoint_jd

    jd_span=max(star_jd)-min(star_jd)
#   freq_min=2./jd_span
    freq_min=1./600.
    freq_max=1./100.
    n_freq=freq_max*jd_span*16

    test_freqs=np.linspace(freq_min,freq_max,n_freq)
    ls_statistic=ls(star_jd,star_magn,test_freqs)
    plt.plot(test_freqs,ls_statistic)
    plt.show()

    print("number of test frequencies: %d"%len(ls_statistic))

    imax=np.where(ls_statistic==max(ls_statistic))
    print("max freq: %s\tmax stat: %s"%(test_freqs[imax],ls_statistic[imax]))
    print("strongest period:%f"%(1./(test_freqs[imax])))
    print("Done perform_LS_periodogram!\n\n")

    return



def perform_wavelet_analysis():
    import numpy as np
    import pandas as pd
    import aavso.aavso as aa
    from scipy import signal
    import matplotlib.pyplot as plt

    raw_data=aa.invalids_delete(
             aa.aavso_csv_load(infile))

    clean_data=aa.fainterthans_delete(
               aa.differentials_delete(
               aa.steps_delete(
               aa.visual_estimates_only(raw_data))))

    midpoint_jd=aa.midpoint_get(clean_data)

    (star_jd,star_magn)=aa.extract_timeseries(clean_data)

    star_jd=star_jd-midpoint_jd

# Make a wavelet noise here

    widths=np.arange(1,50)
    cwtmatr=signal.cwt(star_magn,signal.ricker,widths)
    plt.imshow(cwtmatr,extent=[min(star_jd),max(star_jd),1,50],cmap='gist_earth_r',aspect='auto',vmax=abs(cwtmatr).max(),vmin=-abs(cwtmatr).max())
    plt.show()

    return




def main():


#   make a light curve of all useful data
    make_multipanel_light_curve_all_data() 

#   make a light curve of just visual positive estimates
    make_multipanel_light_curve_vis_pos()

#   Make a light curve of just transformed instrumental photometry
    make_multipanel_light_curve_transformed_phot()

#   Perform a Lomb-Scargle periodogram analysis
#   Note: Assumes you have scipy installed
#   perform_LS_periodogram()

#   Perform a Wavelet analysis
#   Note: Assumes you have scipy installed
#   perform_wavelet_analysis()

    return


if __name__ == '__main__':

    infile='test_data.txt'

    main()
    print("Done with examples.\nThank you for using AAVSO-analysis.\nhttp://github.com/seasidesparrow/AAVSO-analysis.\n\n")


