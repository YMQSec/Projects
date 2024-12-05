# Password Strength Analyzer

The **Password Strength Analyzer** is a Python-based tool designed to evaluate the strength of a password and provide actionable feedback for improving its security. This tool helps users create stronger passwords by analyzing length, character diversity, and complexity.

---

## Features

- **Password Strength Evaluation**:
  - Categorizes passwords as **Weak**, **Medium**, or **Strong**.
  - Scores passwords based on length, use of uppercase/lowercase letters, numbers, and special characters.
  
- **Feedback and Suggestions**:
  - Provides actionable tips to enhance password security.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher. Download it from [Python.org](https://www.python.org).

### Installation

```bash
# Clone this repository
git clone https://github.com/YMQSec/Projects.git

# Navigate to the Password Strength Analyzer directory
cd Projects/Password\ Strength\ Analyzer

# Run the script
python password_strength.py
```

## Usage
```bash
# Execute the script in your terminal
python password_strength.py
```
#### When prompted, enter a password to evaluate its strength. For example:

`Enter your password: MyPassword123!`

#### The program will output an analysis like the following:

`Password Strength: Medium`

#### Feedback:
- Password length is acceptable but could be longer.
- Good mix of uppercase and lowercase letters.
- Includes numbers.
- Add special characters for a stronger password.

## Example Outputs

#### Weak Password
`Input: 12345`

``Output: Password Strength: Weak``

##### Feedback:
- Password is too short. Use at least 12 characters.
- Add both uppercase and lowercase letters.
- Add some numbers.
- Add special characters for a stronger password.

#### Strong Password
`Input: SecureP@ssw0rd123`

``Output: Password Strength: Strong``

##### Feedback:
- Password length is strong.
- Good mix of uppercase and lowercase letters.
- Includes numbers.
- Includes special characters.

## How It Works

The Password Strength Analyzer evaluates passwords based on the following criteria:

#### Length:
- Strong passwords are at least 12 characters long.

#### Character Diversity:
- Checks for a mix of uppercase and lowercase letters.
- Verifies the inclusion of numbers and special characters.

#### Scoring System:
- Assigns points for each criterion met.
- Categorizes the overall password strength based on the score.

## Testing
To ensure the program works as expected, use the following example test cases:

```bash
from password_strength import check_password_strength

def test_password_strength():
    assert check_password_strength("12345")['strength'] == "Weak"
    assert check_password_strength("StrongP@ssw0rd123")['strength'] == "Strong"
    print("All tests passed!")

# Run the test script:
python test_password_strength.py
```
## Future Enhancements

#### Real-time Validation:
  - Integrate the tool into a graphical user interface (GUI) or web application.

#### Common Password Detection:
  - Warn users if their password is commonly used or appears in leaked password databases.

#### Localization:
  - Provide feedback in multiple languages.

---

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the repository**: Create your own copy of the project.
2. **Create a new branch**: Use a descriptive name for your branch.
```bash
  git checkout -b feature-branch-name
```
4. **Commit your changes**:
```bash
  git commit -m "Add your descriptive commit message here"
```
4. **Push the branch**:
```bash
  git push origin feature-branch-name
```
5. **Open a Pull Request.**

---

## License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## Author

**Yansiel Melendez**  
GitHub: [YMQSec](https://github.com/YMQSec)