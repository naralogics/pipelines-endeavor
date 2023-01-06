import os

from dagster import local_file_manager
from dagster_aws.s3 import s3_resource
from pearl.connect.nara.connectome.connectome_definition import connectome_definition_resource
from pearl.pipelines.io_managers.beta import s3_connectome_io_manager
from pearl.pipelines.io_managers.experiments import experiment_results_io_manager
from pearl.pipelines.io_managers.visualization import plotly_io_manager, profile_report_io_manager
from pearl.resources.resources import default_resources

public_asset_base_path = os.environ["ENV_STORAGE_PUBLIC"]

connectome_resource = {
    "connectome_definition": connectome_definition_resource,
    "connectome_io_manager": s3_connectome_io_manager.configured(
        {"s3_bucket": "nara-example", "s3_prefix": "cereal-connectome-data"}
    ),
    "s3": s3_resource,
    "file_manager": local_file_manager.configured({"base_dir": "/tmp/fs_mgr"}),
    "profile_report_io_manager": profile_report_io_manager.configured(
        {"base_path": f"{public_asset_base_path}/profile_report"}
    ),
    "plotly_io_manager": plotly_io_manager.configured(
        {"base_path": f"{public_asset_base_path}/plotly"},
    ),
    "experiment_io_manager": experiment_results_io_manager,
}

RESOURCE_DEFS = default_resources(connectome_resource)
