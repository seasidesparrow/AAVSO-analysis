#!/usr/bin/env python



def make_multipanel_light_curve_all_data():
    import numpy as np
    import pandas as pd
    import aavso

    raw_data=aavso.invalids_delete(
             aavso.aavso_csv_load(infile))

    clean_data=aavso.fainterthans_repair(
               aavso.differentials_delete(
               aavso.nonstandard_filter_delete(
               aavso.steps_delete(raw_data))))

    aavso.multipanel_file(clean_data,7,outf='t_umi_all.png')

    return


def make_multipanel_light_curve_vis_pos():
    import numpy as np
    import pandas as pd
    import aavso

    raw_data=aavso.aavso_csv_load(infile)

    clean_data=aavso.fainterthans_delete(
               aavso.differentials_delete(
               aavso.steps_delete(
               aavso.visual_estimates_only(raw_data))))

    aavso.multipanel_file(clean_data,4,imtype='pdf',outf='t_umi_vis.pdf')

    return


def make_multipanel_light_curve_transformed_phot():
    import numpy as np
    import pandas as pd
    import aavso

    raw_data=aavso.aavso_csv_load(infile)

    clean_data=aavso.fainterthans_delete(
               aavso.differentials_delete(
               aavso.nonstandard_filter_delete(
               aavso.transformed_only(raw_data))))

    aavso.multipanel_file(clean_data,5,outf='t_umi_phot.png')

    return

def main():


#   make a light curve of all useful data
    make_multipanel_light_curve_all_data() 

#   make a light curve of just visual positive estimates
    make_multipanel_light_curve_vis_pos()

#   Make a light curve of just transformed instrumental photometry
    make_multipanel_light_curve_transformed_phot()

    return


if __name__ == '__main__':

    infile='tumi_2450_2458.txt'

    main()
    print "Done with examples.\nThank you for using AAVSO-analysis.\nhttp://github.com/seasidesparrow/AAVSO-analysis."


