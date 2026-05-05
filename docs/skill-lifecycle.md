# Skill Lifecycle

Skills are reusable operational packages. They are progressively disclosed: summaries can be visible early, while full instructions load only when activation criteria are met.

## Skill states

```text
draft
tested
reviewed
active
deprecated
revoked
```

## Minimum skill manifest fields

```text
id
name
summary
activation_criteria
full_instruction_path
required_tools
required_model_class
allowed_side_effects
policy_constraints
memory_inputs
evidence_outputs
evals
version
owner_repo
state
```

## Activation evidence

Every skill activation must record:

- skill id and version;
- activation reason summary;
- required grants;
- required policy checks;
- side-effect class;
- trace level;
- evidence outputs.

## M1 rule

M1 uses only the built-in deterministic `superconscious-basic-planner` skill. It has no side effects and requires no model call.
