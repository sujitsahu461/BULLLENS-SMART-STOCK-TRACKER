"""
CLI interface for BullLens ML models.
Run: python -m bulllens.ml_model.risk_model --symbol RELIANCE --horizon 10
"""

import argparse
import sys
from ml_model.risk_model import train_volatility_model, predict_volatility


def main():
    parser = argparse.ArgumentParser(
        description="BullLens Volatility Prediction Model CLI"
    )
    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Stock symbol (e.g., RELIANCE)"
    )
    parser.add_argument(
        "--horizon",
        type=int,
        default=5,
        help="Prediction horizon in days (2-60, default 5)"
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Train model before predicting"
    )
    parser.add_argument(
        "--n-estimators",
        type=int,
        default=500,
        help="RandomForest n_estimators (default 500)"
    )
    parser.add_argument(
        "--max-depth",
        type=int,
        default=10,
        help="RandomForest max_depth (default 10)"
    )
    
    args = parser.parse_args()
    
    # Validate horizon
    if args.horizon < 2 or args.horizon > 60:
        print("ERROR: horizon must be between 2 and 60 days")
        sys.exit(1)
    
    # Train if requested
    if args.train:
        print(f"Training volatility model for horizon {args.horizon}...")
        try:
            metrics = train_volatility_model(
                horizon=args.horizon,
                n_estimators=args.n_estimators,
                max_depth=args.max_depth
            )
            print(f"✓ Training complete")
            print(f"  CV MAE: {metrics['cv_mae']:.4f}")
            print(f"  CV MAE Std: {metrics['cv_mae_std']:.4f}")
        except Exception as e:
            print(f"✗ Training failed: {e}")
            sys.exit(1)
    
    # Predict
    print(f"\nPredicting volatility for {args.symbol} (horizon {args.horizon}d)...")
    try:
        result = predict_volatility(symbol=args.symbol, horizon=args.horizon)
        print(f"✓ Prediction complete")
        print(f"  Predicted Volatility: {result['predicted_volatility']:.4f}")
        print(f"  CV Score: {result['cv_score']:.4f}")
        print(f"  Unit: {result['unit']}")
    except RuntimeError as e:
        print(f"✗ Prediction failed: {e}")
        print(f"  Hint: Try --train flag to train the model first")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Prediction failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
