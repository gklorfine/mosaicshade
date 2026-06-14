# Adapted from a script I created for a workshop I led:
# https://github.com/gklorfine/Intro-to-Python-Workshop/blob/main/images/logo.py
import matplotlib.pyplot as plt
import matplotlib.patches as patches # For drawing shapes in matplotlib

# Define figure, figure size
plt.figure(figsize = (8, 8))

# Create 'patch' (draw shape)
poly = patches.RegularPolygon(
    (0, 0), # Position (x, y)
    numVertices = 14, 
    radius = 1, 
    facecolor = 'white', edgecolor = "#505050",
    linewidth = 6
)

# Add text
plt.annotate(
    "MosaicShade", (0, .35), ha = "center", va = "center",
    color = "black", 
    fontsize = 54, fontfamily='signpainter'
)

# gcf = 'get current figure'; gca = 'get current axes'
fig = plt.gcf()
ax = fig.gca()

ax.axis('off') # Turn off default matplotlib border

inset_width = 0.3261
axin = ax.inset_axes([(1 - inset_width) / 2, .22, inset_width, inset_width]) # args: [x, y, width, height]

# Draw a compact mosaic using axes-relative coordinates.
margin = 0.04
line_width = 2.1
horizontal_gap = 0.030
vertical_gap = 0.024

x_min, x_max = margin, 1 - margin
y_min, y_max = margin, 1 - margin
plot_width = x_max - x_min
plot_height = y_max - y_min

# Approximate the reference mosaic in normalized coordinates. Each tile is
# transposed below by swapping x/y and width/height. Coordinates describe
# adjoining source regions; a single inset creates equal gaps on every edge.
reference_tiles = [
    # x, y, width, height, face colour, edge colour, line style
    (0.00, 0.86, 0.58, 0.14, "#8080FF", "#0000FF", "-"),
    (0.00, 0.73, 0.58, 0.13, "#FF0000", "#FF0000", (0, (4, 3))),
    (0.58, 0.90, 0.42, 0.10, "#FFFFFF", "#0000FF", "-"),
    (0.58, 0.73, 0.42, 0.17, "#0000FF", "#0000FF", "-"),
    (0.00, 0.57, 0.68, 0.16, "#FFFFFF", "#0000FF", "-"),
    (0.00, 0.40, 0.68, 0.17, "#FFFFFF", "#0000FF", "-"),
    (0.68, 0.61, 0.32, 0.12, "#FF0000", "#FF0000", (0, (4, 3))),
    (0.68, 0.40, 0.32, 0.21, "#0000FF", "#0000FF", "-"),
    (0.00, 0.19, 0.68, 0.21, "#0000FF", "#0000FF", "-"),
    (0.00, 0.00, 0.68, 0.19, "#FF8080", "#FF0000", (0, (4, 3))),
    (0.68, 0.24, 0.32, 0.16, "#FF0000", "#FF0000", (0, (4, 3))),
    (0.68, 0.00, 0.32, 0.24, "#8080FF", "#0000FF", "-"),
]

for source_x, source_y, source_width, source_height, facecolor, edgecolor, linestyle in reference_tiles:
    x = x_min + (source_y + horizontal_gap / 2) * plot_width
    y = y_min + (source_x + vertical_gap / 2) * plot_height
    width = (source_height - horizontal_gap) * plot_width
    height = (source_width - vertical_gap) * plot_height

    axin.add_patch(
        patches.Rectangle(
            (x, y), width, height,
            facecolor=facecolor,
            edgecolor=edgecolor,
            linestyle=linestyle,
            linewidth=line_width,
            capstyle="butt",
            joinstyle="miter",
        )
    )

axin.set_xlim(0, 1)
axin.set_ylim(0, 1)
axin.set_aspect("equal")
axin.axis("off")

# Add 'patch' to figure
ax.add_patch(poly)

# Set figure limits
plt.xlim([-1.15,1.15])
plt.ylim([-1.15,1.15])

# Save figure w/ transparent background
plt.savefig('images/logo.png', dpi = 300, transparent = True, bbox_inches = 'tight', pad_inches = 0.05)

plt.show()
