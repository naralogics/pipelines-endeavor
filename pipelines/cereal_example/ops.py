from dagster import In, op


@op(
    name="gather_and_cleanup_cereal_data",
    description="Gathers the node data and does some basic cleaned",
    ins={
        "input_df": In(
            description="Input DataFrame containing node records to import",
        )
    },
)
def gather_and_cleanup_cereal_data(input_df):
    # This function is a placeholder for pulling in the dataframe and doing initial cleaning
    # The input dataframe comes from the configuration file.

    return input_df


@op(ins={"cereals": In(description="Input DataFrame containing node records to import")})
def cereal_calories(_context, cereals):
    by_calories = cereals.sort_values(by=["calories"], ascending=False)

    most_caloric, least_caloric = tuple(by_calories["name"].iloc[[0, -1]])
    _context.log.info(
        f"""
        Most caloric cereal: {most_caloric}
        Least caloric cereal: {least_caloric}
        """
    )

    return most_caloric, least_caloric
