# Context

The context holds the variables available when rendering a template. It is a nested key/value data structure.

## Building the context

Patterns provide the core context by asking the user a question and associating the answer with a key.

Patterns, Overlays, and Compositions all have `extra_context` attributes that provide a method to add key/values to the context without prompting the user.

Overlays provide an `answer_map` attribute to map one pattern key/value to another.

Compositions use `merge_keys` to merge the values of common pattern keys.

Contexts are built iteratively question by question and pattern by pattern.

The default answer of a question to be the answer to a previous question.

Patterns may have keys that whose answers should be the same, but their keys are different. For example, one pattern might use `project_name` and another might use `library_name`. The overlay's `answer_map` allows you to map the answer of `project_name` to answer of `library_name`.

Patterns that define complex data structures, such as `list`s or `dict`s, may be merged between patterns using the composition's `merge_keys` attribute. For example, if several patterns define a `requirements` dict as in their `extra_context`, you can have the composition merge all the values of `requirements`.
