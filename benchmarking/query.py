from .pipeline import CommonTaskNames, PipelineContext, PipelineTask


class QueryWithClueList(PipelineTask):
    def __init__(self, namespace_pathname: str, clues: list[str]) -> None:
        super().__init__(CommonTaskNames.QUERY)
        self.namespace_pathname = namespace_pathname
        self.clues: list[str] = clues

    def execute(self, context: PipelineContext) -> None:
        context.pipeline_data = dict()
        
        for clue in self.clues:
            resp = context.dp_client.recall({"clue": clue, "namespace_pathname": self.namespace_pathname})
            
            context.pipeline_data[clue] = list(map(lambda x: x["document"], resp.body))
