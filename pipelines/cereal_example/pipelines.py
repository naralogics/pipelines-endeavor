from cereal_example.ops import cereal_calories, gather_and_cleanup_cereal_data
from cereal_example.resources import RESOURCE_DEFS
from dagster import job
from pearl.pipelines.environment import get_run_configs
from pearl.pipelines.pipelines.community_learning.pipeline import community_learning
from pearl.pipelines.pipelines.engine.emitter.pipelines import (
    coalesce_emitter_files,
    recommendations_transform,
)
from pearl.pipelines.solids.combine.concatenate import concatenate_frames
from pearl.pipelines.solids.engine.nodes.submit_node_requests import submit_node_requests
from pearl.pipelines.solids.evaluation.evaluate_accuracy import evaluate_accuracy
from pearl.pipelines.solids.filtering.data_query import query_dataframe
from pearl.pipelines.solids.load.file_loader import read_frames, wait_for_experiment_complete
from pearl.pipelines.solids.nara.node import write_nodes_incremental
from pearl.pipelines.solids.nara.property_weight import write_connectome_property_weight
from pearl.pipelines.solids.nara.rpv import write_rpvs
from pearl.pipelines.solids.profile.dataframe import profile_data
from pearl.pipelines.solids.transforms.discretize import transform_to_intervals
from pearl.pipelines.solids.transforms.enrich import assign_new_columns, slugify_values
from pearl.pipelines.solids.visualization.heatmap import create_heatmap
from pearl.pipelines.solids.visualization.table import create_table

configs = get_run_configs()


@job(config=configs["nodes"], resource_defs=RESOURCE_DEFS)
def connectome_1_nodes():
    dfs = read_frames().collect()  # pylint: disable=no-member
    df = concatenate_frames(dfs)

    nodes_df = gather_and_cleanup_cereal_data(df)

    nodes_df = assign_new_columns(nodes_df)
    nodes_df = slugify_values(nodes_df)

    binned_cereal_data, _ = transform_to_intervals(nodes_df)

    cereal_calories(binned_cereal_data)

    # Todo: Add the map_values solid to map the following:
    # mfr: Manufacturer of cereal
    #   A = American Home Food Products;
    #   G = General Mills
    #   K = Kelloggs
    #   N = Nabisco
    #   P = Post
    #   Q = Quaker Oats
    #   R = Ralston Purina
    # type:
    #   cold
    #   hot

    write_nodes_incremental(node_df=binned_cereal_data, initial_df=df)

    # ToDo: Add cache refresh

    profile_data(binned_cereal_data)


@job(config=configs["properties"], resource_defs=RESOURCE_DEFS)
def connectome_2_properties():
    dfs = read_frames().collect()  # pylint: disable=no-member
    df = concatenate_frames(dfs)
    write_connectome_property_weight(df)


@job(config=configs["rpvs"], resource_defs=RESOURCE_DEFS)
def rpvs_pipeline():
    # Todo: This currently does nothing because the rpv file is empty
    dfs = read_frames().collect()  # pylint: disable=no-member
    df = concatenate_frames(dfs)
    write_rpvs(df)


@job(
    name="simulator_get_recommendations_pipeline",
    config=configs["recommendations"],
    resource_defs=RESOURCE_DEFS,
)
def simulator_get_recommendations_pipeline():
    sample_dfs = read_frames().collect()  # pylint: disable=no-member
    sample_df = concatenate_frames(sample_dfs)
    sample_df = query_dataframe(sample_df)
    sample_df = slugify_values(sample_df)
    response, experiment_label, request_count = submit_node_requests(
        input_df=sample_df
    )  # pylint: disable=no-value-for-parameter
    wait_for_experiment_complete(experiment_label)


@job(
    name="coalesce_emitter_files_pipeline",
    description="Pipeline that coalesces S3 emitter files",
    config=configs["coalesce_emitter_files"],
    resource_defs=RESOURCE_DEFS,
)
def coalesce_emitter_files_pipeline():
    coalesce_emitter_files()


@job(
    name="recommendations_transform_pipeline",
    description="Pipeline that transforms emitter results",
    config=configs["recommendations_transform"],
    resource_defs=RESOURCE_DEFS,
)
def recommendations_transform_pipeline():
    recommendations_transform()


@job(
    name="community_learning_pipeline",
    description="Pipeline that learning communities",
    config=configs["community_learning"],
    resource_defs=RESOURCE_DEFS,
)
def community_learning_pipeline():
    community_learning()


@job(
    name="connectome_evaluation",
    description="Fake job that is meant to demonstrate evaluation solid with mocked data",
    config=configs["evaluation"],
    resource_defs=RESOURCE_DEFS,
)
def connectome_evaluation():
    dfs = read_frames().collect()  # pylint: disable=no-member
    df = concatenate_frames(dfs)
    binned_cereal_data, _ = transform_to_intervals(df)
    profile_data(binned_cereal_data)
    _, _, _, confusion_matrix = evaluate_accuracy(binned_cereal_data)
    create_heatmap(confusion_matrix)
    create_table(binned_cereal_data)


if __name__ == '__main__':
    connectome_1_nodes.execute_in_process()
    # connectome_2_properties.execute_in_process()
    # simulator_get_recommendations_pipeline.execute_in_process()
