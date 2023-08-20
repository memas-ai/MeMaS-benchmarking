from .pipeline import CommonTaskNames, PipelineContext, PipelineTask
import memas_client
import memas_sdk
from memas_client.apis.tags import dp_api
from memas_sdk.apis.tags import cp_api


class InitCorpora(PipelineTask):
    def __init__(self, host: str, port: int, namespace_name: str, corpus_names: list[str]) -> None:
        super().__init__(CommonTaskNames.INIT)
        self.host: str = host
        self.port: int = port
        self.namespace_name: str = namespace_name
        self.corpus_names: list[str] = corpus_names

    def execute(self, context: PipelineContext) -> None:
        configuration = memas_client.Configuration(
            host = f"http://{self.host}:{self.port}"
        )

        context.cp_client = cp_api.CpApi(memas_client.ApiClient(configuration))
        context.dp_client = dp_api.DpApi(memas_sdk.ApiClient(configuration))
        context.cp_client.create_user({"namespace_pathname": self.namespace_name})
        for corpus_name in self.corpus_names:
            context.cp_client.create_corpus({"corpus_pathname": f"{self.namespace_name}:{corpus_name}"})
