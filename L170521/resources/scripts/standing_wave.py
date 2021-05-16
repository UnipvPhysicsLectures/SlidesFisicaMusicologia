import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.style.use('dark_background')

fig = plt.figure(dpi=300)
ax = fig.add_subplot(1, 1, 1)

# Move left y-axis and bottim x-axis to centre, passing through (0,0)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('center')

# Eliminate upper and right axes
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

# Show ticks in the left and lower axes only
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

# set ticks

ax.yaxis.set_ticklabels([])

# axis labels
ax.set_xlabel('$x$', loc='right')
ax.set_ylabel('$y(x)$', loc='top')

# limiti
ax.set_ylim(-4,4)

x = np.arange(-2*np.pi, 2*np.pi, 0.01)
line1, = ax.plot(x, np.sin(x),'r')
line2, = ax.plot(x, np.sin(x),'b')
line3, = ax.plot(x, np.sin(x) + np.sin(x),'white')
ax.legend(['Onda dx','Onda sx','Onda Stazionaria'])
plt.tight_layout()


def animate(i):
    line1.set_ydata(np.sin(x + 2.0*np.pi*i / 300))  # update the data.
    line2.set_ydata(np.sin(x - 2.0*np.pi*i / 300))  # update the data.
    line3.set_ydata(np.sin(x + 2.0*np.pi*i / 300) + np.sin(x - 2.0*np.pi*i / 300))  # update the data.
    return line1,line2,line3


ani = animation.FuncAnimation(
    fig, animate, interval=20, blit=True, save_count=299)

# To save the animation, use e.g.
ani.save("../standing_wave.mp4")
