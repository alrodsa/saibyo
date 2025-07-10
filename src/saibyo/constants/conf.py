COMPARATION_DESCRIPTION = (
    "Creates an extra video that compares the original video with the "
    "interpolated video, showing the differences between them."
)
LIGHTWEIGHT_DESCRIPTION = (
    "If set to True, the model inference will be performed using fp16 precision, "
    "which is faster and uses less memory, but may result in lower quality output."
)
EXPONENTIAL_DESCRIPTION = (
    "The value of the exponential parameter is used to determine the value of the"
    " fps multiplier, which is calculated as 2 ** exponential. For example:\n"
    "\t- If exponential is 1, the fps multiplier is 2 ** 1 = 2, resulting in "
    "double the frames.\n"
    "\t- If exponential is 2, the fps multiplier is 2 ** 2 = 4, resulting in "
    "quadruple the frames.\n"
    "\t- If exponential is 3, the fps multiplier is 2 ** 3 = 8, resulting in "
    "eight times the frames.\n"
    "This allows for flexible control over the frame rate increase during "
    "interpolation."
)
