# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

"""Base classes for all :mod:`torchgeo` trainers."""

from abc import ABC, abstractmethod
from typing import Any

import lightning
from lightning.pytorch import LightningModule
from torch.optim import AdamW
from torch.optim.lr_scheduler import ReduceLROnPlateau


class BaseTask(LightningModule, ABC):
    """Abstract base class for all TorchGeo trainers.

    .. versionadded:: 0.5
    """

    #: Model to train
    model: Any

    #: Performance metric to monitor in learning rate scheduler and callbacks
    monitor = "val_loss"

    def __init__(self) -> None:
        """Initialize a new BaseTask instance."""
        super().__init__()
        self.save_hyperparameters()
        self.configure_losses()
        self.configure_metrics()
        self.configure_models()

    def configure_losses(self) -> None:
        """Initialize the loss criterion."""

    def configure_metrics(self) -> None:
        """Initialize the performance metrics."""

    @abstractmethod
    def configure_models(self) -> None:
        """Initialize the model."""

    def configure_optimizers(
        self,
    ) -> "lightning.pytorch.utilities.types.OptimizerLRSchedulerConfig":
        """Initialize the optimizer and learning rate scheduler.

        Returns:
            Optimizer and learning rate scheduler.
        """
        optimizer = AdamW(self.parameters(), lr=self.hparams["lr"])
        scheduler = ReduceLROnPlateau(optimizer, patience=self.hparams["patience"])
        return {
            "optimizer": optimizer,
            "lr_scheduler": {"scheduler": scheduler, "monitor": self.monitor},
        }

    def forward(self, *args: Any, **kwargs: Any) -> Any:
        """Forward pass of the model.

        Args:
            args: Arguments to pass to model.
            kwargs: Keyword arguments to pass to model.

        Returns:
            Output of the model.
        """
        return self.model(*args, **kwargs)