import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import webbrowser
import threading
import time
import os

class ZestMoneyAnalytics:
    def __init__(self):
        self.initialize_data()
        self.setup_styling()
        
    def initialize_data(self):
        # Financial Performance Data
        self.financial_data = {
            'year': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'revenue_cr': [8.2, 26.7, 72.4, 89.3, 138.4, 243.7, 320.0],
            'loss_cr': [15.2, 45.0, 78.0, 125.8, 398.8, 412.4, 485.0],
            'expenses_cr': [23.4, 71.7, 150.4, 215.1, 543.8, 662.2, 805.0],
            'growth_rate': [0, 225.6, 171.2, 23.3, 55.0, 76.0, 31.3],
            'burn_multiple': [2.85, 2.68, 2.08, 2.41, 3.93, 2.72, 2.52],
            'gross_margin': [28.5, 12.5, 18.7, 22.1, 15.3, 8.9, 12.5],
            'marketing_expenses': [0, 0, 28.5, 48.2, 125.0, 165.0, 220.0],
            'employee_costs': [0, 0, 32.4, 52.8, 93.3, 130.4, 165.0],
            'bad_debt_provisions': [0, 0, 38.2, 78.5, 198.5, 142.8, 195.0]
        }
        
        # Operational Data
        self.operational_data = {
            'year': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
            'users_millions': [0.5, 1.2, 3.0, 6.0, 12.0, 17.0, 17.0],
            'active_users_millions': [0.2, 0.5, 1.2, 2.8, 6.5, 8.5, 6.8],
            'merchants': [50, 200, 1000, 3000, 7500, 10000, 12000],
            'npa_rate': [2.5, 3.5, 4.2, 5.0, 6.5, 6.8, 7.2],
            'industry_npa': [1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
            'churn_rate': [15, 18, 20, 25, 30, 35, 40],
            'nps_score': [65, 70, 75, 70, 65, 60, 55],
            'app_rating': [4.2, 4.1, 3.9, 3.7, 3.4, 3.1, 2.9]
        }
        
        # Strategic Opportunities
        self.opportunities = {
            'name': ['B2B Credit Infrastructure', 'SME Lending Platform', 'Credit Scoring APIs', 'RegTech Solutions', 'Open Banking APIs', 'AI Risk Management'],
            'tam_billions': [25, 195, 18, 12, 32, 28],
            'capital_required': [20, 60, 12, 8, 35, 25],
            'time_to_market': [15, 24, 10, 8, 24, 20],
            'revenue_potential': [9, 8, 8, 7, 9, 8],
            'risk_score': [4, 8, 3, 2, 5, 6],
            'attractiveness': [7.8, 6.1, 7.5, 7.6, 7.4, 7.3]
        }
        
        # Funding History
        self.funding_data = {
            'round': ['Seed', 'Series A', 'Series B', 'Series C', 'Bridge', 'Emergency'],
            'amount': [4.7, 22, 20, 50, 15, 8.5],
            'year': [2016, 2017, 2019, 2021, 2022, 2023],
            'valuation': [20, 85, 180, 435, 420, 380]
        }
        
        # Market Data
        self.market_data = {
            'segment': ['Digital Payments', 'SME Lending', 'Credit APIs', 'RegTech', 'Open Banking', 'AI Fintech'],
            'size_billions': [85, 195, 18, 12, 32, 28],
            'cagr': [45, 24, 32, 36, 52, 59],
            'addressable_pct': [25, 55, 85, 70, 50, 35]
        }
        
        # Customer Segments
        self.customer_data = {
            'segment': ['Young Professionals', 'Students', 'SME Owners', 'Freelancers', 'Tech Workers', 'Urban Salaried'],
            'size_millions': [28, 22, 15, 12, 18, 65],
            'avg_transaction': [25000, 18000, 45000, 22000, 48000, 35000],
            'default_rate': [8, 15, 6, 12, 5, 7],
            'ltv': [125000, 85000, 280000, 110000, 320000, 220000],
            'cac': [3500, 2800, 5500, 4200, 4800, 3200],
            'profitability': [8, 6, 9, 7, 10, 9]
        }
        
        # Risk Data
        self.risk_data = {
            'category': ['Credit Risk', 'Regulatory Risk', 'Market Risk', 'Technology Risk', 'Operational Risk', 'Funding Risk'],
            'probability': [9, 8, 7, 5, 6, 8],
            'impact': [10, 9, 7, 6, 7, 9],
            'mitigation_cost': [25, 12, 8, 15, 10, 35]
        }
        
        # Calculate KPIs
        self.kpis = {
            'total_losses': sum(self.financial_data['loss_cr']),
            'peak_valuation': max(self.funding_data['valuation']),
            'current_revenue': self.financial_data['revenue_cr'][-1],
            'current_users': self.operational_data['users_millions'][-1],
            'npa_multiple': self.operational_data['npa_rate'][-1]/self.operational_data['industry_npa'][-1],
            'revenue_growth': self.financial_data['growth_rate'][-1]
        }

    def setup_styling(self):
        """Setup color schemes"""
        self.colors = {
            'primary': '#0066CC',
            'secondary': '#6C757D',
            'success': '#28a745',
            'danger': '#dc3545',
            'warning': '#ffc107',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40'
        }

    def create_app(self):
        """Create the Dash application with proper tab structure"""
        app = dash.Dash(
            __name__, 
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        
        # Define custom CSS styles for professional look
        app.index_string = '''
        <!DOCTYPE html>
        <html>
            <head>
                {%metas%}
                <title>{%title%}</title>
                {%favicon%}
                {%css%}
                <style>
                    .custom-tabs-container {
                        width: 100%;
                    }
                    .custom-tabs {
                        border-bottom: 2px solid #0066CC;
                    }
                    .custom-tab {
                        color: #6c757d !important;
                        border: none !important;
                        background-color: #f8f9fa !important;
                        font-weight: 600 !important;
                        padding: 12px 24px !important;
                        margin-right: 4px !important;
                        border-radius: 8px 8px 0 0 !important;
                    }
                    .custom-tab--selected {
                        color: white !important;
                        background-color: #0066CC !important;
                        border-bottom: 2px solid #0066CC !important;
                    }
                    .kpi-card {
                        border-left: 4px solid #0066CC;
                        transition: transform 0.2s;
                    }
                    .kpi-card:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                    }
                    .chart-container {
                        background: white;
                        border-radius: 8px;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        padding: 20px;
                        margin-bottom: 20px;
                    }
                </style>
            </head>
            <body>
                {%app_entry%}
                <footer>
                    {%config%}
                    {%scripts%}
                    {%renderer%}
                </footer>
            </body>
        </html>
        '''
        
        # App layout with clean tab structure
        app.layout = dbc.Container([
            # Header Section
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H1("ZestMoney Strategic Intelligence Platform", 
                               style={'color': '#0066CC', 'fontWeight': 'bold', 'marginBottom': '10px'}),
                        html.P("Comprehensive Performance Analysis & Strategic Transformation Dashboard",
                              style={'color': '#6c757d', 'fontSize': '18px', 'marginBottom': '0'})
                    ], style={'textAlign': 'center', 'padding': '30px 0 20px 0'})
                ], width=12)
            ]),
            
            # KPI Cards Row
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"₹{self.kpis['total_losses']:.0f}Cr", style={'color': '#dc3545', 'marginBottom': '5px'}),
                            html.P("Total Losses", style={'color': '#6c757d', 'marginBottom': '0', 'fontSize': '14px'}),
                        ])
                    ], className="kpi-card")
                ], width=2),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"${self.kpis['peak_valuation']:.0f}M", style={'color': '#0066CC', 'marginBottom': '5px'}),
                            html.P("Peak Valuation", style={'color': '#6c757d', 'marginBottom': '0', 'fontSize': '14px'}),
                        ])
                    ], className="kpi-card")
                ], width=2),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"₹{self.kpis['current_revenue']:.0f}Cr", style={'color': '#28a745', 'marginBottom': '5px'}),
                            html.P("Current Revenue", style={'color': '#6c757d', 'marginBottom': '0', 'fontSize': '14px'}),
                        ])
                    ], className="kpi-card")
                ], width=2),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{self.kpis['current_users']:.1f}M", style={'color': '#17a2b8', 'marginBottom': '5px'}),
                            html.P("User Base", style={'color': '#6c757d', 'marginBottom': '0', 'fontSize': '14px'}),
                        ])
                    ], className="kpi-card")
                ], width=2),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{self.kpis['npa_multiple']:.1f}x", style={'color': '#ffc107', 'marginBottom': '5px'}),
                            html.P("NPA vs Industry", style={'color': '#6c757d', 'marginBottom': '0', 'fontSize': '14px'}),
                        ])
                    ], className="kpi-card")
                ], width=2),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H3(f"{self.kpis['revenue_growth']:.1f}%", style={'color': '#6c757d', 'marginBottom': '5px'}),
                            html.P("Revenue Growth", style={'color': '#6c757d', 'marginBottom': '0', 'fontSize': '14px'}),
                        ])
                    ], className="kpi-card")
                ], width=2)
            ], className="mb-4"),
            
            # Tabs Navigation
            html.Div([
                dcc.Tabs(
                    id="main-tabs",
                    value="dashboard",
                    children=[
                        dcc.Tab(label="Executive Dashboard", value="dashboard", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Financial Analysis", value="financial", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Operations", value="operations", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Strategic Planning", value="strategic", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Customer Analytics", value="customer", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Market Intelligence", value="market", className="custom-tab", selected_className="custom-tab--selected"),
                        dcc.Tab(label="Risk Assessment", value="risk", className="custom-tab", selected_className="custom-tab--selected")
                    ],
                    className="custom-tabs",
                    parent_className="custom-tabs-container"
                )
            ], style={'marginBottom': '30px'}),
            
            # Tab Content Area
            html.Div(id='tab-content-area', style={'minHeight': '800px'})
            
        ], fluid=True, style={'backgroundColor': '#f8f9fa', 'minHeight': '100vh', 'padding': '0'})
        
        # Single callback for tab navigation
        @app.callback(
            Output('tab-content-area', 'children'),
            Input('main-tabs', 'value')
        )
        def render_tab_content(active_tab):
            if active_tab == 'financial':
                return self.create_financial_content()
            elif active_tab == 'operations':
                return self.create_operations_content()
            elif active_tab == 'strategic':
                return self.create_strategic_content()
            elif active_tab == 'customer':
                return self.create_customer_content()
            elif active_tab == 'market':
                return self.create_market_content()
            elif active_tab == 'risk':
                return self.create_risk_content()
            else:
                return self.create_dashboard_content()
        
        return app
    
    def create_dashboard_content(self):
        """Create executive dashboard content"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Revenue vs Loss Trend", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_revenue_loss_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.H4("User Growth Analysis", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_user_growth_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Funding Timeline", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_funding_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.H4("NPA Trend Analysis", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_npa_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6)
            ], className="mb-4"),
            
            # Strategic Summary
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Strategic Recommendations", style={'margin': '0', 'color': '#0066CC'})),
                        dbc.CardBody([
                            html.Div([
                                html.Div([
                                    html.Span("✓", style={'color': '#28a745', 'fontSize': '18px', 'marginRight': '10px'}),
                                    "Pivot to B2B SaaS Infrastructure"
                                ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
                                html.Div([
                                    html.Span("✓", style={'color': '#28a745', 'fontSize': '18px', 'marginRight': '10px'}),
                                    "Focus on RegTech Compliance Solutions"
                                ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
                                html.Div([
                                    html.Span("✓", style={'color': '#28a745', 'fontSize': '18px', 'marginRight': '10px'}),
                                    "Implement AI-driven Risk Management"
                                ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
                                html.Div([
                                    html.Span("✓", style={'color': '#28a745', 'fontSize': '18px', 'marginRight': '10px'}),
                                    "Develop Open Banking APIs"
                                ], style={'marginBottom': '10px', 'display': 'flex', 'alignItems': 'center'}),
                                html.Div([
                                    html.Span("✓", style={'color': '#28a745', 'fontSize': '18px', 'marginRight': '10px'}),
                                    "Strategic Asset Monetization"
                                ], style={'display': 'flex', 'alignItems': 'center'})
                            ])
                        ])
                    ], className="chart-container")
                ], width=12)
            ])
        ])
    
    def create_financial_content(self):
        """Create financial analysis content"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Revenue Growth", style={'color': '#0066CC'}),
                            html.H3(f"{self.kpis['revenue_growth']:.1f}%", style={'color': '#28a745'}),
                            html.P("Year-over-Year", style={'color': '#6c757d'})
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Burn Rate", style={'color': '#0066CC'}),
                            html.H3(f"{self.financial_data['burn_multiple'][-1]:.1f}x", style={'color': '#ffc107'}),
                            html.P("Expense/Revenue", style={'color': '#6c757d'})
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Gross Margin", style={'color': '#0066CC'}),
                            html.H3(f"{self.financial_data['gross_margin'][-1]:.1f}%", style={'color': '#17a2b8'}),
                            html.P("Current Margin", style={'color': '#6c757d'})
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Total Expenses", style={'color': '#0066CC'}),
                            html.H3(f"₹{self.financial_data['expenses_cr'][-1]:.0f}Cr", style={'color': '#dc3545'}),
                            html.P("FY2024", style={'color': '#6c757d'})
                        ])
                    ])
                ], width=3)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Revenue & Expense Trends", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_revenue_expense_chart(), style={'height': '450px'})
                    ], className="chart-container")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.H4("Expense Breakdown (2024)", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_expense_breakdown_chart(), style={'height': '450px'})
                    ], className="chart-container")
                ], width=6)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Burn Rate Analysis", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_burn_rate_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=12)
            ])
        ])
    
    def create_operations_content(self):
        """Create operations content"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("User Engagement Analysis", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_detailed_user_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.H4("Merchant Network Growth", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_merchant_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Customer Churn Analysis", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_churn_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.H4("App Rating Trend", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_rating_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6)
            ])
        ])
    
    def create_strategic_content(self):
        """Create strategic planning content"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Strategic Opportunity Matrix", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_opportunity_matrix(), style={'height': '500px'})
                    ], className="chart-container")
                ], width=8),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Top Opportunities", style={'margin': '0', 'color': '#0066CC'})),
                        dbc.CardBody([
                            html.Div([
                                html.H6("1. B2B Credit Infrastructure", style={'color': '#28a745'}),
                                html.P("TAM: $25B, Capital: $20M"),
                                html.Hr(),
                                html.H6("2. RegTech Solutions", style={'color': '#17a2b8'}),
                                html.P("TAM: $12B, Capital: $8M"),
                                html.Hr(),
                                html.H6("3. Credit Scoring APIs", style={'color': '#0066CC'}),
                                html.P("TAM: $18B, Capital: $12M")
                            ])
                        ])
                    ], className="h-100")
                ], width=4)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Market Size Analysis", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_market_size_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.H4("Implementation Timeline", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_roadmap_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6)
            ])
        ])
    
    def create_customer_content(self):
        """Create customer analytics content"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Customer Segmentation", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_customer_segmentation(), style={'height': '500px'})
                    ], className="chart-container")
                ], width=8),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Segment Insights", style={'margin': '0', 'color': '#0066CC'})),
                        dbc.CardBody([
                            html.H6("High-Value Segments:"),
                            html.Ul([
                                html.Li("Tech Workers: ₹3.2L LTV"),
                                html.Li("SME Owners: ₹2.8L LTV"),
                                html.Li("Urban Salaried: ₹2.2L LTV")
                            ]),
                            html.Hr(),
                            html.H6("Growth Opportunities:"),
                            html.Ul([
                                html.Li("Focus on professionals"),
                                html.Li("B2B SME lending"),
                                html.Li("Premium products")
                            ])
                        ])
                    ], className="h-100")
                ], width=4)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("LTV vs CAC Analysis", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_ltv_cac_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=12)
            ])
        ])
    
    def create_market_content(self):
        """Create market intelligence content"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Market Size by Segment", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_market_segments_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6),
                
                dbc.Col([
                    html.Div([
                        html.H4("Growth Rate Analysis", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_growth_rate_chart(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=6)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Addressable Market", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_addressable_market(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=12)
            ])
        ])
    
    def create_risk_content(self):
        """Create risk assessment content"""
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Risk Assessment Matrix", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_risk_matrix(), style={'height': '500px'})
                    ], className="chart-container")
                ], width=8),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Critical Risks", style={'margin': '0', 'color': '#dc3545'})),
                        dbc.CardBody([
                            html.H6("Immediate Attention:"),
                            html.Ul([
                                html.Li("Credit Risk: 9.2/10"),
                                html.Li("Regulatory Risk: 8.1/10"),
                                html.Li("Funding Risk: 8.5/10")
                            ]),
                            html.Hr(),
                            html.H6("Mitigation Cost:"),
                            html.P("Total: $90M over 18 months")
                        ])
                    ], className="h-100")
                ], width=4)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    html.Div([
                        html.H4("Risk Mitigation Timeline", style={'marginBottom': '20px', 'color': '#343a40'}),
                        dcc.Graph(figure=self.create_risk_timeline(), style={'height': '400px'})
                    ], className="chart-container")
                ], width=12)
            ])
        ])
    
    # Chart creation methods
    def create_revenue_loss_chart(self):
        """Revenue vs Loss trend"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.financial_data['year'],
            y=self.financial_data['revenue_cr'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color=self.colors['success'], width=3),
            hovertemplate='<b>Revenue</b><br>Year: %{x}<br>Amount: ₹%{y} Cr<extra></extra>'
        ))
        
        fig.add_trace(go.Scatter(
            x=self.financial_data['year'],
            y=self.financial_data['loss_cr'],
            mode='lines+markers',
            name='Net Loss',
            line=dict(color=self.colors['danger'], width=3),
            hovertemplate='<b>Net Loss</b><br>Year: %{x}<br>Loss: ₹%{y} Cr<extra></extra>'
        ))
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Amount (₹ Crores)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_user_growth_chart(self):
        """User growth analysis"""
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(go.Scatter(
            x=self.operational_data['year'],
            y=self.operational_data['users_millions'],
            mode='lines+markers',
            name='Total Users',
            line=dict(color=self.colors['primary'], width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=self.operational_data['year'],
            y=self.operational_data['active_users_millions'],
            mode='lines+markers',
            name='Active Users',
            line=dict(color=self.colors['info'], width=3)
        ))
        
        engagement_rate = [active/total*100 for active, total in 
                          zip(self.operational_data['active_users_millions'], 
                              self.operational_data['users_millions'])]
        
        fig.add_trace(go.Scatter(
            x=self.operational_data['year'],
            y=engagement_rate,
            mode='lines+markers',
            name='Engagement Rate (%)',
            line=dict(color=self.colors['warning'], width=2, dash='dash'),
            yaxis='y2'
        ), secondary_y=True)
        
        fig.update_layout(
            xaxis_title="Year",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        fig.update_yaxes(title_text="Users (Millions)", secondary_y=False)
        fig.update_yaxes(title_text="Engagement Rate (%)", secondary_y=True)
        
        return fig

    def create_funding_chart(self):
        """Funding timeline"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.funding_data['round'],
            y=self.funding_data['amount'],
            text=[f"${x}M" for x in self.funding_data['amount']],
            textposition='auto',
            marker_color=self.colors['primary'],
            hovertemplate='<b>%{x}</b><br>Amount: $%{y}M<br>Year: %{customdata}<extra></extra>',
            customdata=self.funding_data['year']
        ))
        
        fig.update_layout(
            xaxis_title="Funding Round",
            yaxis_title="Amount ($M)",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_npa_chart(self):
        """NPA trend analysis"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.operational_data['year'],
            y=self.operational_data['npa_rate'],
            mode='lines+markers',
            name='ZestMoney NPA Rate',
            line=dict(color=self.colors['danger'], width=3)
        ))
        
        fig.add_trace(go.Scatter(
            x=self.operational_data['year'],
            y=self.operational_data['industry_npa'],
            mode='lines+markers',
            name='Industry Benchmark',
            line=dict(color=self.colors['success'], width=2, dash='dash')
        ))
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="NPA Rate (%)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_revenue_expense_chart(self):
        """Revenue and expense trend"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.financial_data['year'],
            y=self.financial_data['revenue_cr'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color=self.colors['success'], width=3),
            fill='tozeroy'
        ))
        
        fig.add_trace(go.Scatter(
            x=self.financial_data['year'],
            y=self.financial_data['expenses_cr'],
            mode='lines+markers',
            name='Expenses',
            line=dict(color=self.colors['danger'], width=3),
            fill='tozeroy'
        ))
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Amount (₹ Crores)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_expense_breakdown_chart(self):
        """Expense breakdown"""
        labels = ['Marketing', 'Employee Costs', 'Bad Debt', 'Other']
        values = [220, 165, 195, 225]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            marker_colors=[self.colors['warning'], self.colors['info'], self.colors['danger'], self.colors['secondary']]
        )])
        
        fig.update_layout(
            margin=dict(l=40, r=40, t=20, b=40)
        )
        
        return fig

    def create_burn_rate_chart(self):
        """Burn rate analysis"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.financial_data['year'],
            y=self.financial_data['burn_multiple'],
            marker_color=self.colors['warning'],
            text=[f"{x:.1f}x" for x in self.financial_data['burn_multiple']],
            textposition='auto'
        ))
        
        fig.add_hline(y=1.5, line_dash="dash", line_color="green", 
                     annotation_text="Healthy Benchmark (1.5x)")
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Burn Rate Multiple",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_detailed_user_chart(self):
        """Detailed user analysis"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.operational_data['year'],
            y=self.operational_data['users_millions'],
            name='Total Users',
            marker_color=self.colors['primary'],
            text=[f"{x:.1f}M" for x in self.operational_data['users_millions']],
            textposition='auto'
        ))
        
        fig.add_trace(go.Bar(
            x=self.operational_data['year'],
            y=self.operational_data['active_users_millions'],
            name='Active Users',
            marker_color=self.colors['info'],
            text=[f"{x:.1f}M" for x in self.operational_data['active_users_millions']],
            textposition='auto'
        ))
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Users (Millions)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=20, b=40),
            barmode='group',
            plot_bgcolor='white'
        )
        
        return fig

    def create_merchant_chart(self):
        """Merchant growth"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.operational_data['year'],
            y=self.operational_data['merchants'],
            marker_color=self.colors['info'],
            text=[f"{x:,}" for x in self.operational_data['merchants']],
            textposition='auto'
        ))
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Merchant Partners",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_churn_chart(self):
        """Churn analysis"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.operational_data['year'],
            y=self.operational_data['churn_rate'],
            mode='lines+markers',
            line=dict(color=self.colors['danger'], width=3),
            fill='tozeroy'
        ))
        
        fig.add_hline(y=20, line_dash="dash", line_color="green", 
                     annotation_text="Industry Average (20%)")
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="Annual Churn Rate (%)",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_rating_chart(self):
        """App rating trend"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.operational_data['year'],
            y=self.operational_data['app_rating'],
            mode='lines+markers',
            line=dict(color=self.colors['warning'], width=3),
            fill='tozeroy'
        ))
        
        fig.add_hline(y=4.0, line_dash="dash", line_color="green", 
                     annotation_text="Good Rating (4.0)")
        
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title="App Rating",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_opportunity_matrix(self):
        """Strategic opportunity matrix"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.opportunities['risk_score'],
            y=self.opportunities['revenue_potential'],
            mode='markers+text',
            text=self.opportunities['name'],
            marker=dict(
                size=[tam/3 for tam in self.opportunities['tam_billions']],
                color=self.opportunities['attractiveness'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Attractiveness Score")
            ),
            textposition='top center',
            hovertemplate='<b>%{text}</b><br>Risk: %{x}/10<br>Revenue: %{y}/10<br>TAM: $%{customdata}B<extra></extra>',
            customdata=self.opportunities['tam_billions']
        ))
        
        fig.update_layout(
            xaxis_title="Risk Score (1=Low, 10=High)",
            yaxis_title="Revenue Potential (1=Low, 10=High)",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_market_size_chart(self):
        """Market size analysis"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.opportunities['name'],
            y=self.opportunities['tam_billions'],
            marker_color=self.colors['primary'],
            text=[f"${x}B" for x in self.opportunities['tam_billions']],
            textposition='auto'
        ))
        
        fig.update_layout(
            xaxis_title="Opportunity",
            yaxis_title="Total Addressable Market ($B)",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_roadmap_chart(self):
        """Implementation roadmap"""
        phases = ['Foundation', 'Planning', 'Development', 'Launch', 'Scale']
        timeline = [3, 6, 15, 24, 36]
        investment = [10, 15, 25, 20, 15]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=timeline,
            y=investment,
            mode='lines+markers+text',
            text=phases,
            textposition='top center',
            line=dict(color=self.colors['primary'], width=3),
            marker=dict(size=12)
        ))
        
        fig.update_layout(
            xaxis_title="Timeline (Months)",
            yaxis_title="Investment ($M)",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_customer_segmentation(self):
        """Customer segmentation"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.customer_data['size_millions'],
            y=self.customer_data['profitability'],
            mode='markers+text',
            text=self.customer_data['segment'],
            marker=dict(
                size=[ltv/4000 for ltv in self.customer_data['ltv']],
                color=self.customer_data['default_rate'],
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Default Rate (%)")
            ),
            textposition='top center'
        ))
        
        fig.update_layout(
            xaxis_title="Segment Size (Millions)",
            yaxis_title="Profitability Score",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_ltv_cac_chart(self):
        """LTV vs CAC analysis"""
        ltv_cac_ratio = [ltv/cac for ltv, cac in zip(self.customer_data['ltv'], self.customer_data['cac'])]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.customer_data['segment'],
            y=ltv_cac_ratio,
            marker_color=self.colors['success'],
            text=[f"{val:.1f}x" for val in ltv_cac_ratio],
            textposition='auto'
        ))
        
        fig.add_hline(y=3, line_dash="dash", line_color="red", 
                     annotation_text="Healthy Threshold (3x)")
        
        fig.update_layout(
            xaxis_title="Customer Segment",
            yaxis_title="LTV/CAC Ratio",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_market_segments_chart(self):
        """Market segments"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.market_data['segment'],
            y=self.market_data['size_billions'],
            marker_color=self.colors['info'],
            text=[f"${x}B" for x in self.market_data['size_billions']],
            textposition='auto'
        ))
        
        fig.update_layout(
            xaxis_title="Market Segment",
            yaxis_title="Market Size ($B)",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_growth_rate_chart(self):
        """Growth rate analysis"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.market_data['segment'],
            y=self.market_data['cagr'],
            marker_color=self.colors['success'],
            text=[f"{x}%" for x in self.market_data['cagr']],
            textposition='auto'
        ))
        
        fig.update_layout(
            xaxis_title="Market Segment",
            yaxis_title="CAGR (%)",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_addressable_market(self):
        """Addressable market"""
        addressable = [size * addr/100 for size, addr in 
                      zip(self.market_data['size_billions'], self.market_data['addressable_pct'])]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.market_data['segment'],
            y=self.market_data['size_billions'],
            name='Total Market',
            marker_color=self.colors['info'],
            opacity=0.6
        ))
        
        fig.add_trace(go.Bar(
            x=self.market_data['segment'],
            y=addressable,
            name='Addressable Market',
            marker_color=self.colors['primary']
        ))
        
        fig.update_layout(
            xaxis_title="Market Segment",
            yaxis_title="Market Size ($B)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
            margin=dict(l=40, r=40, t=20, b=40),
            barmode='overlay',
            plot_bgcolor='white'
        )
        
        return fig

    def create_risk_matrix(self):
        """Risk matrix"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.risk_data['probability'],
            y=self.risk_data['impact'],
            mode='markers+text',
            text=self.risk_data['category'],
            marker=dict(
                size=[cost*2 for cost in self.risk_data['mitigation_cost']],
                color=self.risk_data['mitigation_cost'],
                colorscale='Reds',
                showscale=True,
                colorbar=dict(title="Mitigation Cost ($M)")
            ),
            textposition='top center'
        ))
        
        fig.update_layout(
            xaxis_title="Probability Score",
            yaxis_title="Impact Severity",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

    def create_risk_timeline(self):
        """Risk mitigation timeline"""
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=self.risk_data['category'],
            y=self.risk_data['mitigation_cost'],
            marker_color=self.colors['danger'],
            text=[f"${val}M" for val in self.risk_data['mitigation_cost']],
            textposition='auto'
        ))
        
        fig.update_layout(
            xaxis_title="Risk Category",
            yaxis_title="Mitigation Cost ($M)",
            margin=dict(l=40, r=40, t=20, b=40),
            plot_bgcolor='white'
        )
        
        return fig

def main():
    """Main execution function optimized for Heroku deployment"""
    try:
        print("\n🚀 INITIALIZING ZESTMONEY ANALYTICS PLATFORM...")
        
        # Initialize the analytics platform
        analytics = ZestMoneyAnalytics()
        print("✅ Analytics Platform Initialized")
        
        # Create the Dash application
        print("\n🎛️ CREATING INTERACTIVE DASHBOARD...")
        app = analytics.create_app()
        print("✅ Dashboard Created Successfully")
        
        # Configure for deployment
        server = app.server
        
        # Get port from environment variable (Heroku sets this)
        port = int(os.environ.get('PORT', 8050))
        host = os.environ.get('HOST', '0.0.0.0')
        debug = os.environ.get('DEBUG', 'False').lower() == 'true'
        
        # Print summary
        print("\n" + "=" * 80)
        print("ZESTMONEY ANALYTICS DASHBOARD READY")
        print("=" * 80)
        print("📊 Features:")
        print("├─ Executive Dashboard")
        print("├─ Financial Analysis")
        print("├─ Operations Intelligence")
        print("├─ Strategic Planning")
        print("├─ Customer Analytics")
        print("├─ Market Intelligence")
        print("└─ Risk Assessment")
        print("=" * 80)
        
        # Only auto-launch browser in development
        if debug and port == 8050:
            def open_browser():
                time.sleep(1.5)
                webbrowser.open_new(f'http://{host}:{port}/')
            
            print(f"\n📊 LAUNCHING DASHBOARD...")
            print(f"📍 Available at: http://{host}:{port}/")
            print("🔧 Opening browser automatically...")
            
            # Start browser in separate thread
            threading.Timer(1, open_browser).start()
        else:
            print(f"\n📊 DASHBOARD READY ON PORT {port}")
        
        # Run the application
        app.run(debug=debug, host=host, port=port)
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n✅ SESSION COMPLETE")

# Expose server for Heroku
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
analytics = ZestMoneyAnalytics()
app = analytics.create_app()
server = app.server

if __name__ == "__main__":
    main()
