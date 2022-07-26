import logging
import knime_extension as knext

LOGGER = logging.getLogger(__name__)


@knext.node(
    name="My Template Node",
    node_type=knext.NodeType.LEARNER,
    icon_path="icon.png",
    category="/",
)
@knext.input_table(name="Input Data", description="We read data from here")
@knext.input_table(
    name="Tutorial: Input Data 2", description="We also read data from here"
)
@knext.output_table(name="Output Data", description="Whatever the node has produced")
class TemplateNode:
    """

    This node has a description
    """

    some_param = knext.IntParameter(
        "Some Int Parameter", "The answer to everything", 42, min_value=0
    )

    another_param = knext.StringParameter(
        "Some String parameter", "The classic placeholder", "foobar"
    )

    double_param = knext.DoubleParameter(
        "Double Parameter", "Just for test purposes", 3.0
    )

    boolean_param = knext.BoolParameter(
        "Boolean Parameter", "also just for testing", True
    )

    column_param = knext.ColumnParameter()

    def is_numeric(
        column,
    ):  # Filter columns visible in the column_param for numeric ones
        return (
            column.ktype == knext.double()
            or column.ktype == knext.int32()
            or column.ktype == knext.int64()
        )

    column_param = knext.ColumnParameter(
        label="label", description="description", port_index=0, column_filter=is_numeric
    )

    def configure(self, configure_context, input_schema_1, input_schema_2):
        return input_schema_1.append(knext.Column(knext.double(), "column2"))

    def execute(self, exec_context, input_1, input_2):
        input_1_pandas = (
            input_1.to_pandas()
        )  # Transform the input table to some processable format (pandas or pyarrow)
        input_2_pandas = input_2.to_pandas()
        input_1_pandas["column2"] = (
            input_1_pandas["column1"] + input_2_pandas["column1"]
        )
        input_1_pandas["column2"] = input_1_pandas["column2"] + self.double_param
        LOGGER.warning(self.double_param)
        return knext.Table.from_pandas(input_1_pandas)
