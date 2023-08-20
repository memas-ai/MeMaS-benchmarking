import datasets
from .pipeline import CommonTaskNames, PipelineContext, PipelineTask
import memas_client
from memas_client.model.citation import Citation


class DownloadWikipedia(PipelineTask):
    COUNT_ID = "dataset rows"

    def __init__(self) -> None:
        super().__init__(CommonTaskNames.DOWNLOAD)

    def execute(self, context: PipelineContext) -> None:
        context.pipeline_data = datasets.load_dataset("wikipedia", "20220301.en")
        context.results[DownloadWikipedia.COUNT_ID] = context.pipeline_data.num_rows['train']


class LoadWikipedia(PipelineTask):
    def __init__(self, corpus_pathname: str) -> None:
        super().__init__(CommonTaskNames.INSERT)
        self.corpus_pathname: str = corpus_pathname

    def execute(self, context: PipelineContext) -> None:
        i = 0
        for row in context.pipeline_data["train"]:
            citation = Citation({"source_uri": row["url"], "document_name": row["title"], "source_name": "wikipedia", "description":""})
            request_obj = {"document": row["text"], "corpus_pathname": self.corpus_pathname, "citation": citation}

            success = context.dp_client.remember(request_obj).body.get("success", False)

            assert success

            # TODO: remove
            i += 1
            if i > 2000:
                return
