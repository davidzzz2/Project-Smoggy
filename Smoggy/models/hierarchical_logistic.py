"""Bayesian hierarchical logistic baseline for Smoggy.

This script sets up a reproducible workflow for fitting the Phase 3 Model 1
(described in `model_blueprint.md`). It exposes a Typer CLI with two subcommands:

- ``fit``: trains the model on a feature matrix + metadata file and exports the
  posterior trace plus calibration metrics.
- ``predict``: loads a saved posterior and produces calibrated risk estimates on
  a new dataset.

The implementation relies on PyMC/Numpyro-style modeling with hierarchical
intercepts for site/batch effects and optional covariate slopes. All inputs are
specified via a YAML config for repeatability.
"""
from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence

import arviz as az
import numpy as np
import pandas as pd
import pymc as pm
import typer
from pydantic import BaseModel, Field, validator
from rich.console import Console
from rich.table import Table
import yaml

App = typer.Typer(add_completion=False, help="Smoggy Bayesian Model 1 CLI")
console = Console()


class CovariateConfig(BaseModel):
    name: str
    prior_mu: float = 0.0
    prior_sigma: float = 1.0


class ModelConfig(BaseModel):
    label_column: str = Field(..., description="Binary outcome column name")
    feature_columns: List[str] = Field(..., description="Feature columns to model")
    site_column: str = Field(..., description="Site or batch column for hierarchy")
    covariates: List[CovariateConfig] = Field(default_factory=list)
    standardize_features: bool = True
    standardize_covariates: bool = True
    target_positive_label: int = 1
    draws: int = 1500
    tune: int = 1000
    chains: int = 4
    random_seed: int = 17

    @validator("feature_columns", each_item=False)
    def ensure_non_empty(cls, value: Sequence[str]) -> Sequence[str]:
        if not value:
            raise ValueError("feature_columns cannot be empty")
        return value


@dataclass
class DatasetBundle:
    features: np.ndarray
    covariates: np.ndarray
    label: np.ndarray
    site_index: np.ndarray
    site_names: List[str]
    feature_columns: List[str]
    covariate_columns: List[str]


def read_config(path: pathlib.Path) -> ModelConfig:
    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    return ModelConfig(**raw)


def load_dataframe(feature_path: pathlib.Path) -> pd.DataFrame:
    if feature_path.suffix in {".parquet", ".pq"}:
        return pd.read_parquet(feature_path)
    if feature_path.suffix in {".csv", ".tsv"}:
        sep = "\t" if feature_path.suffix == ".tsv" else ","
        return pd.read_csv(feature_path, sep=sep)
    raise ValueError(f"Unsupported file format: {feature_path}")


def prepare_dataset(df: pd.DataFrame, config: ModelConfig) -> DatasetBundle:
    working = df.copy()

    if config.standardize_features:
        working[config.feature_columns] = (
            (working[config.feature_columns] - working[config.feature_columns].mean())
            / working[config.feature_columns].std().replace(0, 1)
        )

    covariate_cols = [c.name for c in config.covariates]
    if covariate_cols and config.standardize_covariates:
        working[covariate_cols] = (
            (working[covariate_cols] - working[covariate_cols].mean())
            / working[covariate_cols].std().replace(0, 1)
        )

    features = working[config.feature_columns].to_numpy(dtype=np.float64)
    covariates = (
        working[covariate_cols].to_numpy(dtype=np.float64)
        if covariate_cols
        else np.zeros((len(working), 0), dtype=np.float64)
    )

    label = (working[config.label_column] == config.target_positive_label).astype(int).to_numpy()

    site_codes, site_idx = np.unique(working[config.site_column], return_inverse=True)

    return DatasetBundle(
        features=features,
        covariates=covariates,
        label=label,
        site_index=site_idx,
        site_names=site_codes.tolist(),
        feature_columns=config.feature_columns,
        covariate_columns=covariate_cols,
    )


def build_model(bundle: DatasetBundle, config: ModelConfig) -> pm.Model:
    coords = {
        "obs_id": np.arange(bundle.features.shape[0]),
        "feature": bundle.feature_columns,
        "covariate": bundle.covariate_columns,
        "site": bundle.site_names,
    }

    with pm.Model(coords=coords) as model:
        X = pm.MutableData("X", bundle.features, dims=("obs_id", "feature"))
        site_idx = pm.MutableData("site_idx", bundle.site_index, dims=("obs_id",))
        y = pm.MutableData("y", bundle.label, dims="obs_id")

        intercept = pm.Normal("intercept", mu=0.0, sigma=2.5)
        beta = pm.HalfNormal("sigma_features", sigma=1.0)
        feature_weights = pm.Normal(
            "feature_weights",
            mu=0.0,
            sigma=beta,
            dims="feature",
        )

        sigma_site = pm.HalfStudentT("sigma_site", nu=4, sigma=1.0)
        site_offset = pm.Normal("site_offset", mu=0.0, sigma=sigma_site, dims="site")

        linpred = intercept + pm.math.dot(X, feature_weights) + site_offset[site_idx]

        if bundle.covariates.size:
            covariate_matrix = pm.MutableData(
                "covariates",
                bundle.covariates,
                dims=("obs_id", "covariate"),
            )
            covariate_priors = []
            for cov in config.covariates:
                covariate_priors.append(
                    pm.Normal(
                        f"beta_{cov.name}",
                        mu=cov.prior_mu,
                        sigma=cov.prior_sigma,
                    )
                )
            cov_beta = pm.math.stack(covariate_priors)
            linpred += pm.math.dot(covariate_matrix, cov_beta)

        pm.Bernoulli("outcome", logit_p=linpred, observed=y, dims="obs_id")
    return model


def fit_model(
    config_path: pathlib.Path,
    feature_table: pathlib.Path,
    output_dir: pathlib.Path,
) -> None:
    config = read_config(config_path)
    df = load_dataframe(feature_table)
    bundle = prepare_dataset(df, config)

    console.log(f"Loaded {len(df)} rows with {len(bundle.feature_columns)} features")
    model = build_model(bundle, config)

    with model:
        trace = pm.sample(
            draws=config.draws,
            tune=config.tune,
            chains=config.chains,
            target_accept=0.9,
            random_seed=config.random_seed,
            nuts_sampler="numpyro",
        )
        loo = az.loo(trace)
        summary = az.summary(trace, var_names=["intercept", "feature_weights", "sigma_site"])

    output_dir.mkdir(parents=True, exist_ok=True)
    az.to_netcdf(trace, output_dir / "posterior_trace.nc")
    with (output_dir / "loo.json").open("w", encoding="utf-8") as handle:
        json.dump({"loo": loo.loo, "loo_se": loo.loo_se}, handle, indent=2)
    summary.to_csv(output_dir / "posterior_summary.csv")

    table = Table(title="Posterior summary (top 8 features)")
    table.add_column("Parameter")
    table.add_column("Mean")
    table.add_column("SD")
    table.add_column("hdi_3%")
    table.add_column("hdi_97%")

    head = summary.head(8)
    for name, row in head.iterrows():
        table.add_row(name, f"{row['mean']:.3f}", f"{row['sd']:.3f}", f"{row['hdi_3%']:.3f}", f"{row['hdi_97%']:.3f}")

    console.print(table)
    console.log(f"Artifacts written to {output_dir}")


def predict(
    config_path: pathlib.Path,
    posterior_path: pathlib.Path,
    feature_table: pathlib.Path,
    output_path: pathlib.Path,
) -> None:
    config = read_config(config_path)
    df = load_dataframe(feature_table)
    bundle = prepare_dataset(df, config)

    id_series = df.get("sample_id", pd.Series(np.arange(len(df))))

    with pm.Model() as empty_model:
        trace = az.from_netcdf(posterior_path)

    feature_weights = trace.posterior["feature_weights"].stack(draw=("chain", "draw"))
    intercept = trace.posterior["intercept"].stack(draw=("chain", "draw"))
    site_offset = trace.posterior["site_offset"].stack(draw=("chain", "draw"))

    logits = (
        intercept.values
        + (bundle.features @ feature_weights.values)
        + site_offset.values[bundle.site_index]
    )
    probs = 1 / (1 + np.exp(-logits))

    mean_prob = probs.mean(axis=1)
    hdi_low = np.quantile(probs, 0.025, axis=1)
    hdi_high = np.quantile(probs, 0.975, axis=1)

    output = pd.DataFrame(
        {
            "sample_id": id_series,
            "posterior_mean": mean_prob,
            "hdi_2.5": hdi_low,
            "hdi_97.5": hdi_high,
        }
    )
    output.to_csv(output_path, index=False)
    console.log(f"Wrote predictions to {output_path}")


@App.command()
def fit(
    config: pathlib.Path = typer.Option(..., exists=True, help="Path to YAML config"),
    features: pathlib.Path = typer.Option(..., exists=True, help="Feature table (csv/tsv/parquet)"),
    output_dir: pathlib.Path = typer.Option(pathlib.Path("artifacts/model1"), help="Directory for outputs"),
):
    """Fit the hierarchical logistic baseline and export artifacts."""
    fit_model(config, features, output_dir)


@App.command()
def predict_cli(
    config: pathlib.Path = typer.Option(..., exists=True),
    posterior: pathlib.Path = typer.Option(..., exists=True, help="NetCDF posterior"),
    features: pathlib.Path = typer.Option(..., exists=True),
    output: pathlib.Path = typer.Option(pathlib.Path("predictions.csv")),
):
    """Generate posterior risk estimates for a new cohort."""
    predict(config, posterior, features, output)


if __name__ == "__main__":
    App()
