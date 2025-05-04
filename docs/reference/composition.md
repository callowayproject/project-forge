# Composition

A [composition](api/project_forge/models/composition.md#project_forge.models.composition.Composition)
defines a set of overlays and methods of context manipulation.

The `steps` attribute contains the list of overlays.
The order is important.
Overlays later in the list can overwrite context items set by previous overlays.

Instead of having one overlay overwrite the context value of another,
you can specify that overlays merge changes to specific context values.
The `merge_keys` attribute defines which keys have their values merged,
and how those values are merged.
