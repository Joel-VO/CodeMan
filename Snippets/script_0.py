def get_user_input(prompt):
    return input(prompt)

def generate_mad_lib():
    # Prompt user for inputs
    name = get_user_input("Enter a person's name: ")
    adjective1 = get_user_input("Enter an adjective: ")
    verb1 = get_user_input("Enter a verb (past tense): ")
    noun1 = get_user_input("Enter a noun: ")
    
    adj2 = get_user_input("Enter another adjective: ")
    place = get_user_input("Enter a place: ")
    verb2 = get_user_input("Enter a verb: ")
    noun2 = get_user_input("Enter another noun: ")

    # Generate the story
    story = f"Once upon a time, there was a {adjective1} person named {name}. " \
            f"One day, {name} {verb1} to a {noun1} in {place}. " \
            f"Upon arrival, {name} found out that the {noun1} was actually a {adj2} {noun2}. " \
            f"{Name} decided to {verb2} and explore it further. The end!"

    return story

# Main function to run the game
def main():
    print("Welcome to Mad Libs!")
    print(generate_mad_lib())

if __name__ == "__main__":
    main()