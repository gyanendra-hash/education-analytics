"""
Main dashboard application using Dash and Plotly
"""

import dash
from dash import dcc, html, Input, Output, callback
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import dash_bootstrap_components as dbc
from app.services.analytics_service import AnalyticsService
from app.db.database import SessionLocal


def create_dashboard_app():
    """Create and configure the main dashboard application"""
    
    # Initialize Dash app with Bootstrap theme
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True
    )
    
    # Define the layout
    app.layout = dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.H1("Education Analytics Dashboard", className="text-center mb-4"),
                html.P("Real-time insights on student performance and institutional KPIs", 
                      className="text-center text-muted mb-4")
            ])
        ]),
        
        # Navigation tabs
        dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(label="Overview", tab_id="overview"),
                    dbc.Tab(label="Student Performance", tab_id="performance"),
                    dbc.Tab(label="Enrollment Analytics", tab_id="enrollment"),
                    dbc.Tab(label="Course Analytics", tab_id="courses"),
                    dbc.Tab(label="Institutional KPIs", tab_id="kpis")
                ], id="main-tabs", active_tab="overview")
            ])
        ], className="mb-4"),
        
        # Tab content
        html.Div(id="tab-content"),
        
        # Store for data
        dcc.Store(id="dashboard-data")
        
    ], fluid=True)
    
    # Callback for tab content
    @app.callback(
        Output("tab-content", "children"),
        Input("main-tabs", "active_tab")
    )
    def render_tab_content(active_tab):
        """Render content based on active tab"""
        if active_tab == "overview":
            return create_overview_tab()
        elif active_tab == "performance":
            return create_performance_tab()
        elif active_tab == "enrollment":
            return create_enrollment_tab()
        elif active_tab == "courses":
            return create_courses_tab()
        elif active_tab == "kpis":
            return create_kpis_tab()
        else:
            return html.Div("Select a tab to view content")
    
    return app


def create_overview_tab():
    """Create overview dashboard tab"""
    return dbc.Container([
        # Key metrics row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Students", className="card-title"),
                        html.H2("2,847", className="text-primary"),
                        html.P("+5.2% from last month", className="text-success small")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Active Courses", className="card-title"),
                        html.H2("156", className="text-primary"),
                        html.P("+12 new this semester", className="text-success small")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Average GPA", className="card-title"),
                        html.H2("3.24", className="text-primary"),
                        html.P("+0.08 from last semester", className="text-success small")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Retention Rate", className="card-title"),
                        html.H2("87.3%", className="text-primary"),
                        html.P("+2.1% from last year", className="text-success small")
                    ])
                ], className="text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Charts row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Student Performance Trends"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="performance-trend-chart",
                            figure=create_performance_trend_chart()
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Enrollment by Department"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="enrollment-department-chart",
                            figure=create_enrollment_department_chart()
                        )
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Additional charts row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Grade Distribution"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="grade-distribution-chart",
                            figure=create_grade_distribution_chart()
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Course Completion Rates"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="completion-rates-chart",
                            figure=create_completion_rates_chart()
                        )
                    ])
                ])
            ], width=6)
        ])
    ])


def create_performance_tab():
    """Create student performance analytics tab"""
    return dbc.Container([
        # Filters
        dbc.Row([
            dbc.Col([
                dbc.Label("Select Department:"),
                dcc.Dropdown(
                    id="department-filter",
                    options=[
                        {"label": "Computer Science", "value": "cs"},
                        {"label": "Mathematics", "value": "math"},
                        {"label": "Physics", "value": "physics"},
                        {"label": "All Departments", "value": "all"}
                    ],
                    value="all"
                )
            ], width=3),
            dbc.Col([
                dbc.Label("Select Time Period:"),
                dcc.Dropdown(
                    id="time-period-filter",
                    options=[
                        {"label": "Last 6 Months", "value": "6m"},
                        {"label": "Last Year", "value": "1y"},
                        {"label": "Last 2 Years", "value": "2y"},
                        {"label": "All Time", "value": "all"}
                    ],
                    value="1y"
                )
            ], width=3)
        ], className="mb-4"),
        
        # Performance charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("GPA Distribution"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="gpa-distribution-chart",
                            figure=create_gpa_distribution_chart()
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Performance by Course Level"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="performance-level-chart",
                            figure=create_performance_level_chart()
                        )
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Detailed performance analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Student Performance Heatmap"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="performance-heatmap",
                            figure=create_performance_heatmap()
                        )
                    ])
                ])
            ], width=12)
        ])
    ])


def create_enrollment_tab():
    """Create enrollment analytics tab"""
    return dbc.Container([
        # Enrollment metrics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("New Enrollments", className="card-title"),
                        html.H2("342", className="text-primary"),
                        html.P("This semester", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Graduations", className="card-title"),
                        html.H2("287", className="text-success"),
                        html.P("This semester", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Retention Rate", className="card-title"),
                        html.H2("87.3%", className="text-info"),
                        html.P("Year-over-year", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Drop Rate", className="card-title"),
                        html.H2("12.7%", className="text-warning"),
                        html.P("This semester", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Enrollment charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Enrollment Trends Over Time"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="enrollment-trends-chart",
                            figure=create_enrollment_trends_chart()
                        )
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Enrollment by Program"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="enrollment-program-chart",
                            figure=create_enrollment_program_chart()
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Student Demographics"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="demographics-chart",
                            figure=create_demographics_chart()
                        )
                    ])
                ])
            ], width=6)
        ])
    ])


def create_courses_tab():
    """Create course analytics tab"""
    return dbc.Container([
        # Course metrics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Courses", className="card-title"),
                        html.H2("156", className="text-primary"),
                        html.P("Active this semester", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Average Class Size", className="card-title"),
                        html.H2("28", className="text-info"),
                        html.P("Students per course", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Completion Rate", className="card-title"),
                        html.H2("89.2%", className="text-success"),
                        html.P("Course completion", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Pass Rate", className="card-title"),
                        html.H2("78.5%", className="text-warning"),
                        html.P("Students passing", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3)
        ], className="mb-4"),
        
        # Course performance charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Top Performing Courses"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="top-courses-chart",
                            figure=create_top_courses_chart()
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Course Difficulty Analysis"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="course-difficulty-chart",
                            figure=create_course_difficulty_chart()
                        )
                    ])
                ])
            ], width=6)
        ], className="mb-4"),
        
        # Course details table
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Course Performance Details"),
                    dbc.CardBody([
                        html.Div(id="course-details-table")
                    ])
                ])
            ], width=12)
        ])
    ])


def create_kpis_tab():
    """Create institutional KPIs tab"""
    return dbc.Container([
        # KPI metrics
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Student Satisfaction", className="card-title"),
                        html.H2("4.2/5", className="text-success"),
                        html.P("Based on surveys", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Faculty Ratio", className="card-title"),
                        html.H2("15:1", className="text-info"),
                        html.P("Student to faculty", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Budget Utilization", className="card-title"),
                        html.H2("87.3%", className="text-warning"),
                        html.P("Annual budget used", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Graduation Rate", className="card-title"),
                        html.H2("78.5%", className="text-primary"),
                        html.P("4-year graduation", className="text-muted")
                    ])
                ], className="text-center")
            ], width=3)
        ], className="mb-4"),
        
        # KPI charts
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("KPI Trends Over Time"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="kpi-trends-chart",
                            figure=create_kpi_trends_chart()
                        )
                    ])
                ])
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Department Performance Comparison"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="department-comparison-chart",
                            figure=create_department_comparison_chart()
                        )
                    ])
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Resource Allocation"),
                    dbc.CardBody([
                        dcc.Graph(
                            id="resource-allocation-chart",
                            figure=create_resource_allocation_chart()
                        )
                    ])
                ])
            ], width=6)
        ])
    ])


# Chart creation functions
def create_performance_trend_chart():
    """Create performance trend chart"""
    # Sample data - in real implementation, this would come from the database
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
    gpa = [3.1, 3.2, 3.3, 3.25, 3.4, 3.35]
    enrollments = [1200, 1250, 1180, 1300, 1280, 1350]
    
    fig = go.Figure()
    
    # Add GPA line
    fig.add_trace(go.Scatter(
        x=months, y=gpa,
        mode='lines+markers',
        name='Average GPA',
        yaxis='y',
        line=dict(color='blue', width=3)
    ))
    
    # Add enrollment line
    fig.add_trace(go.Scatter(
        x=months, y=enrollments,
        mode='lines+markers',
        name='Enrollments',
        yaxis='y2',
        line=dict(color='green', width=3)
    ))
    
    fig.update_layout(
        title="Student Performance and Enrollment Trends",
        xaxis_title="Month",
        yaxis=dict(title="GPA", side="left"),
        yaxis2=dict(title="Enrollments", side="right", overlaying="y"),
        hovermode='x unified'
    )
    
    return fig


def create_enrollment_department_chart():
    """Create enrollment by department chart"""
    departments = ['Computer Science', 'Mathematics', 'Physics', 'Chemistry', 'Biology']
    enrollments = [450, 320, 280, 250, 200]
    
    fig = px.pie(
        values=enrollments,
        names=departments,
        title="Enrollment Distribution by Department"
    )
    
    return fig


def create_grade_distribution_chart():
    """Create grade distribution chart"""
    grades = ['A', 'B', 'C', 'D', 'F']
    counts = [450, 680, 420, 180, 95]
    
    fig = px.bar(
        x=grades, y=counts,
        title="Grade Distribution",
        color=grades,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    
    fig.update_layout(
        xaxis_title="Grade",
        yaxis_title="Number of Students"
    )
    
    return fig


def create_completion_rates_chart():
    """Create course completion rates chart"""
    courses = ['CS101', 'MATH201', 'PHYS301', 'CHEM401', 'BIO501']
    completion_rates = [92, 88, 85, 90, 87]
    
    fig = px.bar(
        x=courses, y=completion_rates,
        title="Course Completion Rates (%)",
        color=completion_rates,
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        xaxis_title="Course",
        yaxis_title="Completion Rate (%)"
    )
    
    return fig


def create_gpa_distribution_chart():
    """Create GPA distribution histogram"""
    import numpy as np
    
    # Generate sample GPA data
    np.random.seed(42)
    gpa_data = np.random.normal(3.2, 0.5, 1000)
    gpa_data = np.clip(gpa_data, 0, 4.0)  # Clip to valid GPA range
    
    fig = px.histogram(
        x=gpa_data,
        nbins=20,
        title="GPA Distribution",
        labels={'x': 'GPA', 'y': 'Number of Students'}
    )
    
    fig.update_layout(
        xaxis_title="GPA",
        yaxis_title="Number of Students"
    )
    
    return fig


def create_performance_level_chart():
    """Create performance by course level chart"""
    levels = ['100-level', '200-level', '300-level', '400-level']
    avg_gpa = [3.4, 3.2, 3.1, 3.0]
    
    fig = px.bar(
        x=levels, y=avg_gpa,
        title="Average GPA by Course Level",
        color=avg_gpa,
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        xaxis_title="Course Level",
        yaxis_title="Average GPA"
    )
    
    return fig


def create_performance_heatmap():
    """Create student performance heatmap"""
    import numpy as np
    
    # Generate sample data
    students = [f'Student {i}' for i in range(1, 21)]
    courses = [f'Course {i}' for i in range(1, 11)]
    
    # Generate random performance data
    np.random.seed(42)
    performance_data = np.random.uniform(2.0, 4.0, (20, 10))
    
    fig = px.imshow(
        performance_data,
        x=courses,
        y=students,
        color_continuous_scale='RdYlGn',
        title="Student Performance Heatmap (GPA by Course)"
    )
    
    fig.update_layout(
        xaxis_title="Courses",
        yaxis_title="Students"
    )
    
    return fig


def create_enrollment_trends_chart():
    """Create enrollment trends over time"""
    months = ['Jan 2023', 'Feb 2023', 'Mar 2023', 'Apr 2023', 'May 2023', 'Jun 2023']
    new_enrollments = [120, 135, 110, 140, 125, 130]
    graduations = [85, 90, 75, 95, 80, 88]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=new_enrollments,
        mode='lines+markers',
        name='New Enrollments',
        line=dict(color='blue', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=graduations,
        mode='lines+markers',
        name='Graduations',
        line=dict(color='green', width=3)
    ))
    
    fig.update_layout(
        title="Enrollment and Graduation Trends",
        xaxis_title="Month",
        yaxis_title="Number of Students",
        hovermode='x unified'
    )
    
    return fig


def create_enrollment_program_chart():
    """Create enrollment by program chart"""
    programs = ['Bachelor', 'Master', 'PhD', 'Certificate']
    enrollments = [1200, 800, 200, 150]
    
    fig = px.bar(
        x=programs, y=enrollments,
        title="Enrollment by Program Type",
        color=programs,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_layout(
        xaxis_title="Program Type",
        yaxis_title="Number of Students"
    )
    
    return fig


def create_demographics_chart():
    """Create student demographics chart"""
    categories = ['Male', 'Female', 'Other', 'International', 'Domestic']
    percentages = [45, 50, 5, 25, 75]
    
    fig = px.pie(
        values=percentages,
        names=categories,
        title="Student Demographics"
    )
    
    return fig


def create_top_courses_chart():
    """Create top performing courses chart"""
    courses = ['CS101', 'MATH201', 'PHYS301', 'CHEM401', 'BIO501']
    avg_scores = [92, 88, 85, 90, 87]
    
    fig = px.bar(
        x=avg_scores, y=courses,
        orientation='h',
        title="Top Performing Courses (Average Score)",
        color=avg_scores,
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        xaxis_title="Average Score",
        yaxis_title="Course"
    )
    
    return fig


def create_course_difficulty_chart():
    """Create course difficulty analysis chart"""
    courses = ['CS101', 'MATH201', 'PHYS301', 'CHEM401', 'BIO501']
    difficulty = [2.5, 3.8, 4.2, 3.5, 3.0]  # 1-5 scale
    pass_rate = [95, 78, 65, 82, 88]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=difficulty, y=pass_rate,
        mode='markers+text',
        text=courses,
        textposition="top center",
        marker=dict(size=15, color=pass_rate, colorscale='RdYlGn'),
        name='Courses'
    ))
    
    fig.update_layout(
        title="Course Difficulty vs Pass Rate",
        xaxis_title="Difficulty (1-5 scale)",
        yaxis_title="Pass Rate (%)"
    )
    
    return fig


def create_kpi_trends_chart():
    """Create KPI trends over time"""
    months = ['Q1 2023', 'Q2 2023', 'Q3 2023', 'Q4 2023']
    satisfaction = [4.0, 4.1, 4.2, 4.2]
    graduation_rate = [75, 77, 78, 78.5]
    retention_rate = [85, 86, 87, 87.3]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=months, y=satisfaction,
        mode='lines+markers',
        name='Student Satisfaction',
        yaxis='y',
        line=dict(color='blue', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=graduation_rate,
        mode='lines+markers',
        name='Graduation Rate (%)',
        yaxis='y2',
        line=dict(color='green', width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=months, y=retention_rate,
        mode='lines+markers',
        name='Retention Rate (%)',
        yaxis='y2',
        line=dict(color='orange', width=3)
    ))
    
    fig.update_layout(
        title="Key Performance Indicators Over Time",
        xaxis_title="Quarter",
        yaxis=dict(title="Satisfaction Score", side="left"),
        yaxis2=dict(title="Rate (%)", side="right", overlaying="y"),
        hovermode='x unified'
    )
    
    return fig


def create_department_comparison_chart():
    """Create department performance comparison chart"""
    departments = ['CS', 'Math', 'Physics', 'Chemistry', 'Biology']
    gpa = [3.4, 3.2, 3.1, 3.3, 3.0]
    satisfaction = [4.3, 4.1, 3.9, 4.2, 3.8]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=gpa, y=satisfaction,
        mode='markers+text',
        text=departments,
        textposition="top center",
        marker=dict(size=20, color=gpa, colorscale='Viridis'),
        name='Departments'
    ))
    
    fig.update_layout(
        title="Department Performance Comparison",
        xaxis_title="Average GPA",
        yaxis_title="Student Satisfaction"
    )
    
    return fig


def create_resource_allocation_chart():
    """Create resource allocation chart"""
    categories = ['Faculty', 'Infrastructure', 'Research', 'Student Services', 'Administration']
    percentages = [40, 25, 15, 12, 8]
    
    fig = px.pie(
        values=percentages,
        names=categories,
        title="Resource Allocation by Category"
    )
    
    return fig
