from guidance import models

def load_model_to_cpu(model_path: str, context_window: str):
    model = models.LlamaCpp(model_path, n_ctx=context_window, echo=True)
    return model

