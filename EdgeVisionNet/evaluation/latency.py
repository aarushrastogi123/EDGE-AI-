import time
import numpy as np
import tensorflow as tf


def measure_latency_tf(model, dataset, num_samples: int = 100):
    total_time = 0.0
    samples = 0
    for x_batch, _ in dataset.unbatch().batch(1).take(num_samples):
        start = time.perf_counter()
        _ = model(x_batch, training=False)
        end = time.perf_counter()
        total_time += end - start
        samples += 1

    average_latency = total_time / max(samples, 1)
    fps = 1.0 / average_latency if average_latency > 0 else 0.0
    return {
        "average_latency_seconds": average_latency,
        "frames_per_second": fps,
        "samples_evaluated": samples,
    }


def measure_latency_tflite(interpreter: tf.lite.Interpreter, dataset, num_samples: int = 100):
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    total_time = 0.0
    samples = 0

    for x_batch, _ in dataset.unbatch().batch(1).take(num_samples):
        image = x_batch.numpy().astype(input_details["dtype"])
        interpreter.set_tensor(input_details["index"], image)
        start = time.perf_counter()
        interpreter.invoke()
        _ = interpreter.get_tensor(output_details["index"])
        end = time.perf_counter()
        total_time += end - start
        samples += 1

    average_latency = total_time / max(samples, 1)
    fps = 1.0 / average_latency if average_latency > 0 else 0.0
    return {
        "average_latency_seconds": average_latency,
        "frames_per_second": fps,
        "samples_evaluated": samples,
    }
