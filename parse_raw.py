import time

from llama_cpp import Llama

def generate(
    user_input: str,
    system_prompt: str,
    max_tokens: int = 1024,
    temperature: float = 0.0,
    top_p: float = 1.0,
) -> str:
    """
    Generate text using a local GGUF Llama model.

    Args:
        user_input: User message/content
        system_prompt: System instruction/prompt
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        top_p: Top-p sampling

    Returns:
        Generated response as plain string
    """

    # Load once globally for better performance
    llm = Llama(
        model_path="Llama-3.2-1B-Instruct-IQ4_XS.gguf",
        n_ctx=2048,
        n_batch=1024,      # Increased for faster prompt processing
        n_threads=4,       # Match physical 'Big' cores (usually 4 on modern SoCs)
        n_threads_batch=8, # Use all cores for the initial prefill burst
        flash_attn=True,   # Critical for 1000+ token prompts
        use_mlock=True,    # Keep model in high-speed RAM
        temperature=0.0,
        max_tokens=1024,
        n_gpu_layers=-1,
        verbose=False
    )

    response = llm.create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_input,
            },
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )

    return response["choices"][0]["message"]["content"].strip()


# Example usage
with open("prompt.txt") as f:
    prompt = f.read()

with open("samples.txt") as f:
    text = f.read()

start = time.time()
output = generate(text, prompt)
end = time.time()

print("Time taken:",end-start)

print(output)