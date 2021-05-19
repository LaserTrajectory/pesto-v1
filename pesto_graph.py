import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import scipy.integrate as integrate

st.title("P.E.S.T.O – PyEcon Student Tools, Open Source")

st.subheader("A project by Aniruddh Bhaskaran")

tool_select = st.sidebar.selectbox("Choose a tool", ("Demand and Supply", "Placeholder"))

if tool_select == "Demand and Supply":

    st.header("Demand and Supply Graphing")

    st.write("""We want to start with a simple plotting mechanism, 
            so we will go with the easiest plots in economics - 
            the demand and supply curves.""")

    st.write("""A demand function is given in the form: $Q_{d} = a - bP$.
                A supply function is given in the form: $Q_{s} = c + dP$.""")

    st.write("""To plot a basic demand curve we need values for $a$, $b$, $c$ and $d$.
                In the boxes below, please enter a value for each
                (I've added 0.1 as a minimum value for b
                to avoid a division by 0 error later on). Once you enter
                these values, we can plot the demand and supply curves for you :)""")

    st.write("""We also calculate consumer and producer surplus for you!""")


    a = st.number_input("a = ")

    st.write("a is the y-intercept (or the P-axis intercept) of the demand curve")

    b = st.number_input("b = ", min_value=0.1)

    st.write("b is the absolute value of the slope of the demand curve")

    c = st.number_input("c = ")

    st.write("c is the y-intercept (or the P-axis intercept) of the supply curve")

    d = st.number_input("d = ")

    st.write("d is the absolute value of the slope of the supply curve")

    x = np.arange((a / b) + 1)

    x_half = np.arange(((a / b) + 1) / 2)

    # x_half = list(range(int(np.ceil((a / b) + 1) / 2)))

    x_int = (a - c) / (b + d)

    y_int = a - (b * x_int)

    # st.write("x_int = ", x_int)

    # x_half.append(x_int)

    new_half = np.append(x_half, [x_int])

    # st.write("new_half = ", new_half)

    p_l_domain = np.arange(0)

    x_test = 0

    while x_test < x_int:

        p_l_domain = np.append(p_l_domain, [x_test])

        x_test += 1

    p_l_domain = np.append(p_l_domain, [x_int])

    # st.write(p_l_domain)

    one_arr = np.ones(len(p_l_domain))

    demand_fn = lambda r: a - b*r

    supply_fn = lambda p: c + d*p

    demand_area = integrate.quad(demand_fn, 0, x_int)

    supply_area = integrate.quad(supply_fn, 0, x_int)

    # st.write(total_area[0])

    cs = demand_area[0] - (y_int * x_int)

    ps = (y_int * x_int) - supply_area[0]

    fig = go.Figure(data=go.Line(x=x, y = (a - b*x), name='Demand'))

    # fig = go.Figure()

    fig.update_layout(title='Demand and Supply Graph', width=750, height=500)

    fig.update_yaxes(rangemode="nonnegative", mirror=True, range=[-1, a + 3], 
                    zerolinewidth=2, zerolinecolor='black', 
                    title_text='Price', title_standoff=5, nticks=10, dtick=1)
    fig.update_xaxes(rangemode="nonnegative", mirror=True, range=[-1, ((a / b) + 2)], 
                    zerolinewidth=2, zerolinecolor='black', 
                    title_text='Quantity', nticks=10, dtick=0.5)

    fig.add_trace(go.Line(x=x, y=(c + d*x), name='Supply'))

    # fig.add_trace(go.Line(x=p_l_domain, y=(c + d*(p_l_domain)), name='Supply Half', 
    #               fill='tonext', showlegend=False))

    # fig.add_trace(go.Line(x=p_l_domain, y=(a - b*(p_l_domain)), name='Demand Half', showlegend=False))

    # st.write(x_half)

    # fig.add_trace(go.Line(x=x, y=(one_arr * y_int), name='Price Line', fill='tonextx'))

    # fig.add_trace(go.Line(x=p_l_domain, y=(one_arr * y_int), name='Price Line 2', 
    #               fill='tonextx', fillcolor='turquoise', showlegend=False))

    fig.add_trace(go.Line(x=p_l_domain, y=(one_arr * y_int), name='Price Line 2', 
                  showlegend=False))

    # fig.add_shape(type='line',
    #               x0 = 0, y0 = y_int,
    #               x1 = (a / b) + 1, y1 = y_int,
    #               line=dict(color='black', dash='dash'))

    fig.add_trace(go.Scatter(x=[0, 0, x_int, 0], y=[c, y_int, y_int, c], fill='toself', 
                  name='Producer Surplus = {:.2f}'.format(ps)))

    fig.add_trace(go.Scatter(x=[0, 0, x_int, 0], y=[y_int, a, y_int, y_int], fill='toself', 
                  name='Consumer Surplus = {:.2f}'.format(cs)))

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
                name='P intercept - Demand',
                marker=dict(
                    color='darkgreen',
                    size=10
                )
    ))

    fig.add_trace(go.Scatter(
                mode='markers',
                x=[0],
                y=[c],
                name='P intercept - Supply',
                marker=dict(
                    color='darkred',
                    size=10
                )
    ))


    lim_cs = round(cs, 3)
    lim_ps = round(ps, 3)
    lim_ss = round((cs + ps), 3)

    st.write("Consumer Surplus = ", lim_cs)

    st.write("Producer Surplus = ", lim_ps)

    st.write("Social Surplus = ", lim_ss)

    st.plotly_chart(fig)

    controls = st.checkbox("Toggle price controls")

    if controls:

        pc_select = st.selectbox("Choose a price control to be added to the graph:", 
                                ("Price Ceiling", "Price Floor"))

        if pc_select == "Price Ceiling":

            price_ceil = st.number_input("Enter a value for the price ceiling: ", max_value=y_int,
                        value = y_int - 1, min_value=c)

            st.markdown("""Note: The default value of the price ceiling is set to $P_{eq} - 1$
            to avoid rendering issues. But you can change it to any value lesser than or 
            equal to $P_{eq}$ :) """)

            st.write("""The value of the price ceiling has to be lesser than or equal to the
                        current equilibrium price {:.2f} – otherwise there's no point to having a price 
                        ceiling! It should also be greater than or equal to the price intercept
                        {:.2f} – it can't get any lower than that!""".format(y_int, c))

            long_one_arr = np.ones(len(x))

            pc_fig = go.Figure(data=go.Line(x=x, y = (a - b*x), name='Demand'))

            pc_fig.update_layout(title='Demand and Supply Graph', width=750, height=500)

            pc_fig.update_yaxes(rangemode="nonnegative", mirror=True, range=[-1, a + 3], 
                            zerolinewidth=2, zerolinecolor='black', 
                            title_text='Price', title_standoff=5, nticks=10, dtick=1)
            pc_fig.update_xaxes(rangemode="nonnegative", mirror=True, range=[-1, ((a / b) + 2)], 
                            zerolinewidth=2, zerolinecolor='black', 
                            title_text='Quantity', nticks=10, dtick=0.5)

            pc_fig.add_trace(go.Line(x=x, y=(c + d*x), name='Supply'))

            pc_fig.add_trace(go.Line(x=x, y=(long_one_arr * price_ceil), name='Price Ceiling', 
                  showlegend=True, line=dict(color='black')))

            pc_fig.add_trace(go.Line(x=p_l_domain, y=(one_arr * y_int), name='Price Line 2', 
                  showlegend=False))

            pc_fig.add_trace(go.Scatter(
                mode='markers',
                x=[x_int],
                y=[y_int],
                name='D-S Intercept',
                marker=dict(
                    color='blue',
                    size=10
                )
            ))

            pc_fig.add_trace(go.Scatter(
                mode='markers',
                x=[a / b],
                y=[0],
                name='Q intercept',
                marker=dict(
                    color='green',
                    size=10
                )
            ))

            pc_fig.add_trace(go.Scatter(
                mode='markers',
                x=[0],
                y=[a],
                name='P intercept - Demand',
                marker=dict(
                    color='darkgreen',
                    size=10
                )
            ))

            pc_fig.add_trace(go.Scatter(
                mode='markers',
                x=[0],
                y=[c],
                name='P intercept - Supply',
                marker=dict(
                    color='darkred',
                    size=10
                )
            ))

            new_qs = (price_ceil - c) / d

            # st.write("Quantity supplied after price ceiling = ", new_qs)

            pc_demand_area = integrate.quad(demand_fn, 0, new_qs)

            pc_supply_area = integrate.quad(supply_fn, 0, new_qs)

            dwl_demand_area = integrate.quad(demand_fn, new_qs, x_int)

            dwl_supply_area = integrate.quad(supply_fn, new_qs, x_int)

            dwl_area = dwl_demand_area[0] - dwl_supply_area[0]

            pc_pl_area = new_qs * y_int

            pc_cs = pc_demand_area[0] - pc_pl_area

            pc_ps = pc_pl_area - pc_supply_area[0]

            pc_fig.add_trace(go.Scatter(
                    mode = 'markers',
                    x=[new_qs],
                    y=[price_ceil],
                    name='Producer Price and Quantity',
                    marker=dict(
                        color = 'purple',
                        size = 10
                    )
            ))

            pc_fig.add_trace(go.Scatter(
                    mode = 'markers',
                    x = [new_qs],
                    y = [(a - b*new_qs)],
                    name = "Consumer Price and Quantity",
                    marker = dict(
                        color = 'purple',
                        size = 10
                    )
            ))

            pc_fig.add_trace(go.Scatter(
                    mode = 'markers',
                    x = [new_qs],
                    y = [y_int],
                    name='Marker on Price Line-New_QS intersection',
                    showlegend = False,
                    marker = dict(
                        color = 'purple',
                        size = 10
                    )
            ))

            pc_fig.add_trace(go.Scatter(
                    mode = 'markers',
                    x = [(a - price_ceil) / b],
                    y = [price_ceil],
                    name = 'Marker on Price Ceiling-Demand Curve intersection',
                    showlegend=False,
                    marker=dict(
                        color='purple',
                        size=10
                    )
            ))

            pc_fig.add_trace(go.Scatter(x=[0, 0, new_qs, new_qs, 0], 
            y=[c, y_int, y_int, price_ceil, c], fill='toself', 
            name='Price Ceiling Producer Surplus = {:.2f}'.format(pc_ps)))

            pc_fig.add_trace(go.Scatter(x=[0, 0, new_qs, new_qs, 0], 
            y=[y_int, a, (a - b*new_qs), y_int, y_int], 
            fill='toself', name='Price Ceiling Consumer Surplus = {:.2f}'.format(pc_cs)))

            pc_fig.add_trace(go.Scatter(x=[new_qs, new_qs, x_int, new_qs], 
            y=[price_ceil, (a - b*new_qs), y_int, price_ceil], 
            fill='toself', name='Deadweight Loss = {:.2f}'.format(dwl_area), line_color='gray'))

            pc_fig.add_shape(type="line", 
                          x0=new_qs, y0 = 0, x1 = new_qs, y1 = (a - b*new_qs),
                          line = dict(dash='dash'))
            
            pc_fig.add_shape(type="line", 
                          x0=(a - price_ceil) / b, y0 = 0, x1 = (a - price_ceil) / b, y1 = price_ceil,
                          line = dict(dash='dash'))

            shortage = ((a - price_ceil) / b) - new_qs

            pc_fig.add_trace(go.Scatter(x=[new_qs, (a - price_ceil) / b], y=[price_ceil, price_ceil],
                             line_color='chocolate', name='Shortage = {:.2f}'.format(shortage)))

            pc_fig.update_layout(title='Demand and Supply with Price Ceiling = {}'.format(price_ceil))

            st.plotly_chart(pc_fig)



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

