# TDGT UHC 2026

# Import hashlib for hashing capabilities and json so it can understand 
import hashlib
import json

# Function to produce hash as required
def produce_hash(string_to_hash):
    hashed_object = hashlib.sha256(string_to_hash.encode('utf-8'))
    return hashed_object.hexdigest()

# Keeps program running until user chooses to exit 
user_wants_to_continue = True

# While the user is wanting to continue, the main loop will run
while user_wants_to_continue:

    # Ask for JSON file or exit
    user_file = input("Enter your json file path or [E] to exit: ")
    # If uppercase or lowercase, exit will work regardless. States [e] as exit command
    if user_file.lower() == 'e':
        print("Goodbye!")
        # Ends program
        user_wants_to_continue = False
        continue

    try:
        # Open the json file in read mode
        json_file = open(user_file, 'r')
        # Creates a variable, then loading the json files data into it (users as it loads the username and hash)
        users = json.load(json_file)
        # Closes json file
        json_file.close()
    # Error block for json file if it is broken in anyway 
    except:
        print("Error loading JSON file, make sure it is written correctly")
        # Continues to next line of code
        continue

    # Open rockyou.txt using latin-1 encoding
    try:
        file_list = open("rockyou.txt", 'r', encoding='latin-1')
        # splits lines into singular words
        words = file_list.read().splitlines()
        # Closes file after data has been put into words variable
        file_list.close()
    # Error block for if rockyou.txt is not in the same folder as program
    except:
        print("Rockyou.txt file not found, make sure it is in the same folder as UHC program")
        # continues to next line of code
        continue

    # Store word list in 'passwords' for dictionary building
    passwords = words

    # Build dictionary of hashes from rockyou.txt wordlist
    password_dict = {}
    # Takes passwords in rockyou and puts them under variable fast_hash
    for fast_hash in passwords:
        # produce_hash turns fast_hash passwords into hashed form, then put into hashed_password
        hashed_password = produce_hash(fast_hash)
        # Puts the hashed password into dictionary
        password_dict[hashed_password] = fast_hash

    # list for results
    results = []

    # Loop through users in the json
    for user in users:
        username = user['user_name']
        user_hash = user['user_password']

        # Directly checks the user's hash in the dictionary instead of looping through every password, making the lookup much faster and cleaner
        if user_hash in password_dict:
            found_password = password_dict[user_hash]
        # If password is not found, it is defaulted to "" (blank)
        else:
            found_password = ""
            
        # Creates variable for the "" (blank) found_password so it can be used in the json output file
        match_found = found_password != ""

        # Append entries of user data for printing and json dumping
        results.append({
            'username': username,
            'password': found_password,
            'password_found': match_found
        })

    # Print results cleanly
    for ending_result in results:
        # Creates variable for the username 
        username = ending_result['username']
        # Creates variable for the password_found
        password_found = ending_result['password_found']

        # Checks if password was found or not stating "Match Found" if so and "No Match" if not 
        if password_found:
            print(username + ": Match Found")
        else:
            print(username + ": No Match")

    # Save results to JSON and make it readable to people through indentation
    try:
        # Opens in write to be able to create/write in results.json
        output_file = open("results.json", 'w')
        # Dumps the results list into output_file variable at an indentation of 4 (easy readability) 
        json.dump(results, output_file, indent=4)
        # Closes output_file as it is not needed anymore
        output_file.close()
        print("Results saved to results.json")
    # States to user an error has occured, breaking off code
    except:
        print("Error saving results, program will end, please open and try again")
        user_wants_to_continue = False
        
