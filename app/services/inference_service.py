import torch
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from repositories.inference_repository import InferenceRepository


class InferenceService:

    SCALER = MinMaxScaler()

    def __init__(self, repo: InferenceRepository):
        self.repo = repo

    def infer(self, model_name, model_id, input_data: list[float]):
        model = self.repo.get_model(model_name, model_id)
        reshaped = np.array(input_data)[..., None]
        scaled = self.SCALER.fit_transform(reshaped).squeeze()[..., None]
        tensor = torch.from_numpy(scaled).float()
        unsqueezed = tensor.unsqueeze(0)
        with torch.no_grad():
            output = model(unsqueezed)
            pred = self.SCALER.inverse_transform(output.numpy())
            return pred
