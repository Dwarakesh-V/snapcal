import time
from llama_cpp import Llama

print("Loading model into memory... (Please wait)")
load_start = time.time()

# Load once globally for better performance
llm = Llama(
    model_path="Llama-3.2-1B-Instruct-IQ4_XS.gguf",

    # Keep context smaller for speed
    n_ctx=1024,

    # Bigger batch = better throughput until VRAM fills
    n_batch=2048,
    n_ubatch=2048,


    # GPU acceleration
    n_gpu_layers=-1,      # offload everything possible

    # Fast attention kernels
    flash_attn=True,

    # Memory options
    use_mlock=False,      # usually slower startup/no major speed gain
    use_mmap=True,

    # Performance flags
    logits_all=False,
    embedding=False,

    # Rope scaling off unless needed
    rope_freq_base=0,
    rope_freq_scale=0,

    # Misc
    verbose=False
)

load_end = time.time()
print(f"Model Load Time: {load_end - load_start:.2f} seconds\n")

def generate_with_metrics(
    user_input: str,
    system_prompt: str,
    max_tokens: int = 256,
    temperature: float = 0.0,
    top_p: float = 1.0,
) -> str:
    """
    Generate text using a local GGUF Llama model while tracking detailed timing metrics.
    """
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    total_start_time = time.time()

    # We use stream=True so we can intercept the exact moment the first token arrives
    response_generator = llm.create_chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True 
    )

    first_token_time = None
    generated_text = ""
    token_count = 0

    # Stream processing loop
    for chunk in response_generator:
        # Capture Time to First Token
        if first_token_time is None:
            first_token_time = time.time()

        delta = chunk["choices"][0].get("delta", {})
        if "content" in delta:
            generated_text += delta["content"]
            token_count += 1

    end_time = time.time()

    # TTFT (Time to First Token) covers the Prompt Evaluation / Prefill phase
    ttft = first_token_time - total_start_time
    
    # Generation Time covers the decoding phase (producing new tokens)
    generation_time = end_time - first_token_time
    total_time = end_time - total_start_time
    
    tokens_per_second = token_count / generation_time if generation_time > 0 else 0

    print("--- Performance Metrics ---")
    print(f"Prefill Time (TTFT):   {ttft:.3f} seconds (Prompt Processing)")
    print(f"Generation Time:       {generation_time:.3f} seconds")
    print(f"Total Inference Time:  {total_time:.3f} seconds")
    print(f"Tokens Generated:      {token_count} tokens")
    print(f"Decode Speed:          {tokens_per_second:.2f} tokens/sec")
    print("---------------------------\n")

    return generated_text.strip()

with open("prompt.txt") as f:
        prompt = f.read()

with open("samples.txt") as f:
    text = f.read()

# text = """
# We have distributed systems test on January 10th.
# """

print("Cold Run")
output_1 = generate_with_metrics(text, prompt)
print(f"Output:\n{output_1}\n")

print("Warm Run (KV Caching)")
output_2 = generate_with_metrics(text, prompt)
print(f"Output:\n{output_2}\n")