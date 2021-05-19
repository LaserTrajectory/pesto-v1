import streamlit as st
from bokeh.plotting import ColumnDataSource, figure, output_file, show
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

st.title("PyEcon – a simple tool for simple economics")

tool_select = st.sidebar.selectbox("Choose a tool", ("PyEcon Graphing Tool", "Placeholder"))

if tool_select == "PyEcon Graphing Tool":

    st.header("Demand and Supply Graphing")

    st.write("""We want to start with a simple plotting mechanism, 
            so we will go with the easiest plots in economics - 
            the demand and supply curves.""")

    st.write("""A demand function is given in the form: $Q_{d} = a - bP$.
                A supply function is given in the form: $Q_{s} = c + dP$""")

    st.write("""To plot a basic demand curve we need values for $a$, $b$, $c$ and $d$.
                In the boxes below, please enter a value for each
                (I've added 0.1 as a minimum value for b
                to avoid a division by 0 error later on). Once you enter
                these values, we can plot the demand curve for you :)""")


    a = st.number_input("a = ")

    b = st.number_input("b = ", min_value=0.1)

    c = st.number_input("c = ")

    d = st.number_input("d = ")

    x = np.arange((a / b) + 1)

    fig = go.Figure(data=go.Line(x=x, y = (a - b*x), name='Demand'))

    fig.update_layout(width=750, height=500)

    fig.update_yaxes(rangemode="nonnegative", mirror=True, range=[-1, a + 3], 
                    zerolinewidth=2, zerolinecolor='black', 
                    title_text='Price', title_standoff=5, nticks=10, dtick=1)
    fig.update_xaxes(rangemode="nonnegative", mirror=True, range=[-1, ((a / b) + 2)], 
                    zerolinewidth=2, zerolinecolor='black', 
                    title_text='Quantity', nticks=10, dtick=0.5)

    fig.add_trace(go.Line(x=x, y=(c + d*x), name='Supply'))

    x_int = (a - c) / (b + d)

    y_int = a - (b * x_int)

    fig.add_trace(go.Scatter(
                mode='markers',
                x=[x_int],
                y=[y_int],
                name='D-S Intercept',
                marker=dict(
                    color='blue',
                    size=10
                )
    ))

    fig.add_trace(go.Scatter(
                mode='markers',
                x=[a / b],
                y=[0],
                name='Q intercept',
                marker=dict(
                    color='green',
                    size=10
                )

    ))

    fig.add_trace(go.Scatter(
                mode='markers',
                x=[0],
                y=[a],
                name='P intercept',
                marker=dict(
                    color='red',
                    size=10
                )
    ))

    st.plotly_chart(fig)

if tool_select == "Placeholder":

    st.write("Placeholder for now :)")


# Legacy Code 

# st.text("We want to start with a simple plotting mechanism, so we")
# st.text("will go with the easiest plot in economics - the demand curve.")

# st.text("A demand function is given in the form: ")

# st.markdown("$Q_{d} = a - bP$")

# st.text("To plot a basic demand curve we need values for a and b.")

# st.text("In the boxes below, please enter a value for $a$ and a value for $b$ so that")
# st.text("we can plot the demand curve for you :)")

# x = np.linspace(0, 10, 100)
# y = a - (b * x)

# TOOLTIPS = [
#     ("(x, y)", "($x, $y)"),
# ]

# p = figure(
#     title = 'demand curve (hopefully lol)',
#     x_axis_label = 'quantity demanded',
#     y_axis_label = 'price',
#     tooltips=TOOLTIPS)

# p.line(x, y, legend_label='Demand trend')

# st.bokeh_chart(p, use_container_width=True)

