import torch


def _get_optimal_batch_size() -> int:
    """GPU メモリに基づいて最適なバッチサイズを決定"""
    if not torch.cuda.is_available():
        return 1

    # モデルロード後の空きメモリを確認（より正確）
    free_memory_gb = torch.cuda.mem_get_info()[0] / 1024**3
    total_memory_gb = torch.cuda.mem_get_info()[1] / 1024**3

    print(f"GPU総メモリ: {total_memory_gb:.2f} GB")
    print(f"空きメモリ: {free_memory_gb:.2f} GB")

    # 空きメモリに基づいてバッチサイズを決定
    # translategemma-4bの場合、1サンプルあたり約100-200MBと想定
    if free_memory_gb < 2:
        return 4
    elif free_memory_gb < 4:
        return 8
    elif free_memory_gb < 8:
        return 16
    elif free_memory_gb < 12:
        return 32
    elif free_memory_gb < 20:
        return 64
    else:
        return 128


if torch.cuda.is_available():
    # デバイス数
    device_count = torch.cuda.device_count()
    print(f"利用可能なGPU数: {device_count}")

    for i in range(device_count):
        # GPU名
        gpu_name = torch.cuda.get_device_name(i)
        print(f"\nGPU {i}: {gpu_name}")

        # CUDAコア数に関連する情報
        props = torch.cuda.get_device_properties(i)
        print(f"  マルチプロセッサ数: {props.multi_processor_count}")
        print(f"  総メモリ: {props.total_memory / 1024**3:.2f} GB")
        print(f"  Compute Capability: {props.major}.{props.minor}")

        print(f"  最適バッチサイズの推定: {_get_optimal_batch_size()}")

        # 概算のCUDAコア数（アーキテクチャによる）
        # この値は正確ではないが目安になります
        cores_per_sm = {
            (3, 0): 192,
            (3, 5): 192,
            (3, 7): 192,  # Kepler
            (5, 0): 128,
            (5, 2): 128,  # Maxwell
            (6, 0): 64,
            (6, 1): 128,  # Pascal
            (7, 0): 64,
            (7, 5): 64,  # Volta, Turing
            (8, 0): 64,
            (8, 6): 128,  # Ampere
            (9, 0): 128,  # Hopper
        }.get((props.major, props.minor), 64)

        estimated_cores = props.multi_processor_count * cores_per_sm
        print(f"  推定CUDAコア数: {estimated_cores}")
else:
    print("CUDAが利用できません")
