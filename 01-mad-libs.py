def get_input(word):
    user_input = input(f"Enter a {word} >> ")
    return user_input

def story():
    noun1 = get_input("Noun 1")
    noun2 = get_input("Noun 2")
    verb1 = get_input("Verb 1")
    verb2 = get_input("Verb 2")
    adj1 = get_input("Adjective 1")
    adj2 = get_input("Adjective 2")
    adj3 = get_input("Adjective 3")

    story = f"""
    One sunny morning, a {adj1} {noun1} woke up with an unstoppable urge to {verb1}. 
    Without thinking twice, the {adj1} {noun1} started {verb1}ing everywhere—on the table, 
    on the floor, and even in places where {verb1}ing absolutely made no sense at all.

    Suddenly, a {adj2} {noun2} appeared, stared for a moment, and decided that this was 
    way too weird to ignore. Instead of asking questions, the {adj2} {noun2} joined in, 
    and together they went off to {verb2} like two {adj3} friends on the strangest adventure ever.

    And that’s how a {adj1} {noun1} and a {adj2} {noun2} accidentally became 
    {adj3} legends of {verb2}ing.
    """

    print(story)


if __name__ == "__main__":
    story()