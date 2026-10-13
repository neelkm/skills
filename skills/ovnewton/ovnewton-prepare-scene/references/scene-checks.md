# Scene checks and physical meaning

## Units and coordinates

Ovnewton-built models retain the stage's length units. A centimetre stage can return positions in centimetres and linear velocities in centimetres per second. Do not relabel them as metres. If normalizing a scene, convert geometry, translations, velocities, gravity, inertia, and other dimensional physical quantities consistently; changing only metadata changes physical meaning.

USD angular joint state uses degrees and degrees/s. Native Newton joint arrays use radians and radians/s. Ovnewton's shared `jointPosition` and `jointVelocity` output fields convert angular axes back to degrees and degrees/s. Check the field, not just its shape.

Native `body_q` is body-origin world pose with XYZW quaternion order. Native `body_qd` contains world-frame center-of-mass linear velocity followed by angular velocity. A body-origin velocity and a center-of-mass velocity can differ when the body rotates.

## Mass and geometry

- Apply the intended physics schemas. A property with the right name can be ignored when its API schema is absent.
- Inspect the final model's mass, full body-frame inertia tensor, and local center-of-mass offset. A positive scalar mass does not establish that the inertia is sensible.
- Zero mass can be appropriate for static/kinematic behavior; do not replace every zero with an arbitrary positive number.
- Check collision shapes separately from visuals. A rendered mesh does not establish collision fidelity.
- Check nested transforms, non-uniform scale, reflections, and joint anchors. A transform decomposition that changes the mechanism is not a harmless import fix.
- Verify material bindings at each relevant collider. Partial inherited/collection-based binding support can change effective properties.

## Joints and controls

Check body0/body1 relationships, world attachments, articulation roots, axis directions, anchor frames, limits, and supported drive modes. Validate initial joint state and connected-body poses together. Ensure that a control target corresponds to the intended joint, units, and body order.

Use solver capability tables to verify limits, effort limits, armature, friction, and drives. The existence of an array in a Newton model does not establish that the selected solver enforces it. Stage runtime updates are narrower than initial model import.

## Public 0.2.0 boundaries

Check these against the installed release rather than assuming all future versions share them:

| Feature | Documented boundary | Appropriate response |
| --- | --- | --- |
| Native USD physics instances | Rejected | Explain the limitation; propose explicit composed copies only if they preserve the requested semantics. |
| Physics PointInstancer | Rejected | Do not silently omit its physics. |
| D6 per-axis runtime state | Not synchronized | Distinguish imported joint structure, direct Newton controls, and stage state updates. |
| Mimics involving D6 merges | Rejected when the required source axes cannot be preserved | Keep the intended coupling explicit; evaluate a supported representation. |
| Inherited/collection material binding | Partial support | Inspect final effective material values. |
| Surface cloth | Limited subset | Confirm non-kinematic enabled bodies, identity world transforms, constant thickness, density-derived mass, and supported material fields. |
| Newton actuator schemas, cables, volume deformables | Unsupported | Report the missing path; do not infer support from Newton alone. |

A standard joint drive is not the same feature as a Newton actuator-schema component. The actuator limitation does not mean all joint control is unsupported.

Recoverable import diagnostics may explain normalized or ignored inputs. Record diagnostic code and prim path. A warning-free import still needs task-specific verification; the importer can only evaluate the data visible through population.

## Sources

- [Public support snapshot](https://github.com/NVIDIA-Omniverse/ovnewton/blob/f5febec0718c19a23cb8c4cfd9cfdb9a2069515e/docs/site/support.md)
- [Output units and layouts](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/output-reads.md)
- [Model construction](https://github.com/NVIDIA-Omniverse/ovnewton/blob/main/docs/site/concepts.md)
- [Newton USD import](https://github.com/newton-physics/newton/blob/main/docs/concepts/usd_parsing.rst)
