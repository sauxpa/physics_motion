import numpy as np
import pandas as pd
from particle import Particle

from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import Slider, Tabs, TextInput
from bokeh.layouts import row, WidgetBox
from bokeh.plotting import figure


def extract_numeric_input(s: str) -> int:
    try:
        int(s)
        return int(s)
    except:  # noqa
        try:
            float(s)
            return float(s)
        except:  # noqa
            raise Exception('{:s} must be numeric.'.format(s))


def make_dataset(mass,
                 mass_attractive_center,
                 exponent,
                 n_steps_ode,
                 T,
                 r0,
                 drdt0,
                 theta0,
                 dthetadt0,
                 ):
    """Creates a ColumnDataSource object with data to plot.
    """
    p = Particle(
        mass=mass,
        mass_attractive_center=mass_attractive_center,
        exponent=exponent,
        n_steps_ode=n_steps_ode,
    )

    t, traj = p.motion(r0, drdt0, theta0, dthetadt0, T)
    r, drdt, theta = traj
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    df = pd.DataFrame(
        {
            't': t,
            'x': x,
            'y': y
        }).set_index('t')

    df0 = pd.DataFrame(columns=['t0', 'x0', 'y0'])
    df0['t0'] = [0.0]
    df0['x0'] = [x[0]]
    df0['y0'] = [y[0]]
    df0 = df0.set_index('t0')

    # Convert dataframe to column data source
    return ColumnDataSource(df), ColumnDataSource(df0)


def make_plot(src, src0):
    """Create a figure object to host the plot.
    """
    # Blank plot with correct labels
    fig = figure(plot_width=700,
                 plot_height=700,
                 title='Particle motion',
                 )

    # original function
    fig.line('x',
             'y',
             source=src,
             color='blue',
             line_color='blue',
             legend='Trajectory',
             )

    fig.circle(x='x0',
               y='y0',
               source=src0,
               size=12,
               color='red',
               legend='Initial position'
               )

    fig.legend.click_policy = 'hide'
    fig.legend.location = 'bottom_right'
    return fig


def update(attr, old, new):
    """Update ColumnDataSource object.
    """
    # Create new ColumnDataSource
    new_src, new_src0 = make_dataset(
        extract_numeric_input(mass_select.value),
        extract_numeric_input(mass_attractive_center_select.value),
        extract_numeric_input(exponent_select.value),
        extract_numeric_input(n_steps_ode_select.value),
        extract_numeric_input(T_select.value),
        extract_numeric_input(r0_select.value),
        extract_numeric_input(drdt0_select.value),
        extract_numeric_input(theta0_select.value),
        extract_numeric_input(dthetadt0_select.value),
        )

    # Update the data on the plot
    src.data.update(new_src.data)
    src0.data.update(new_src0.data)


mass_select = TextInput(value='1.00', title='Particle mass')
mass_attractive_center_select = TextInput(value='1.00',
                                          title='Attractive center mass'
                                          )
exponent_select = TextInput(value='-2.00', title='Central force exponent')

n_steps_ode_select = TextInput(value='1000', title='Number of ODE steps')
T_select = Slider(start=0.0,
                  end=1000.0,
                  step=1.0,
                  value=10.0,
                  title='T'
                  )

r0_select = TextInput(value='1.00', title='r0')
drdt0_select = TextInput(value='0.00', title='dr/dt_0')
theta0_select = TextInput(value='0.00', title='theta0')
dthetadt0_select = TextInput(value='1.00', title='dtheta/dt_0')

# Update the plot when yields are changed
mass_select.on_change('value', update)
mass_attractive_center_select.on_change('value', update)
mass_attractive_center_select.on_change('value', update)
exponent_select.on_change('value', update)

n_steps_ode_select.on_change('value', update)
T_select.on_change('value', update)

r0_select.on_change('value', update)
drdt0_select.on_change('value', update)
theta0_select.on_change('value', update)
dthetadt0_select.on_change('value', update)

src, src0 = make_dataset(
    extract_numeric_input(mass_select.value),
    extract_numeric_input(mass_attractive_center_select.value),
    extract_numeric_input(exponent_select.value),
    extract_numeric_input(n_steps_ode_select.value),
    extract_numeric_input(T_select.value),
    extract_numeric_input(r0_select.value),
    extract_numeric_input(drdt0_select.value),
    extract_numeric_input(theta0_select.value),
    extract_numeric_input(dthetadt0_select.value),
)

fig = make_plot(src, src0)

controls = WidgetBox(
    mass_select,
    mass_attractive_center_select,
    exponent_select,
    n_steps_ode_select,
    T_select,
    r0_select,
    drdt0_select,
    theta0_select,
    dthetadt0_select,
    width=150,
    height=700,
)

# Create a row layout
layout = row(controls, fig)

# Make a tab with the layout
tab = Panel(child=layout, title='Central force motion')

# ALL TABS TOGETHER
tabs = Tabs(tabs=[tab])

curdoc().add_root(tabs)
