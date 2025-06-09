import numpy as np

class anatomy_plotter():
    """
    plotter to plot units on top of slice boundaries

    """
    def __init__(self): 
        from .hist.atlas import AllenAtlas
        self.atlas = AllenAtlas(25)

    def plot_anat_canvas(self,ax,coord,axis='dv'):
        
        # just need some realistic numbers so that the ccf2xyz conversion works
        fake_dv = 3000
        fake_ap = 8000
        fake_ml = 7300

        self.axis = axis 
        self.ax = ax

        # get the coordinate in xyz system
        if self.axis=='dv':
            coord = coord + 332
            xyz_ref = self.atlas.ccf2xyz(np.array([fake_ap,coord,fake_ml]),ccf_order='apdvml')
            self.atlas.plot_hslice(xyz_ref[2],volume='boundary',ax=ax,aspect='auto')
        elif self.axis=='ap':
            coord = coord + 5400 # we can receive the coord relative to breagma 
            xyz_ref = self.atlas.ccf2xyz(np.array([coord,fake_dv,fake_ml]),ccf_order='apdvml')
            self.atlas.plot_cslice(xyz_ref[1],volume='boundary',ax=ax,aspect='auto')
        elif self.axis== 'ml':
            coord = coord + 5739 # we can receive the coord relative to breagma 
            xyz_ref = self.atlas.ccf2xyz(np.array([fake_ap,fake_dv,coord]),ccf_order='apdvml')
            self.atlas.plot_sslice(xyz_ref[0],volume='boundary',ax=ax,aspect='auto')


    def plot_points(self,x,y,unilateral=False,**plot_kwargs):
        """x,y in apdvml coordinates relative to bregma ??  according to IBL 
            ALLEN_CCF_LANDMARKS_MLAPDV_UM = [5739, 5400,  332] """
        
        if self.axis=='dv':
            if unilateral:
                hemi = np.sign(x-5739)
                x = (x-5739)*hemi + 5739             
            x_ = -x + 5739 # ml coordinate 
            y_ = -y + 5400 # ap coordinate 
        elif self.axis == 'ap':
            if unilateral:
                hemi = np.sign(x-5739)
                x = (x-5739)*hemi + 5739
            x_ = -x + 5739 # ml coordinate 
            y_ = -y + 332 # dv coordinate 
        elif self.axis=='ml':
            x_ = -x + 5400 # ap coordinate
            y_ = -y + 332 #dv coordinate
        self.ax.scatter(x_,y_,**plot_kwargs)