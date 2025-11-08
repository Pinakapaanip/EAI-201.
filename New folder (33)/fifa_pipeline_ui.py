import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd, numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt, joblib, os, threading, webbrowser

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("FIFA 2026 ML Prediction Pipeline")
        self.root.attributes("-fullscreen", True)
        self.frame = ttk.Frame(root, padding=20)
        self.frame.pack(fill="both", expand=True)
        self.df = None
        self.features_df = None
        self.lr = None
        self.rf = None
        self.scaler = None
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#0d1117")
        style.configure("TLabel", background="#0d1117", foreground="white", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 11, "bold"), padding=6)
        self.create_widgets()

    def create_widgets(self):
        row = 0
        ttk.Label(self.frame, text="FIFA 2026 Machine Learning Pipeline", font=("Segoe UI", 22, "bold")).grid(column=0, row=row, columnspan=4, pady=15)
        row += 1
        ttk.Button(self.frame, text="Load cleaned_fifa_dataset.csv", command=self.load_data).grid(column=0, row=row, sticky="w", padx=10, pady=6)
        self.data_label = ttk.Label(self.frame, text="No file loaded")
        self.data_label.grid(column=1, row=row, columnspan=3, sticky="w")
        row += 1
        ttk.Button(self.frame, text="Generate TeamTournament Features", command=lambda: threading.Thread(target=self.preprocess).start()).grid(column=0, row=row, padx=10, pady=6, sticky="w")
        ttk.Button(self.frame, text="Train Models", command=lambda: threading.Thread(target=self.train_models).start()).grid(column=1, row=row, padx=10, pady=6, sticky="w")
        ttk.Button(self.frame, text="Evaluate & Save ", command=lambda: threading.Thread(target=self.evaluate).start()).grid(column=2, row=row, padx=10, pady=6, sticky="w")
        ttk.Button(self.frame, text="Predict 2026 & Save", command=lambda: threading.Thread(target=self.predict_latest).start()).grid(column=3, row=row, padx=10, pady=6, sticky="w")
        row += 1
        ttk.Button(self.frame, text="Open Output Folder", command=self.open_output_folder).grid(column=0, row=row, padx=10, pady=6, sticky="w")
        ttk.Button(self.frame, text="Exit", command=self.root.quit).grid(column=3, row=row, padx=10, pady=6, sticky="e")
        row += 1
        ttk.Label(self.frame, text="Log / Output", font=("Segoe UI", 12, "bold")).grid(column=0, row=row, pady=10, sticky="w")
        row += 1
        self.log = tk.Text(self.frame, height=18, width=120, bg="#161b22", fg="white", font=("Consolas", 10))
        self.log.grid(column=0, row=row, columnspan=4)
        row += 1
        self.progress = ttk.Progressbar(self.frame, length=700, mode="determinate")
        self.progress.grid(column=0, row=row, columnspan=4, pady=10)
        self.log_insert("Ready")

    def log_insert(self, t):
        self.log.insert("end", f"{t}\n")
        self.log.see("end")

    def load_data(self):
        p = filedialog.askopenfilename(title="Select cleaned_fifa_dataset.csv", filetypes=[("CSV files","*.csv")])
        if not p:
            return
        try:
            self.df = pd.read_csv(p)
            self.data_label.config(text=os.path.basename(p))
            self.log_insert(f"Loaded {p} rows={self.df.shape[0]} cols={self.df.shape[1]}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def preprocess(self):
        if self.df is None:
            messagebox.showwarning("No data","Load dataset first")
            return
        self.progress['value'] = 10
        df = self.df.copy()
        df['Year'] = df['tournament Name'].str.extract(r'(\d{4})').astype(int)
        tournaments = sorted(df['Tournament Id'].unique(), key=lambda tid: int(df[df['Tournament Id']==tid]['Year'].iloc[0]))
        tid_to_year = {tid: int(df[df['Tournament Id']==tid]['Year'].iloc[0]) for tid in df['Tournament Id'].unique()}
        team_records = []
        for tid in tournaments:
            year = tid_to_year[tid]
            sub = df[df['Tournament Id']==tid]
            teams = pd.unique(sub[['Home Team Name','Away Team Name']].values.ravel('K'))
            finalists = set(sub[sub['Stage Name'].str.contains('final', case=False, na=False)][['Home Team Name','Away Team Name']].values.ravel('K'))
            for team in teams:
                made_final = 1 if team in finalists else 0
                team_records.append({'Tournament Id':tid,'Year':year,'Team':team,'Made_Final':made_final})
        team_df = pd.DataFrame(team_records)
        self.progress['value'] = 40
        past_stats = []
        for _, r in team_df.iterrows():
            y = r['Year']; t = r['Team']
            past = team_df[(team_df['Team']==t) & (team_df['Year']<y)]
            appearances = len(past)
            rec = {'Tournament Id':r['Tournament Id'],'Year':y,'Team':t,'Prev_Appearances':appearances,'Made_Final':r['Made_Final']}
            past_stats.append(rec)
        features_df = pd.DataFrame(past_stats).fillna(0)
        self.features_df = features_df
        features_df.to_csv("pre_features_df.csv", index=False)
        self.progress['value'] = 100
        self.log_insert("Preprocessing done. Saved pre_features_df.csv")
        self.progress['value'] = 0

    def train_models(self):
        if self.features_df is None:
            messagebox.showwarning("No features","Run preprocessing first")
            return
        df = self.features_df.copy()
        features = ['Prev_Appearances']
        train = df[df['Year']<=2018]
        X_train, y_train = train[features].values, train['Made_Final'].values
        self.scaler = StandardScaler()
        X_train_s = self.scaler.fit_transform(X_train)
        self.lr = LogisticRegression(max_iter=2000)
        self.rf = RandomForestClassifier(n_estimators=300, random_state=42)
        self.lr.fit(X_train_s, y_train)
        self.rf.fit(X_train, y_train)
        joblib.dump(self.lr, "pre_lr.joblib")
        joblib.dump(self.rf, "pre_rf.joblib")
        joblib.dump(self.scaler, "pre_scaler.joblib")
        self.log_insert("Training complete. Models saved")

    def evaluate(self):
        if self.features_df is None or self.lr is None or self.rf is None:
            messagebox.showwarning("Missing","Run preprocessing and training first")
            return
        df = self.features_df.copy()
        features = ['Prev_Appearances']
        X, y = df[features].values, df['Made_Final'].values
        Xs = self.scaler.transform(X)
        yp_lr = self.lr.predict(Xs)
        yp_rf = self.rf.predict(X)
        def score(yp, y):
            return {'acc':accuracy_score(y,yp),'prec':precision_score(y,yp,zero_division=0),'rec':recall_score(y,yp,zero_division=0),'f1':f1_score(y,yp,zero_division=0)}
        s_lr = score(yp_lr,y)
        s_rf = score(yp_rf,y)
        self.log_insert(f"LogReg: acc={s_lr['acc']:.3f} prec={s_lr['prec']:.3f} rec={s_lr['rec']:.3f} f1={s_lr['f1']:.3f}")
        self.log_insert(f"RandForest: acc={s_rf['acc']:.3f} prec={s_rf['prec']:.3f} rec={s_rf['rec']:.3f} f1={s_rf['f1']:.3f}")
        self.log_insert("Evaluation complete")

    def predict_latest(self):
        if self.features_df is None or self.rf is None:
            messagebox.showwarning("Missing","Run preprocessing and training first")
            return
        df = self.features_df.copy()
        latest = df[df['Year']==2022].copy()
        if latest.shape[0]==0:
            latest = df.groupby('Team').last().reset_index()
        probs = self.rf.predict_proba(latest[['Prev_Appearances']].values)[:,1]
        latest['Made_Final_Prob'] = probs
        latest = latest.sort_values('Made_Final_Prob', ascending=False)
        latest.to_csv("predictions_2026.csv", index=False)
        top5 = latest.head(5)
        self.log_insert("Predicted top 5 teams most likely to reach final:")
        for i, row in top5.iterrows():
            self.log_insert(f"{row['Team']} ({row['Made_Final_Prob']:.3f})")
        self.log_insert(f"Most probable winner: {top5.iloc[0]['Team']}")
        self.log_insert("Predictions saved to predictions_2026.csv")

    def open_output_folder(self):
        os.startfile(os.getcwd())

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
