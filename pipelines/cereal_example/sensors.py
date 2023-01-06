from cereal_example.pipelines import (
    coalesce_emitter_files_pipeline,
    recommendations_transform_pipeline,
)
from dagster import sensor
from pearl.pipelines.environment import get_run_configs
from pearl.pipelines.sensors.engine.emitter.sensors import coalesce_s3_files, emitter_file

configs = get_run_configs()


@sensor(job=recommendations_transform_pipeline, minimum_interval_seconds=120)
def emitter_file_sensor():
    for run_request in emitter_file(configs["recommendations_transform"]):
        yield run_request


@sensor(job=coalesce_emitter_files_pipeline, minimum_interval_seconds=120)
def coalesce_s3_files_sensor():
    for run_request in coalesce_s3_files(configs["coalesce_emitter_files"]):
        yield run_request
