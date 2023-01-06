"""
Defines the catalogs of pipelines for the Rocketeer environment.
"""
from cereal_example.pipelines import (
    coalesce_emitter_files_pipeline,
    community_learning_pipeline,
    connectome_1_nodes,
    connectome_2_properties,
    connectome_evaluation,
    recommendations_transform_pipeline,
    rpvs_pipeline,
    simulator_get_recommendations_pipeline,
)
from cereal_example.sensors import coalesce_s3_files_sensor, emitter_file_sensor
from dagster import repository


@repository()
def local_catalog():
    """Define the pipelines in the example  environment."""
    return {
        "pipelines": {
            "connectome_1_nodes": lambda: connectome_1_nodes,
            "connectome_2_properties": lambda: connectome_2_properties,
            "rpvs_pipeline": lambda: rpvs_pipeline,
            "connectome_evaluation": lambda: connectome_evaluation,
            "simulator_get_recommendations_pipeline": lambda: simulator_get_recommendations_pipeline,
            "recommendations_transform_pipeline": lambda: recommendations_transform_pipeline,
            "coalesce_emitter_files_pipeline": lambda: coalesce_emitter_files_pipeline,
        },
        "sensors": {
            "emitter_file_sensor": lambda: emitter_file_sensor,
            "coalesce_s3_files_sensor": lambda: coalesce_s3_files_sensor,
        },
    }


@repository()
def community_learning_workflow():
    """Define the pipelines for community workflow"""
    return {
        "pipelines": {
            "community_learning_pipeline": lambda: community_learning_pipeline,
        },
    }
