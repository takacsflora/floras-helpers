
def off_axes(ax,which='all'):
    """
    plot to turn off certain axes
    Parameters: 
        ax: the matplotlib ax object 
        which: str
            options: 'all','top','exceptx','excepty'
    """
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    offx, offy = False, False
    if which=='all': offx = True 
    if which=='excepty': offx = True 

    if which=='all': offy = True
    if which=='exceptx': offy = True 

    if offx: 
        ax.spines['bottom'].set_visible(False)
        ax.set_xticks([])
        ax.set_xlabel('')

    if offy: 
        ax.spines['left'].set_visible(False)
        ax.set_yticks([])
        ax.set_xlabel('')  