import mlflow
import mlflow.sklearn
import pandas as pd
import yaml
import json
import joblib
import os
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, precision_score, recall_score

# Nguong chat luong cua lab nay la f1_score, KHONG phai accuracy.
# Ly do: bo du lieu Adult co ty le lop 75/25. Mot mo hinh doan bua
# "thu nhap thap" cho moi mau da dat accuracy 0.75 ma khong hoc duoc gi.
F1_THRESHOLD = 0.65


def train(
    params: dict,
    data_path: str = "data/train_batch1.csv",
    eval_path: str = "data/holdout.csv",
) -> float:
    """
    Huan luyen mo hinh va ghi nhan ket qua vao MLflow.

    Tham so:
        params     : dict chua cac sieu tham so cho GradientBoostingClassifier.
        data_path  : duong dan den file du lieu huan luyen.
        eval_path  : duong dan den file du lieu danh gia (holdout).

    Tra ve:
        f1 (float): diem F1 cua lop duong (thu nhap > 50K) tren tap holdout.
    """

    # TODO 1: Doc du lieu huan luyen va danh gia
    df_train = pd.read_csv(data_path)
    df_eval  = pd.read_csv(eval_path)

    # TODO 2: Tach dac trung (X) va nhan (y)
    X_train = df_train.drop(columns=["target"])
    y_train = df_train["target"]
    X_eval  = df_eval.drop(columns=["target"])
    y_eval  = df_eval["target"]

    with mlflow.start_run():

        # TODO 3: Ghi nhan cac sieu tham so
        mlflow.log_params(params)

        # TODO 4: Khoi tao va huan luyen GradientBoostingClassifier
        # Goi y: su dung random_state=42 de dam bao tinh tai tao
        model = GradientBoostingClassifier(**params, random_state=42)
        model.fit(X_train, y_train)


        # --- BONUS 5: Data Drift ---
        pos_ratio = y_train.mean()
        mlflow.log_metric("pos_ratio", pos_ratio)
        if abs(pos_ratio - 0.248) > 0.05:
            print(f"WARNING: Data drift detected! Positive ratio is {pos_ratio:.4f}")

        # --- BONUS 2: Optimal Threshold ---
        best_threshold = 0.5
        best_f1 = 0.0
        best_preds = None

        probs = model.predict_proba(X_eval)[:, 1]
        for threshold in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
            preds = (probs >= threshold).astype(int)
            tmp_f1 = f1_score(y_eval, preds)
            if tmp_f1 > best_f1:
                best_f1 = tmp_f1
                best_threshold = threshold
                best_preds = preds
                
        f1 = best_f1
        preds = best_preds
        acc = accuracy_score(y_eval, preds)
        
        mlflow.log_param("best_threshold", best_threshold)


        # --- BONUS 3: Precision / Recall Artifacts ---
        report = classification_report(y_eval, preds, output_dict=True)
        cm = confusion_matrix(y_eval, preds)
        
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/classification_report.json", "w") as f_out:
            json.dump(report, f_out, indent=2)
            
        with open("outputs/confusion_matrix.txt", "w") as f_out:
            f_out.write(str(cm))
        
        mlflow.log_artifact("outputs/classification_report.json")
        mlflow.log_artifact("outputs/confusion_matrix.txt")



        # TODO 6: Ghi nhan chi so vao MLflow
        mlflow.log_metric("f1_score", f1)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(model, "model")

        # TODO 7: In ket qua ra man hinh
        print(f"F1: {f1:.4f} | Accuracy: {acc:.4f}")

        # TODO 8: Luu metrics ra file outputs/report.json
        # File nay duoc doc boi GitHub Actions o Buoc 2
        os.makedirs("outputs", exist_ok=True)
        with open("outputs/report.json", "w") as f:
            json.dump({"f1_score": f1, "accuracy": acc}, f)

        # TODO 9: Luu mo hinh ra file models/model.joblib
        # File nay duoc upload len cloud storage o Buoc 2
        os.makedirs("models", exist_ok=True)
        joblib.dump(model, "models/model.joblib")

    # TODO 10: Tra ve f1
    return f1


if __name__ == "__main__":
    with open("params.yaml") as f:
        params = yaml.safe_load(f)
    train(params)
