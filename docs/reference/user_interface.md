# User interface

- Provides interface for different types of questions, validation, error handling, etc

- messaging of status or state

- Abstract enough that it is pluggable for both console or web or other

- Interface

    - `type`
    - `prompt`
    - `help`
    - `choices`
    - `multiselect`
    - `default` (pre-rendered)
    - `validator` (a function to call to validate the input)

- Returns the answer
