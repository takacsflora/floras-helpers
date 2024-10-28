from io import StringIO
import pyperclip

def off_axes(ax, which="all"):
    """
    plot to turn off certain axes
    Parameters:
        ax: the matplotlib ax object
        which: str
            options: 'all','top','exceptx','excepty'
    """
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    offx, offy = False, False
    if which == "all":
        offx = True
    if which == "excepty":
        offx = True

    if which == "all":
        offy = True
    if which == "exceptx":
        offy = True

    if offx:
        ax.spines["bottom"].set_visible(False)
        ax.set_xticks([])
        ax.set_xlabel("")

    if offy:
        ax.spines["left"].set_visible(False)
        ax.set_yticks([])
        ax.set_xlabel("")


def copy_svg_to_clipboard(fig):
    """
    function that can directly grab a matplotlib figure and copy to clipboard as an SVG.
    you just need to put the fig object into the argument!

    """

    # Step 2: Save the figure as an SVG string
    svg_io = StringIO()
    fig.savefig(svg_io, format="svg")
    # plt.close(fig)  # Close the plot so it doesn't display twice

    # Step 3: Get the SVG content as a string
    svg_code = svg_io.getvalue()

    # Step 4: Copy the SVG string to the clipboard
    pyperclip.copy(svg_code)

    print("SVG content copied to clipboard!")

