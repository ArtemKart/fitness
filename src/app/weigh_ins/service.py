import plotly.express as px
import plotly.graph_objects as go


async def get_history_weighs_plot(points: list) -> go.Figure:
    weigh_data_dict = {
        "weighs": [row[0] for row in points],
        "dates": sorted([str(row[1].date()) for row in points]),
    }
    return px.line(
        points,
        x=weigh_data_dict["dates"],
        y=weigh_data_dict["weighs"],
        width=700,
        height=700,
    )
