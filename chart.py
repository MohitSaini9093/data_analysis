import pandas as pd
import plotly as px
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
import plotly.subplots as sp

class Charts:
    def __init__(self, data):
        self.data = data

    def create_bar_chart(self, x, y, title):
        fig = px.bar(self.data, x=x, y=y, title=title)
        return fig

    def create_line_chart(self, x, y, title):
        fig = px.line(self.data, x=x, y=y, title=title)
        return fig

    def create_scatter_plot(self, x, y, title):
        fig = px.scatter(self.data, x=x, y=y, title=title)
        return fig

    def create_histogram(self, x, title):
        fig = px.histogram(self.data, x=x, title=title)
        return fig