from typing import Dict, List, Sequence, Optional
from llama_index.core.llama_dataset.base import (
    BaseLlamaDataExample,
    BaseLlamaDataset,
    CreatedBy,
    BaseLlamaExamplePrediction,
    BaseLlamaPredictionDataset,
)
from llama_index.core.llms import LLM
from llama_index.core.bridge.pydantic import Field
from pandas import DataFrame as PandasDataFrame


class SimpleExamplePrediction(BaseLlamaExamplePrediction):
    """RAG example prediction class.

    Args:
        response (str): The response generated by the LLM.
        contexts (Optional[List[str]]): The retrieved context (text) for generating
                                        response.
    """

    label: str = Field(
        default_factory=str,
        description="The generated (predicted) label that can be compared to a reference (ground-truth) label.",
    )

    @property
    def class_name(self) -> str:
        """Data example class name."""
        return "SimpleExamplePrediction"


class SimplePredictionDataset(BaseLlamaPredictionDataset):
    """RagDataset class."""

    _prediction_type = SimpleExamplePrediction

    def to_pandas(self) -> PandasDataFrame:
        """Create pandas dataframe."""
        data: Dict[str, List[str]] = {"label": []}
        if self.predictions:
            for t in self.predictions:
                assert isinstance(t, self._prediction_type)

                data["label"].append(t.label)

        return PandasDataFrame(data)

    @property
    def class_name(self) -> str:
        """Class name."""
        return "SimplePredictionDataset"


class LabelledSimpleDataExample(BaseLlamaDataExample):
    reference_label: str = Field(default_factory=str, description="Class label")
    text: str = Field(default_factory=str, description="Text body of example")
    text_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the query."
    )

    @property
    def class_name(self) -> str:
        """Data example class name."""
        return "LabelledSimpleDataExample"


class LabelledSimpleDataset(BaseLlamaDataset[LLM]):
    _example_type = LabelledSimpleDataExample

    def _construct_prediction_dataset(
        self, predictions: Sequence[SimpleExamplePrediction]  # type: ignore
    ) -> SimplePredictionDataset:
        """Construct the specific prediction dataset.

        Args:
            predictions (List[BaseLlamaExamplePrediction]): the list of predictions.

        Returns:
            BaseLlamaPredictionDataset: A dataset of predictions.
        """
        return SimplePredictionDataset(predictions=predictions)

    def to_pandas(self) -> PandasDataFrame:
        """Create pandas dataframe."""
        data: Dict[str, List[str]] = {
            "reference_label": [],
            "text": [],
            "text_by": [],
        }
        for example in self.examples:
            if not isinstance(example, self._example_type):
                raise ValueError(
                    f"Expected example of type {LabelledSimpleDataExample}, got {type(example)}"
                )

            data["reference_label"].append(example.reference_label)
            data["text"].append(example.text)
            data["text_by"].append(str(example.text_by))

        return PandasDataFrame(data)

    async def _apredict_example(
        self,
        predictor: LLM,
        example: BaseLlamaDataExample,
        sleep_time_in_seconds: int,
    ) -> BaseLlamaExamplePrediction:
        """Async predict RAG example with a query engine."""
        raise NotImplementedError("This method has not yet been implemented.")

    def _predict_example(
        self,
        predictor: LLM,
        example: BaseLlamaDataExample,
        sleep_time_in_seconds: int = 0,
    ) -> BaseLlamaExamplePrediction:
        raise NotImplementedError("This method has not yet been implemented.")

    @property
    def class_name(self) -> str:
        """Data example class name."""
        return "LabelledSimpleDataset"
