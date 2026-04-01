
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import filedialog, messagebox
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import mean_squared_error, accuracy_score, r2_score, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.decomposition import PCA
import warnings
warnings.filterwarnings('ignore')

# Modern Theme Configuration
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class ModernDataDashboard:
    def __init__(self):
        self.app = ctk.CTk()
        self.app.title("Modern Admin Data Dashboard")
        self.app.geometry("1400x900")
        self.app.minsize(1200, 800)
        
        # Color scheme
        self.colors = {
            'primary': "#3B82F6",
            'success': "#10B981",
            'warning': "#F59E0B",
            'danger': "#EF4444",
            'bg_dark': "#0F172A",
            'card': "#1E293B",
            'text': "#F1F5F9"
        }
        
        # Fonts
        self.font_title = ("Inter", 24, "bold")
        self.font_header = ("Inter", 16, "bold")
        self.font_text = ("Inter", 12)
        self.font_small = ("Inter", 10)
        
        self.df = None
        self.df_original = None
        self.figures = []
        self.current_tab = "overview"
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with gradient effect
        self.main_container = ctk.CTkFrame(self.app, fg_color=self.colors['bg_dark'])
        self.main_container.pack(fill="both", expand=True)
        
        # Header
        self.create_header()
        
        # Content area
        self.content_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Sidebar
        self.create_sidebar()
        
        # Main dashboard area
        self.dashboard_frame = ctk.CTkFrame(self.content_frame, fg_color=self.colors['card'], corner_radius=15)
        self.dashboard_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
        
        # Initialize with welcome screen
        self.show_welcome()
        
    def create_header(self):
        header = ctk.CTkFrame(self.main_container, height=70, fg_color=self.colors['card'], corner_radius=0)
        header.pack(fill="x", pady=(0, 10))
        header.pack_propagate(False)
        
        # Logo/Title
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", padx=20, pady=10)
        
        ctk.CTkLabel(title_frame, text="📊", font=("Inter", 28)).pack(side="left")
        ctk.CTkLabel(title_frame, text="DataAdmin Pro", font=self.font_title, text_color=self.colors['text']).pack(side="left", padx=10)
        
        # Status indicator
        self.status_frame = ctk.CTkFrame(header, fg_color="transparent")
        self.status_frame.pack(side="right", padx=20)
        
        self.status_dot = ctk.CTkLabel(self.status_frame, text="●", font=("Inter", 16), text_color=self.colors['danger'])
        self.status_dot.pack(side="left")
        
        self.status_text = ctk.CTkLabel(self.status_frame, text="No Dataset", font=self.font_text, text_color="gray")
        self.status_text.pack(side="left", padx=5)
        
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self.content_frame, width=280, fg_color=self.colors['card'], corner_radius=15)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Data Operations Section
        self.create_section_header(sidebar, "📁 Data Operations")
        
        self.create_modern_button(sidebar, "Upload Dataset", self.upload_file, self.colors['primary'])
        self.create_modern_button(sidebar, "Auto Clean Data", self.auto_clean, self.colors['warning'])
        self.create_modern_button(sidebar, "Export Results", self.export_results, self.colors['success'])
        
        # Analysis Section
        self.create_section_header(sidebar, "🔍 Analysis")
        
        self.create_modern_button(sidebar, "Dataset Overview", self.show_overview, "#6366F1")
        self.create_modern_button(sidebar, "Correlation Matrix", self.show_correlation, "#8B5CF6")
        self.create_modern_button(sidebar, "Auto Visualizations", self.auto_visualize, "#EC4899")
        self.create_modern_button(sidebar, "ML Predictions", self.run_ml_analysis, "#14B8A6")
        
        # Settings
        self.create_section_header(sidebar, "⚙️ Settings")
        
        theme_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        theme_frame.pack(fill="x", padx=15, pady=5)
        ctk.CTkLabel(theme_frame, text="Theme:", font=self.font_small).pack(side="left")
        
        self.theme_switch = ctk.CTkSegmentedButton(theme_frame, values=["Dark", "Light"], command=self.toggle_theme)
        self.theme_switch.pack(side="right")
        self.theme_switch.set("Dark")
        
    def create_section_header(self, parent, text):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=(20, 10))
        ctk.CTkLabel(frame, text=text, font=self.font_header, text_color=self.colors['primary']).pack(anchor="w")
        ctk.CTkFrame(parent, height=2, fg_color=self.colors['primary']).pack(fill="x", padx=15, pady=(0, 10))
        
    def create_modern_button(self, parent, text, command, color):
        btn = ctk.CTkButton(parent, text=text, command=command, 
                           font=self.font_text, height=40,
                           fg_color=color, hover_color=self.darken_color(color),
                           corner_radius=10)
        btn.pack(fill="x", padx=15, pady=8)
        return btn
        
    def darken_color(self, hex_color):
        # Simple darken for hover effect
        return hex_color
        
    def show_welcome(self):
        self.clear_dashboard()
        
        welcome_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        welcome_frame.pack(expand=True)
        
        ctk.CTkLabel(welcome_frame, text="👋 Welcome to DataAdmin Pro", 
                    font=("Inter", 32, "bold"), text_color=self.colors['text']).pack(pady=20)
        
        ctk.CTkLabel(welcome_frame, 
                    text="Upload a dataset to begin analysis\nSupports CSV, Excel, and JSON formats",
                    font=self.font_text, text_color="gray").pack()
        
        upload_btn = ctk.CTkButton(welcome_frame, text="📂 Upload Your First Dataset", 
                                  command=self.upload_file, font=("Inter", 16, "bold"),
                                  height=50, width=300, fg_color=self.colors['primary'],
                                  corner_radius=15)
        upload_btn.pack(pady=30)
        
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Dataset",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx *.xls"),
                ("JSON files", "*.json"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.df_original = pd.read_csv(file_path)
                elif file_path.endswith(('.xlsx', '.xls')):
                    self.df_original = pd.read_excel(file_path)
                elif file_path.endswith('.json'):
                    self.df_original = pd.read_json(file_path)
                else:
                    self.df_original = pd.read_csv(file_path)
                    
                self.df = self.df_original.copy()
                filename = file_path.split('/')[-1]
                
                # Update status
                self.status_dot.configure(text_color=self.colors['success'])
                self.status_text.configure(text=f"Loaded: {filename} ({len(self.df)} rows)")
                
                messagebox.showinfo("Success", f"Dataset loaded successfully!\nRows: {len(self.df)}\nColumns: {len(self.df.columns)}")
                self.show_overview()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
                
    def auto_clean(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please upload a dataset first!")
            return
            
        try:
            df_clean = self.df.copy()
            
            # Remove duplicates
            duplicates = df_clean.duplicated().sum()
            df_clean = df_clean.drop_duplicates()
            
            # Handle missing values intelligently
            for col in df_clean.columns:
                if df_clean[col].dtype in ['int64', 'float64']:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].median())
                else:
                    df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else "Unknown")
            
            # Encode categoricals
            self.encoders = {}
            for col in df_clean.select_dtypes(include=['object']).columns:
                le = LabelEncoder()
                df_clean[col] = le.fit_transform(df_clean[col].astype(str))
                self.encoders[col] = le
            
            self.df = df_clean
            
            messagebox.showinfo("Cleaning Complete", 
                              f"Removed {duplicates} duplicates\nFilled missing values\nEncoded {len(self.encoders)} categorical columns")
            self.show_overview()
            
        except Exception as e:
            messagebox.showerror("Error", f"Cleaning failed:\n{str(e)}")
            
    def show_overview(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please upload a dataset first!")
            return
            
        self.clear_dashboard()
        self.current_tab = "overview"
        
        # Header
        header = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="📊 Dataset Overview", font=self.font_title, text_color=self.colors['text']).pack(anchor="w")
        
        # Stats Cards
        stats_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        stats = [
            ("Total Rows", f"{len(self.df):,}", self.colors['primary']),
            ("Total Columns", f"{len(self.df.columns)}", self.colors['success']),
            ("Numeric Features", f"{len(self.df.select_dtypes(include=[np.number]).columns)}", self.colors['warning']),
            ("Missing Values", f"{self.df.isnull().sum().sum():,}", self.colors['danger'])
        ]
        
        for title, value, color in stats:
            card = ctk.CTkFrame(stats_frame, fg_color=self.colors['bg_dark'], corner_radius=12, width=200)
            card.pack(side="left", expand=True, fill="both", padx=5)
            card.pack_propagate(False)
            card.configure(height=100)
            
            ctk.CTkLabel(card, text=title, font=self.font_small, text_color="gray").pack(pady=(15, 0))
            ctk.CTkLabel(card, text=value, font=("Inter", 24, "bold"), text_color=color).pack()
            
        # Data Preview
        preview_frame = ctk.CTkFrame(self.dashboard_frame, fg_color=self.colors['bg_dark'], corner_radius=12)
        preview_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ctk.CTkLabel(preview_frame, text="📋 Data Preview (First 10 Rows)", 
                    font=self.font_header, text_color=self.colors['text']).pack(anchor="w", padx=15, pady=10)
        
        # Create scrollable text widget for data
        text_frame = ctk.CTkFrame(preview_frame, fg_color="transparent")
        text_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        preview_text = ctk.CTkTextbox(text_frame, font=("Consolas", 11), 
                                     fg_color=self.colors['card'], text_color=self.colors['text'])
        preview_text.pack(fill="both", expand=True)
        
        preview = self.df.head(10).to_string()
        preview_text.insert("1.0", preview)
        preview_text.configure(state="disabled")
        
    def show_correlation(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please upload a dataset first!")
            return
            
        numeric_df = self.df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) < 2:
            messagebox.showwarning("Warning", "Need at least 2 numeric columns for correlation!")
            return
            
        self.clear_dashboard()
        
        header = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="🔥 Correlation Matrix", font=self.font_title, text_color=self.colors['text']).pack(anchor="w")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 8), facecolor=self.colors['card'])
        ax.set_facecolor(self.colors['card'])
        
        corr = numeric_df.corr()
        mask = np.triu(np.ones_like(corr, dtype=bool))
        
        sns.heatmap(corr, mask=mask, annot=True, fmt='.2f', cmap='RdYlBu_r', 
                   center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
                   annot_kws={'size': 8, 'color': 'white'})
        
        plt.title('Feature Correlation Matrix', color='white', fontsize=14, pad=20)
        plt.xticks(rotation=45, ha='right', color='white')
        plt.yticks(rotation=0, color='white')
        
        # Embed in tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.dashboard_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=20, pady=20)
        
        self.figures.append(fig)
        
    def auto_visualize(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please upload a dataset first!")
            return
            
        self.clear_dashboard()
        
        header = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="📈 Automatic Visualizations", font=self.font_title, text_color=self.colors['text']).pack(anchor="w")
        
        # Create scrollable frame for multiple charts
        scroll_frame = ctk.CTkScrollableFrame(self.dashboard_frame, fg_color="transparent")
        scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) > 0:
            # Distribution plots
            dist_frame = ctk.CTkFrame(scroll_frame, fg_color=self.colors['bg_dark'], corner_radius=12)
            dist_frame.pack(fill="x", pady=10)
            ctk.CTkLabel(dist_frame, text="📊 Distributions", font=self.font_header).pack(anchor="w", padx=15, pady=10)
            
            fig, axes = plt.subplots(1, min(3, len(numeric_cols)), figsize=(12, 4), facecolor=self.colors['card'])
            if len(numeric_cols) == 1:
                axes = [axes]
                
            for idx, col in enumerate(numeric_cols[:3]):
                ax = axes[idx] if len(numeric_cols) > 1 else axes[0]
                ax.set_facecolor(self.colors['card'])
                sns.histplot(self.df[col], kde=True, ax=ax, color=self.colors['primary'])
                ax.set_title(f'{col}', color='white')
                ax.tick_params(colors='white')
                
            plt.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=dist_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="x", padx=15, pady=15)
            self.figures.append(fig)
            
        if len(numeric_cols) >= 2:
            # Scatter plot matrix
            scatter_frame = ctk.CTkFrame(scroll_frame, fg_color=self.colors['bg_dark'], corner_radius=12)
            scatter_frame.pack(fill="x", pady=10)
            ctk.CTkLabel(scatter_frame, text="🔗 Relationships", font=self.font_header).pack(anchor="w", padx=15, pady=10)
            
            fig, ax = plt.subplots(figsize=(8, 6), facecolor=self.colors['card'])
            ax.set_facecolor(self.colors['card'])
            
            # Plot first two numeric columns
            x_col, y_col = numeric_cols[0], numeric_cols[1]
            ax.scatter(self.df[x_col], self.df[y_col], alpha=0.6, c=self.colors['primary'], s=50)
            ax.set_xlabel(x_col, color='white')
            ax.set_ylabel(y_col, color='white')
            ax.set_title(f'{x_col} vs {y_col}', color='white')
            ax.tick_params(colors='white')
            
            canvas = FigureCanvasTkAgg(fig, master=scatter_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="x", padx=15, pady=15)
            self.figures.append(fig)
            
    def run_ml_analysis(self):
        if self.df is None:
            messagebox.showwarning("Warning", "Please upload a dataset first!")
            return
            
        numeric_df = self.df.select_dtypes(include=[np.number])
        if len(numeric_df.columns) < 2:
            messagebox.showwarning("Warning", "Need numeric columns for ML analysis!")
            return
            
        self.clear_dashboard()
        
        header = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="🤖 Machine Learning Analysis", font=self.font_title, text_color=self.colors['text']).pack(anchor="w")
        
        # ML Configuration Frame
        config_frame = ctk.CTkFrame(self.dashboard_frame, fg_color=self.colors['bg_dark'], corner_radius=12)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(config_frame, text="Target Column:", font=self.font_text).pack(side="left", padx=15, pady=15)
        
        target_var = ctk.StringVar(value=numeric_df.columns[-1])
        target_menu = ctk.CTkOptionMenu(config_frame, values=list(numeric_df.columns), 
                                       variable=target_var, width=200)
        target_menu.pack(side="left", padx=10)
        
        ctk.CTkLabel(config_frame, text="Problem Type:", font=self.font_text).pack(side="left", padx=(30, 10))
        
        problem_var = ctk.StringVar(value="Auto")
        problem_menu = ctk.CTkOptionMenu(config_frame, values=["Auto", "Regression", "Classification"], 
                                        variable=problem_var, width=150)
        problem_menu.pack(side="left", padx=10)
        
        run_btn = ctk.CTkButton(config_frame, text="🚀 Run Analysis", 
                               command=lambda: self.execute_ml(target_var.get(), problem_var.get()),
                               fg_color=self.colors['success'], font=self.font_text)
        run_btn.pack(side="right", padx=15)
        
        # Results frame
        self.ml_results_frame = ctk.CTkFrame(self.dashboard_frame, fg_color="transparent")
        self.ml_results_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
    def execute_ml(self, target_col, problem_type):
        # Clear previous results
        for widget in self.ml_results_frame.winfo_children():
            widget.destroy()
            
        try:
            numeric_df = self.df.select_dtypes(include=[np.number])
            X = numeric_df.drop(columns=[target_col])
            y = numeric_df[target_col]
            
            # Auto-detect problem type
            if problem_type == "Auto":
                unique_values = y.nunique()
                problem_type = "Classification" if unique_values <= 10 else "Regression"
                
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Scale features
            scaler = StandardScaler()
            X_train_scaled = scaler.fit_transform(X_train)
            X_test_scaled = scaler.transform(X_test)
            
            results_card = ctk.CTkFrame(self.ml_results_frame, fg_color=self.colors['bg_dark'], corner_radius=12)
            results_card.pack(fill="both", expand=True)
            
            if problem_type == "Regression":
                model = RandomForestRegressor(n_estimators=100, random_state=42)
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                
                mse = mean_squared_error(y_test, y_pred)
                r2 = r2_score(y_test, y_pred)
                
                # Metrics display
                metrics_frame = ctk.CTkFrame(results_card, fg_color="transparent")
                metrics_frame.pack(fill="x", padx=20, pady=20)
                
                self.create_metric_card(metrics_frame, "MSE", f"{mse:.4f}", self.colors['warning'])
                self.create_metric_card(metrics_frame, "R² Score", f"{r2:.4f}", self.colors['success'])
                self.create_metric_card(metrics_frame, "RMSE", f"{np.sqrt(mse):.4f}", self.colors['primary'])
                
            else:
                model = RandomForestClassifier(n_estimators=100, random_state=42)
                model.fit(X_train_scaled, y_train)
                y_pred = model.predict(X_test_scaled)
                
                acc = accuracy_score(y_test, y_pred)
                
                metrics_frame = ctk.CTkFrame(results_card, fg_color="transparent")
                metrics_frame.pack(fill="x", padx=20, pady=20)
                
                self.create_metric_card(metrics_frame, "Accuracy", f"{acc:.2%}", self.colors['success'])
                self.create_metric_card(metrics_frame, "Classes", f"{y.nunique()}", self.colors['primary'])
                
            # Feature importance
            importance_frame = ctk.CTkFrame(results_card, fg_color="transparent")
            importance_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            
            ctk.CTkLabel(importance_frame, text="📊 Feature Importance", 
                        font=self.font_header).pack(anchor="w", pady=(0, 10))
            
            fig, ax = plt.subplots(figsize=(10, 5), facecolor=self.colors['card'])
            ax.set_facecolor(self.colors['card'])
            
            importances = model.feature_importances_
            indices = np.argsort(importances)[::-1][:10]  # Top 10
            
            ax.bar(range(len(indices)), importances[indices], color=self.colors['primary'])
            ax.set_xticks(range(len(indices)))
            ax.set_xticklabels([X.columns[i] for i in indices], rotation=45, ha='right', color='white')
            ax.set_ylabel('Importance', color='white')
            ax.set_title('Top 10 Feature Importances', color='white')
            ax.tick_params(colors='white')
            
            canvas = FigureCanvasTkAgg(fig, master=importance_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            self.figures.append(fig)
            
        except Exception as e:
            messagebox.showerror("ML Error", f"Analysis failed:\n{str(e)}")
            
    def create_metric_card(self, parent, title, value, color):
        card = ctk.CTkFrame(parent, fg_color=self.colors['card'], corner_radius=10, width=200)
        card.pack(side="left", expand=True, fill="both", padx=5)
        card.pack_propagate(False)
        card.configure(height=80)
        
        ctk.CTkLabel(card, text=title, font=self.font_small, text_color="gray").pack(pady=(10, 0))
        ctk.CTkLabel(card, text=value, font=("Inter", 20, "bold"), text_color=color).pack()
        
    def export_results(self):
        if self.df is None:
            messagebox.showwarning("Warning", "No data to export!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.df.to_csv(file_path, index=False)
                else:
                    self.df.to_excel(file_path, index=False)
                messagebox.showinfo("Success", "Data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed:\n{str(e)}")
                
    def toggle_theme(self, value):
        ctk.set_appearance_mode(value.lower())
        
    def clear_dashboard(self):
        for widget in self.dashboard_frame.winfo_children():
            widget.destroy()
        plt.close('all')
        
    def run(self):
        self.app.mainloop()

if __name__ == "__main__":
    app = ModernDataDashboard()
    app.run()
