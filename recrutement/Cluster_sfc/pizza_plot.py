import matplotlib.pyplot as plt
from highlight_text import fig_text
from mplsoccer import PyPizza, FontManager

font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))

# parameter and values list
# The values are taken from the excellent fbref website (supplied by StatsBomb)
params = [
    "xG", "Shots", "Dispossessed", "Turnovers", "Deep Progressions", "Carries",
    "Dribbles", "Successful Dribbles", "Touches In Box", "Successful Crosses",
    "PintoB", "Key Passes", "xG Assisted", "Assists", "Aerial Wins",
    "Passes Inside Box"
]
#values = [40,39,57,57,44,45,54,47,39,43,41,44,40,40,56,40 ]    #  risky 
#values = [34,39,46,32,58,64,54,51,36,70,62,70,65,62,43,62] # scoring chance
#values = [40,51,70,51,68,70,77,75,41,61,55,60,55,45,46,56] # Dribblers
#values = [59, 56, 37, 53, 33, 32,38,34,51,39,39,43,43,41,68,38] target man 
#values = [68,70,54,47,50,50,58,53,75,55,55,60,66,60,53,56]#finishr
values = [46,63,51,44,77,81,73,69,64,80,85,83,87,80,43,87]
values_2 = [47,53,53,48,55,57,59,55,51,58,56,60,60,55,52,57]  # median

params_offset = [
    False, False, True, False, True, False,
    True, True, True, False, True, False, True, True, False, True
]
# instantiate PyPizza class
baker = PyPizza(
    params=params,                  # list of parameters
    background_color="#EBEBE9",     # background color
    straight_line_color="#222222",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    last_circle_color="#222222",    # color of last circle
    other_circle_ls="-.",           # linestyle for other circles
    other_circle_lw=1               # linewidth for other circles
)

# plot pizza
fig, ax = baker.make_pizza(
    values,                     # list of values
    compare_values=values_2,    # comparison values
    figsize=(8, 8),             # adjust figsize according to your need
    kwargs_slices=dict(
        facecolor="#870E26", edgecolor="#222222",
        zorder=2, linewidth=1
    ),                          # values to be used when plotting slices
    kwargs_compare=dict(
        facecolor="black", edgecolor="#222222",
        zorder=2, linewidth=1,
    ),
    kwargs_params=dict(
        color="#000000", fontsize=10,
        fontproperties=font_normal.prop, va="center"
    ),                          # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=8,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="white",
            boxstyle="round,pad=0.2", lw=1
        )
    ),                          # values to be used when adding parameter-values labels
    kwargs_compare_values=dict(
        color="#000000", fontsize=8, fontproperties=font_normal.prop, zorder=3,
        bbox=dict(edgecolor="#000000", facecolor="white", boxstyle="round,pad=0.2", lw=1)
    ),                          # values to be used when adding parameter-values labels
)

# adjust text for comparison-values-text
baker.adjust_texts(params_offset, offset=-0.17, adj_comp_values=True)
# add title
fig_text(
    0.515, 0.99, "<Finisher> vs <mean Offensive>", size=17, fig=fig,
    highlight_textprops=[{"color": '#870E26'}, {"color": 'black'}],
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

# add subtitle
fig.text(
    0.515, 0.942,
    "Season 2020-21",
    size=15,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)
plt.show()
