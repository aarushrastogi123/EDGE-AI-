import logging

logger = logging.getLogger(__name__)


def apply_pruning(model, pruning_fraction: float = 0.2):
    try:
        import tensorflow_model_optimization as tfmot
    except ImportError:
        logger.warning(
            "TensorFlow Model Optimization is not installed. Pruning will be skipped."
        )
        return model

    pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
        initial_sparsity=0.0,
        final_sparsity=pruning_fraction,
        begin_step=0,
        end_step=1000,
    )

    prune_low_magnitude = tfmot.sparsity.keras.prune_low_magnitude
    model = prune_low_magnitude(model, pruning_schedule=pruning_schedule)
    logger.info("Applied pruning wrapper to model. You still need to recompile and retrain for sparse weights.")
    return model
