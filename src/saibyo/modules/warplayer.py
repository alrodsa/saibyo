import torch

backwarp_grid_cache = {}

def warp(
    input_tensor: torch.Tensor,
    flow_tensor: torch.Tensor,
    device: torch.device
) -> torch.Tensor:
    """
    Warp the input tensor using the flow tensor.
    The flow tensor is expected to be in the format of (batch_size, 2, height,
    width), where the first channel represents the horizontal flow and the
    second channel represents the vertical flow.
    The input tensor is expected to be in the format of (batch_size, channels,
    height, width).

    Parameters
    ----------
    input_tensor : torch.Tensor
        The input tensor to be warped.
    flow_tensor : torch.Tensor
        The flow tensor used for warping.
    device : torch.device
        The device on which the tensors are located.

    Returns
    -------
    torch.Tensor
        The warped tensor.

    """
    key = (str(flow_tensor.device), str(flow_tensor.size()))

    if key not in backwarp_grid_cache:
        horizontal = torch.linspace(
            -1.0, 1.0, flow_tensor.shape[3], device=device
        ).view(
            1, 1, 1, flow_tensor.shape[3]
        ).expand(flow_tensor.shape[0], -1, flow_tensor.shape[2], -1)

        vertical = torch.linspace(
            -1.0, 1.0, flow_tensor.shape[2], device=device
        ).view(
            1, 1, flow_tensor.shape[2], 1
        ).expand(flow_tensor.shape[0], -1, -1, flow_tensor.shape[3])

        backwarp_grid_cache[key] = torch.cat(
            [horizontal, vertical], dim=1
        ).to(device)

    normalized_flow = torch.cat([
        flow_tensor[:, 0:1, :, :] / ((input_tensor.shape[3] - 1.0) / 2.0),
        flow_tensor[:, 1:2, :, :] / ((input_tensor.shape[2] - 1.0) / 2.0)
    ], dim=1)

    sampling_grid = (
        backwarp_grid_cache[key] + normalized_flow
    ).permute(0, 2, 3, 1)

    return torch.nn.functional.grid_sample(
        input=input_tensor,
        grid=sampling_grid,
        mode="bilinear",
        padding_mode="border",
        align_corners=True
    )
