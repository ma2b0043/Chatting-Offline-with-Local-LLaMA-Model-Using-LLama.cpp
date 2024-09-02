from llama_cpp import Llama
import re

def load_model(model_path):
    """Load the LLaMA model from the specified path."""
    try:
        # Initialize the model
        llm = Llama(
            model_path=model_path,
            # Configure these parameters if needed
            # n_gpu_layers=-1, # For GPU acceleration
            # seed=1337, # Set a specific seed
            # n_ctx=2048, # Increase the context window
        )
        return llm
    except Exception as e:
        print(f"Failed to load model: {e}")
        return None

def chat_with_model(model, prompt, temperature=0.3):
    """Generate a response from the model based on the provided prompt."""
    try:
        output = model.create_chat_completion(
            messages=[
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_object",
            },
            temperature=temperature  # Set the temperature parameter here
        )
        
        # Extract the response text from the output
        response_text = output['choices'][0]['message']['content']
        return response_text.strip()
    except Exception as e:
        print(f"Error during model inference: {e}")
        return "Error generating response."

def main():
    # Define the path to your model
    model_path = './models/meta-llama-3.1-8b-instruct-q6_k.gguf'
    
    # Load the model
    model = load_model(model_path)
    if not model:
        print("Model could not be loaded. Exiting.")
        return
    
    print("Chatbot is ready! Type 'exit' to end the conversation.")
    
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            print("LLama: Goodbye!")
            break
        
        # Prepare the prompt for the model
        prompt = user_input  # Directly pass user input as prompt
        
        # Get the model's response with the desired temperature
        response = chat_with_model(model, prompt, temperature=0.7)
        print(f"LLama: {response}")

if __name__ == "__main__":
    main()
