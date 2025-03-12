#imports
from gpt4all import GPT4All
import os 

def get_user_input() -> str:
    """ function to get the inputs from the user."""
    dietary_preferences = input("Enter your dietary preferences: ")
    allergies = input("Enter any food allergies you have: ")
    return dietary_preferences, allergies


def build_prompt(dietary_preferences, allergies) -> str: 
    prompt = f"""
    You are an expert chef specializing in personalized recipe creation. Your task is to generate a unique, delicious dinner recipe based on the user's preferences.
    
    - The recipe must align with the following dietary preference(s): {dietary_preferences}.
    - The recipe must avoid these allergens: {allergies}.
    
    Provide a detailed recipe including:
    1. A creative and appetizing recipe name.
    2. A full list of ingredients (ensuring none of the allergens are included).
    3. Step-by-step cooking instructions.
    
    Follow the Chain-of-Thought (CoT) methodology to reason through ingredient selection before presenting the final recipe. Use an engaging and structured format.

    ###Example Recipe Format:
    
    **Recipe Name:** Creamy Tomato Basil Pasta (Dairy-Free)
    
    **Ingredients:**  
    - 2 cups gluten-free pasta  
    - 1 can (14 oz) crushed tomatoes  
    - 2 cloves garlic, minced  
    - 1 tbsp olive oil  
    - 1/2 tsp salt  
    - 1/4 tsp black pepper  
    - 1/4 cup fresh basil, chopped  
    
    **Instructions:**  
    1. Boil the pasta according to package instructions. Drain and set aside.  
    2. In a saucepan, heat olive oil over medium heat and sauté garlic until fragrant.  
    3. Add crushed tomatoes, salt, and pepper. Simmer for 10 minutes.  
    4. Stir in fresh basil and mix well.  
    5. Toss the cooked pasta with the sauce and serve warm.  

    Now, generate a **completely new recipe** that aligns with the given dietary preferences and avoids the specified allergens.
    """
    return prompt


def query_gpt4all(prompt):
    """Prompts local LLM and returns response"""
    model_path = os.path.join(os.getcwd(), "mistral-7b-openorca.Q4_K_M.gguf") #local downloaded model path

    try:
        #Force GPT4All to use the local model
        model = GPT4All(model_path, allow_download=False) #Prevents downloading
        response = model.generate(prompt, max_tokens=500)
        return response
    except Exception as e:
        return f"Error generating response: {e}"

def save_to_file(prompt, response):
    fp = os.path.join(os.getcwd(),"generated_recipe.txt" )
    with open(fp, "w", encoding="utf-8") as file:
        file.write("Prompt:\n")
        file.write(prompt + "\n\n")
        file.write("Generated Recipe:\n")
        file.write(response)
    print(f"Recipe saved to {fp}")

def main(): 
    dietary_preferences, allergies = get_user_input()
    prompt = build_prompt(dietary_preferences, allergies)
    response = query_gpt4all(prompt)
    print("\nGenerated Recipe:\n", response)
    save_to_file(prompt, response)

if __name__ == "__main__":
    main()